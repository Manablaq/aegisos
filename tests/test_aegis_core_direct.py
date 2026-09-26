from __future__ import annotations

import hashlib
from pathlib import Path

from gltest.direct import (
    VMContext,
    deploy_contract,
)


CANDIDATE = (
    Path(__file__).resolve().parents[1]
    / "contracts"
    / "aegis_core.py"
)

EXPECTED_CANDIDATE_SHA = (
    "df7f279e651681a24fdb3b0f71079edb"
    "64ebdf45a0e5c398806804f07fb3d21b"
)

SDK_VERSION = "v0.2.16"

BASE_ISO = "2026-09-22T20:00:00Z"
ADJUDICATE_ISO = "2026-09-22T20:01:01Z"

BASE_TS = 1790107200

PUBLISHED_AT = BASE_TS - 30
EVIDENCE_EXPIRES_AT = BASE_TS + 1800
RECOVERY_DEADLINE = BASE_TS + 3600

CHALLENGE_WINDOW_SECONDS = 60
MAX_EVIDENCE_AGE_SECONDS = 600

GENERATION = 1
PRINCIPAL = 1000

STATE_ACTIVE = 2
STATE_CHALLENGE_WINDOW = 3
STATE_REPAIR_REQUIRED = 5
STATE_DECISION_RECORDED = 7

OUTCOME_CREATOR = 1
OUTCOME_COUNTERPARTY = 2

CONSEQUENCE_PAY_CREATOR = 1
CONSEQUENCE_PAY_COUNTERPARTY = 2

AUTHORITY_ROLE_PRIMARY = 1
AUTHORITY_ROLE_CORROBORATOR = 2

POLICY_TEXT = (
    "Policy v1: resolve the full principal only from "
    "fresh authenticated independent evidence."
)

AUTHORITY_TEXT = (
    "Authority set v1: PRIMARY and CORROBORATOR are "
    "distinct bound authorities."
)

PRIMARY_EVIDENCE_TEXT = (
    "Primary evidence v1: the authenticated record "
    "supports the tested adjudication request."
)

CORROBORATING_EVIDENCE_TEXT = (
    "Corroborating evidence v1: an independent "
    "authenticated record corroborates the request."
)


def _sha_text(value: str) -> str:
    return hashlib.sha256(
        value.encode("utf-8")
    ).hexdigest()


def _raw_address(seed: str) -> bytes:
    return hashlib.sha256(
        seed.encode("utf-8")
    ).digest()[:20]


def _hex_address(value: bytes) -> str:
    return "0x" + value.hex()


def _candidate_sha() -> str:
    return hashlib.sha256(
        CANDIDATE.read_bytes()
    ).hexdigest()


def _assert_candidate_frozen() -> None:
    assert CANDIDATE.is_file()
    assert (
        _candidate_sha()
        == EXPECTED_CANDIDATE_SHA
    )

    source = CANDIDATE.read_text(
        encoding="utf-8"
    )

    required_constants = (
        "STATE_ACTIVE = 2",
        "STATE_CHALLENGE_WINDOW = 3",
        "STATE_REPAIR_REQUIRED = 5",
        "STATE_DECISION_RECORDED = 7",
        "OUTCOME_CREATOR = 1",
        "OUTCOME_COUNTERPARTY = 2",
        "CONSEQUENCE_PAY_CREATOR = 1",
        "CONSEQUENCE_PAY_COUNTERPARTY = 2",
        "AUTHORITY_ROLE_PRIMARY = 1",
        "AUTHORITY_ROLE_CORROBORATOR = 2",
    )

    for declaration in required_constants:
        assert declaration in source


def _set_actor(
    vm: VMContext,
    sender: bytes,
    origin: bytes | None = None,
) -> None:
    vm.sender = sender
    vm.origin = (
        sender
        if origin is None
        else origin
    )


def _actors(
    agreement_id: str,
) -> dict[str, bytes]:
    return {
        "creator":
            _raw_address(
                "creator:" + agreement_id
            ),
        "counterparty":
            _raw_address(
                "counterparty:" + agreement_id
            ),
        "primary":
            _raw_address(
                "primary:" + agreement_id
            ),
        "corroborator":
            _raw_address(
                "corroborator:" + agreement_id
            ),
        "intruder":
            _raw_address(
                "intruder:" + agreement_id
            ),
    }


def _new_accepted_contract(
    vm: VMContext,
    agreement_id: str,
):
    _assert_candidate_frozen()

    actors = _actors(
        agreement_id
    )

    _set_actor(
        vm,
        actors["creator"],
    )

    contract = deploy_contract(
        CANDIDATE,
        vm,
        sdk_version=SDK_VERSION,
    )

    contract.create_probe(
        agreement_id,
        _hex_address(
            actors["counterparty"]
        ),
        _sha_text(POLICY_TEXT),
        _sha_text(AUTHORITY_TEXT),
        _hex_address(
            actors["primary"]
        ),
        _hex_address(
            actors["corroborator"]
        ),
        PRINCIPAL,
        CHALLENGE_WINDOW_SECONDS,
        MAX_EVIDENCE_AGE_SECONDS,
        RECOVERY_DEADLINE,
    )

    _set_actor(
        vm,
        actors["counterparty"],
    )

    contract.accept_probe(
        agreement_id
    )

    record = contract.get_probe(
        agreement_id
    )

    assert bool(record.accepted) is True
    assert int(record.state) == STATE_ACTIVE

    assert (
        record.creator.as_hex.lower()
        == _hex_address(
            actors["creator"]
        )
    )

    assert (
        record.counterparty.as_hex.lower()
        == _hex_address(
            actors["counterparty"]
        )
    )

    return {
        "contract": contract,
        "agreement_id": agreement_id,
        "actors": actors,
    }


def _attest_call(
    env: dict,
    role: int,
) -> None:
    contract = env["contract"]
    agreement_id = env["agreement_id"]

    if role == AUTHORITY_ROLE_PRIMARY:
        record_id = (
            agreement_id
            + "-primary-record"
        )
        source_ref = (
            "immutable://primary/"
            + agreement_id
            + "/v1"
        )
        evidence_text = (
            PRIMARY_EVIDENCE_TEXT
        )
        source_material = (
            "primary-source-content:"
            + agreement_id
        )

    elif (
        role
        == AUTHORITY_ROLE_CORROBORATOR
    ):
        record_id = (
            agreement_id
            + "-corroborator-record"
        )
        source_ref = (
            "immutable://corroborator/"
            + agreement_id
            + "/v1"
        )
        evidence_text = (
            CORROBORATING_EVIDENCE_TEXT
        )
        source_material = (
            "corroborator-source-content:"
            + agreement_id
        )

    else:
        raise AssertionError(
            "invalid test role"
        )

    contract.attest_evidence_probe(
        agreement_id,
        role,
        record_id,
        "v1",
        source_ref,
        _sha_text(
            evidence_text
        ),
        _sha_text(
            source_material
        ),
        PUBLISHED_AT,
        EVIDENCE_EXPIRES_AT,
        GENERATION,
    )


def _prepare_adjudication(
    vm: VMContext,
    agreement_id: str,
):
    env = _new_accepted_contract(
        vm,
        agreement_id,
    )

    actors = env["actors"]
    contract = env["contract"]

    _set_actor(
        vm,
        actors["primary"],
    )

    _attest_call(
        env,
        AUTHORITY_ROLE_PRIMARY,
    )

    _set_actor(
        vm,
        actors["corroborator"],
    )

    _attest_call(
        env,
        AUTHORITY_ROLE_CORROBORATOR,
    )

    primary = contract.get_attestation(
        agreement_id,
        AUTHORITY_ROLE_PRIMARY,
    )

    corroborator = contract.get_attestation(
        agreement_id,
        AUTHORITY_ROLE_CORROBORATOR,
    )

    assert bool(primary.present) is True
    assert bool(corroborator.present) is True

    assert (
        primary.authority.as_hex.lower()
        == _hex_address(
            actors["primary"]
        )
    )

    assert (
        corroborator.authority.as_hex.lower()
        == _hex_address(
            actors["corroborator"]
        )
    )

    assert (
        primary.evidence_record_id
        != corroborator.evidence_record_id
    )

    assert (
        primary.immutable_source_ref
        != corroborator.immutable_source_ref
    )

    _set_actor(
        vm,
        actors["creator"],
    )

    contract.bind_evidence_probe(
        agreement_id,
        GENERATION,
    )

    record = contract.get_probe(
        agreement_id
    )

    assert (
        int(record.state)
        == STATE_CHALLENGE_WINDOW
    )

    assert (
        int(record.generation)
        == GENERATION
    )

    assert (
        int(record.challenge_deadline)
        == BASE_TS
        + CHALLENGE_WINDOW_SECONDS
    )

    assert (
        int(record.evidence_expires_at)
        == EVIDENCE_EXPIRES_AT
    )

    vm.warp(
        ADJUDICATE_ISO
    )

    return env


def _leader_adjudicate(
    vm: VMContext,
    env: dict,
    decision: str,
) -> None:
    vm.clear_validators()
    vm.clear_mocks()

    vm.mock_llm(
        r".*",
        decision,
    )

    _set_actor(
        vm,
        env["actors"]["creator"],
    )

    env["contract"].adjudicate_probe(
        env["agreement_id"],
        POLICY_TEXT,
        AUTHORITY_TEXT,
        PRIMARY_EVIDENCE_TEXT,
        CORROBORATING_EVIDENCE_TEXT,
        "",
    )


def _validator_agrees(
    vm: VMContext,
    decision: str,
) -> None:
    vm.clear_mocks()

    vm.mock_llm(
        r".*",
        decision,
    )

    assert (
        vm.run_validator()
        is True
    )


def test_direct_authority_accepts_matching_sender_and_origin():
    vm = VMContext()
    vm.warp(BASE_ISO)

    with vm.activate():
        env = _new_accepted_contract(
            vm,
            "authority-accept",
        )

        primary = env[
            "actors"
        ]["primary"]

        _set_actor(
            vm,
            primary,
        )

        _attest_call(
            env,
            AUTHORITY_ROLE_PRIMARY,
        )

        attestation = (
            env["contract"]
            .get_attestation(
                env["agreement_id"],
                AUTHORITY_ROLE_PRIMARY,
            )
        )

        assert (
            bool(attestation.present)
            is True
        )

        assert (
            int(attestation.generation)
            == GENERATION
        )

        assert (
            attestation.authority.as_hex.lower()
            == _hex_address(primary)
        )

    print(
        "R60_CASE_AUTHORITY_ACCEPT=PASS"
    )


def test_direct_authority_rejects_foreign_sender():
    vm = VMContext()
    vm.warp(BASE_ISO)

    with vm.activate():
        env = _new_accepted_contract(
            vm,
            "authority-foreign-sender",
        )

        actors = env["actors"]

        _set_actor(
            vm,
            actors["intruder"],
            actors["primary"],
        )

        with vm.expect_revert(
            "BOUND_AUTHORITY_ONLY"
        ):
            _attest_call(
                env,
                AUTHORITY_ROLE_PRIMARY,
            )

    print(
        "R60_CASE_FOREIGN_SENDER_REJECT=PASS"
    )


def test_direct_authority_accepts_matching_sender_with_divergent_origin_runtime_compatibility():
    vm = VMContext()
    vm.warp(BASE_ISO)
    with vm.activate():
        env = _new_accepted_contract(
            vm,
            "authority-runtime-origin-divergence",
        )
        actors = env["actors"]
        _set_actor(
            vm,
            actors["primary"],
            actors["intruder"],
        )
        _attest_call(
            env,
            AUTHORITY_ROLE_PRIMARY,
        )
        attestation = env["contract"].get_attestation(
            env["agreement_id"],
            AUTHORITY_ROLE_PRIMARY,
        )
        assert bool(attestation.present) is True
        assert int(attestation.generation) == GENERATION
        assert (
            attestation.authority.as_hex.lower()
            == _hex_address(actors["primary"])
        )
    print(
        "R94_R9_CASE_MATCHING_SENDER_DIVERGENT_ORIGIN_ACCEPT=PASS"
    )


def test_creator_decision_and_validator_agreement():
    vm = VMContext()
    vm.warp(BASE_ISO)

    with vm.activate():
        env = _prepare_adjudication(
            vm,
            "decision-creator",
        )

        _leader_adjudicate(
            vm,
            env,
            "CREATOR",
        )

        record = env["contract"].get_probe(
            env["agreement_id"]
        )

        assert (
            bool(record.decision_recorded)
            is True
        )

        assert (
            int(record.state)
            == STATE_DECISION_RECORDED
        )

        assert (
            int(record.outcome_code)
            == OUTCOME_CREATOR
        )

        assert (
            int(record.consequence_code)
            == CONSEQUENCE_PAY_CREATOR
        )

        assert (
            record.beneficiary.as_hex.lower()
            == _hex_address(
                env["actors"]["creator"]
            )
        )

        assert (
            int(record.entitlement_amount)
            == PRINCIPAL
        )

        assert (
            len(record.decision_digest)
            == 64
        )

        _validator_agrees(
            vm,
            "CREATOR",
        )

    print(
        "R60_CASE_CREATOR_AGREEMENT=PASS"
    )


def test_counterparty_decision_and_validator_agreement():
    vm = VMContext()
    vm.warp(BASE_ISO)

    with vm.activate():
        env = _prepare_adjudication(
            vm,
            "decision-counterparty",
        )

        _leader_adjudicate(
            vm,
            env,
            "COUNTERPARTY",
        )

        record = env["contract"].get_probe(
            env["agreement_id"]
        )

        assert (
            bool(record.decision_recorded)
            is True
        )

        assert (
            int(record.state)
            == STATE_DECISION_RECORDED
        )

        assert (
            int(record.outcome_code)
            == OUTCOME_COUNTERPARTY
        )

        assert (
            int(record.consequence_code)
            == CONSEQUENCE_PAY_COUNTERPARTY
        )

        assert (
            record.beneficiary.as_hex.lower()
            == _hex_address(
                env["actors"][
                    "counterparty"
                ]
            )
        )

        assert (
            int(record.entitlement_amount)
            == PRINCIPAL
        )

        assert (
            len(record.decision_digest)
            == 64
        )

        _validator_agrees(
            vm,
            "COUNTERPARTY",
        )

    print(
        "R60_CASE_COUNTERPARTY_AGREEMENT=PASS"
    )


def test_repair_decision_and_validator_agreement():
    vm = VMContext()
    vm.warp(BASE_ISO)

    with vm.activate():
        env = _prepare_adjudication(
            vm,
            "decision-repair",
        )

        _leader_adjudicate(
            vm,
            env,
            "REPAIR",
        )

        record = env["contract"].get_probe(
            env["agreement_id"]
        )

        assert (
            bool(record.decision_recorded)
            is False
        )

        assert (
            int(record.state)
            == STATE_REPAIR_REQUIRED
        )

        assert int(
            record.outcome_code
        ) == 0

        assert int(
            record.consequence_code
        ) == 0

        assert int(
            record.entitlement_amount
        ) == 0

        assert (
            record.decision_digest
            == ""
        )

        _validator_agrees(
            vm,
            "REPAIR",
        )

    print(
        "R60_CASE_REPAIR_AGREEMENT=PASS"
    )


def test_validator_rejects_exact_decision_disagreement():
    vm = VMContext()
    vm.warp(BASE_ISO)

    with vm.activate():
        env = _prepare_adjudication(
            vm,
            "validator-disagreement",
        )

        _leader_adjudicate(
            vm,
            env,
            "CREATOR",
        )

        vm.clear_mocks()

        vm.mock_llm(
            r".*",
            "COUNTERPARTY",
        )

        assert (
            vm.run_validator()
            is False
        )

    print(
        "R60_CASE_VALIDATOR_DISAGREEMENT=PASS"
    )


def test_validator_rejects_invalid_results_and_leader_error():
    vm = VMContext()
    vm.warp(BASE_ISO)

    with vm.activate():
        env = _prepare_adjudication(
            vm,
            "validator-invalid-results",
        )

        _leader_adjudicate(
            vm,
            env,
            "CREATOR",
        )

        assert (
            vm.run_validator(
                leader_result="INVALID"
            )
            is False
        )

        assert (
            vm.run_validator(
                leader_error=RuntimeError(
                    "forced leader error"
                )
            )
            is False
        )

        vm.clear_mocks()

        vm.mock_llm(
            r".*",
            "INVALID",
        )

        assert (
            vm.run_validator()
            is False
        )

    print(
        "R60_CASE_INVALID_RESULT_REJECTION=PASS"
    )


def test_direct_authority_rejects_nonempty_call_stack():
    vm = VMContext()
    vm.warp(BASE_ISO)

    with vm.activate():
        env = _new_accepted_contract(
            vm,
            "authority-nonempty-stack",
        )

        actors = env["actors"]

        _set_actor(
            vm,
            actors["primary"],
            actors["intruder"],
        )

        from genlayer import gl

        assert "stack" in gl.message_raw

        assert len(
            gl.message_raw[
                "stack"
            ]
        ) == 0

        caller = (
            gl.message.contract_address
        )

        gl.message_raw[
            "stack"
        ] = [
            caller,
        ]

        assert len(
            gl.message_raw[
                "stack"
            ]
        ) == 1

        with vm.expect_revert(
            "DIRECT_AUTHORITY_TRANSACTION_REQUIRED"
        ):
            _attest_call(
                env,
                AUTHORITY_ROLE_PRIMARY,
            )

        assert len(
            gl.message_raw[
                "stack"
            ]
        ) == 1

        gl.message_raw[
            "stack"
        ] = []

    print(
        "R94_R13B_CASE_NONEMPTY_STACK_REJECT=PASS"
    )
