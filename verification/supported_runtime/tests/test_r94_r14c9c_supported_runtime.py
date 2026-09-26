from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import time
from typing import Any

from gltest import (
    create_accounts,
    get_contract_factory,
    get_gl_client,
)

from gltest.assertions import (
    tx_execution_failed,
    tx_execution_succeeded,
)

from gltest.types import (
    TransactionStatus,
)


from genlayer_py.types import CalldataAddress

ROOT = Path(
    os.environ[
        "AEGISOS_R94_R14C9C_ROOT"
    ]
)

EVIDENCE = (
    ROOT
    / "evidence"
)

CORE_PATH = (
    ROOT
    / "contracts"
    / "aegis_core.py"
)

HELPER_PATH = (
    ROOT
    / "contracts"
    / "aegis_digest_helper.py"
)

WITNESS_PATH = (
    ROOT
    / "contracts"
    / "aegis_stack_witness.py"
)

RELAY_PATH = (
    ROOT
    / "contracts"
    / "aegis_stack_relay.py"
)


EXPECTED_CORE_SHA = (
    "df7f279e651681a24fdb3b0f71079ed"
    "b64ebdf45a0e5c398806804f07fb3d21b"
)

EXPECTED_HELPER_SHA = (
    "624129618401b57c8547e6b4c4b14528"
    "fbce154a9f8e00a621596221b7864d73"
)


POLICY_TEXT = (
    "R94-R14C9A supported-runtime "
    "authority policy."
)

AUTHORITY_TEXT = (
    "R94-R14C9A bound primary and "
    "corroborating authorities."
)

PRIMARY_EVIDENCE = (
    "R94-R14C9A primary evidence."
)

PRIMARY_SOURCE = (
    "R94-R14C9A immutable primary source."
)

FOREIGN_EVIDENCE = (
    "R94-R14C9A foreign-sender evidence."
)

FOREIGN_SOURCE = (
    "R94-R14C9A immutable foreign source."
)


def h(
    value: str,
) -> str:
    return hashlib.sha256(
        value.encode(
            "utf-8"
        )
    ).hexdigest()


def file_sha(
    path: Path,
) -> str:
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def account_address(
    account: Any,
) -> str:
    value = getattr(
        account,
        "address",
        None,
    )

    if value is None:
        raise AssertionError(
            "ACCOUNT_ADDRESS_MISSING"
        )

    return str(
        value
    )


def save_json(
    name: str,
    value: Any,
) -> None:
    (
        EVIDENCE
        / name
    ).write_text(
        json.dumps(
            value,
            sort_keys=True,
            indent=2,
            default=str,
        )
        + "\n",
        encoding="utf-8",
    )


def normalized_address(
    value: Any,
) -> str:
    if hasattr(
        value,
        "as_hex",
    ):
        value = value.as_hex

    text = str(
        value
    ).strip()

    if text.startswith(
        "addr#"
    ):
        text = (
            "0x"
            + text[5:]
        )

    match = re.search(
        r"0x[0-9a-fA-F]{40}",
        text,
    )

    if match is None:
        raise AssertionError(
            "UNRECOGNIZED_ADDRESS_VALUE:"
            + text
        )

    return (
        match.group(0)
        .lower()
    )


def transact(
    contract: Any,
    method: str,
    args: list[Any],
    account: Any,
):
    connected = (
        contract.connect(
            account
        )
    )

    function = getattr(
        connected,
        method,
    )

    return function(
        args=args
    ).transact(
        consensus_max_rotations=3,
        wait_transaction_status=(
            TransactionStatus.ACCEPTED
        ),
        wait_interval=1000,
        wait_retries=120,
    )


def deploy(
    path: Path,
    account: Any,
    args: list[Any] | None = None,
):
    factory = (
        get_contract_factory(
            contract_file_path=path
        )
    )

    return factory.deploy(
        args=args,
        account=account,
        consensus_max_rotations=3,
        wait_transaction_status=(
            TransactionStatus.ACCEPTED
        ),
        wait_interval=1000,
        wait_retries=120,
    )


def leader_error_text(
    receipt: dict[str, Any],
) -> str:
    consensus = receipt.get(
        "consensus_data",
        {},
    )

    if not isinstance(
        consensus,
        dict,
    ):
        return ""

    leader = consensus.get(
        "leader_receipt",
        [],
    )

    if not isinstance(
        leader,
        list,
    ) or not leader:
        return ""

    first = leader[0]

    if not isinstance(
        first,
        dict,
    ):
        return ""

    genvm = first.get(
        "genvm_result",
        {},
    )

    if not isinstance(
        genvm,
        dict,
    ):
        return ""

    return "\n".join(
        str(
            genvm.get(
                key,
                "",
            )
        )
        for key in (
            "stdout",
            "stderr",
            "message",
        )
    )


def receipt_tx_id(
    receipt: dict[str, Any],
) -> str | None:
    for key in (
        "id",
        "tx_id",
        "transaction_id",
        "hash",
    ):
        value = receipt.get(
            key
        )

        if value:
            return str(
                value
            )

    return None


def decoded_transaction_error_evidence(client, tx_id):
    import base64

    transaction = client.get_transaction(
        tx_id
    )

    payloads = []

    def walk(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if (
                    key == "payload"
                    and isinstance(
                        child,
                        str,
                    )
                ):
                    payloads.append(
                        child
                    )

                if (
                    key == "result"
                    and isinstance(
                        child,
                        str,
                    )
                ):
                    try:
                        decoded = base64.b64decode(
                            child,
                            validate=True,
                        ).decode(
                            "utf-8",
                            errors="replace",
                        )
                    except Exception:
                        decoded = None

                    if decoded:
                        payloads.append(
                            decoded
                        )

                walk(child)

        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(transaction)

    normalized = sorted(
        {
            value.lstrip("\x01")
            for value in payloads
            if isinstance(
                value,
                str,
            )
        }
    )

    return {
        "tx_id":
            tx_id,

        "status_name":
            transaction.get(
                "status_name"
            ),

        "decoded_error_payloads":
            normalized,
    }


def test_r94_r14c9c_real_supported_runtime():
    assert (
        file_sha(
            CORE_PATH
        )
        == EXPECTED_CORE_SHA
    )

    assert (
        file_sha(
            HELPER_PATH
        )
        == EXPECTED_HELPER_SHA
    )

    print(
        "R94_R14C9C_CANDIDATE_SHA_GATE=PASS"
    )

    #
    # This call is deliberately INSIDE the test.
    # pytest_configure has already populated GeneralConfig.
    #
    client = get_gl_client()

    assert int(
        client.chain.id
    ) == 61999

    print(
        "R94_R14C9C_CONFIGURED_CLIENT_CHAIN_61999=PASS"
    )

    actors = create_accounts(
        5
    )

    assert len(
        actors
    ) == 5

    (
        creator,
        counterparty,
        primary,
        corroborator,
        intruder,
    ) = actors

    addresses = [
        account_address(
            actor
        )
        for actor in actors
    ]

    assert len(
        {
            value.lower()
            for value in addresses
        }
    ) == 5

    funding_receipts = []

    for actor in actors:
        address = account_address(
            actor
        )

        funding_tx_raw = client.fund_account(
            address,
            1000,
        )

        if not isinstance(
            funding_tx_raw,
            (
                bytes,
                bytearray,
            ),
        ):
            raise AssertionError(
                "FUNDING_TX_NOT_BYTES_LIKE:"
                + repr(
                    funding_tx_raw
                )
            )

        funding_tx = (
            "0x"
            + bytes(
                funding_tx_raw
            ).hex()
        )

        assert re.fullmatch(
            r"0x[0-9a-f]{64}",
            funding_tx,
        )

        funding_receipt = client.wait_for_transaction_receipt(
            transaction_hash=funding_tx,
            status=TransactionStatus.ACCEPTED,
            interval=1000,
            retries=120,
        )

        funding_receipts.append(
            funding_receipt
        )

        balance_response = client.provider.make_request(
            method="eth_getBalance",
            params=[
                address,
            ],
        )

        balance = balance_response.get(
            "result"
        )

        if isinstance(
            balance,
            str,
        ):
            balance_value = int(
                balance,
                0,
            )
        else:
            balance_value = int(
                balance
            )

        assert balance_value == 1000

    save_json(
        "funding-receipts.json",
        funding_receipts,
    )

    print(
        "R94_R14C9C_ISOLATED_ACTORS_FUNDED=PASS"
    )

    helper = deploy(
        HELPER_PATH,
        creator,
    )

    print(
        "R94_R14C9C_HELPER_DEPLOY=PASS"
    )

    core = deploy(
        CORE_PATH,
        creator,
        args=[
            CalldataAddress(
                helper.address
            ),
        ],
    )

    print(
        "R94_R14C9C_R13B_CORE_DEPLOY=PASS"
    )

    agreement_id = (
        "r94-r14c9a-supported-runtime"
    )

    now = int(
        time.time()
    )

    recovery_deadline = (
        now
        + 86400
    )

    create_receipt = transact(
        core,
        "create_probe",
        [
            agreement_id,
            account_address(
                counterparty
            ),
            h(
                POLICY_TEXT
            ),
            h(
                AUTHORITY_TEXT
            ),
            account_address(
                primary
            ),
            account_address(
                corroborator
            ),
            1000,
            60,
            3600,
            recovery_deadline,
        ],
        creator,
    )

    save_json(
        "candidate-create-receipt.json",
        create_receipt,
    )

    assert tx_execution_succeeded(
        create_receipt
    )

    print(
        "R94_R14C9C_CORE_CREATE=PASS"
    )

    accept_receipt = transact(
        core,
        "accept_probe",
        [
            agreement_id,
        ],
        counterparty,
    )

    save_json(
        "candidate-accept-receipt.json",
        accept_receipt,
    )

    assert tx_execution_succeeded(
        accept_receipt
    )

    print(
        "R94_R14C9C_CORE_ACCEPT=PASS"
    )

    probe = (
        core.get_probe(
            args=[
                agreement_id,
            ]
        ).call()
    )

    assert isinstance(
        probe,
        dict,
    )

    assert (
        probe.get(
            "accepted"
        )
        is True
    )

    assert int(
        probe.get(
            "state",
            -1,
        )
    ) == 2

    print(
        "R94_R14C9C_ACCEPTED_STATE=PASS"
    )

    attest_now = int(
        time.time()
    )

    primary_receipt = transact(
        core,
        "attest_evidence_probe",
        [
            agreement_id,
            1,
            (
                agreement_id
                + "-primary-record"
            ),
            "v1",
            (
                "urn:aegisos:r94:"
                "r14c9a:primary:v1"
            ),
            h(
                PRIMARY_EVIDENCE
            ),
            h(
                PRIMARY_SOURCE
            ),
            attest_now - 5,
            attest_now + 7200,
            1,
        ],
        primary,
    )

    save_json(
        "candidate-primary-attestation-receipt.json",
        primary_receipt,
    )

    assert tx_execution_succeeded(
        primary_receipt
    )

    print(
        "R94_R14C9C_DIRECT_PRIMARY_ATTESTATION=PASS"
    )

    primary_record = (
        core.get_attestation(
            args=[
                agreement_id,
                1,
            ]
        ).call()
    )

    assert isinstance(
        primary_record,
        dict,
    )

    assert (
        primary_record.get(
            "present"
        )
        is True
    )

    assert int(
        primary_record.get(
            "generation",
            -1,
        )
    ) == 1

    assert (
        primary_record.get(
            "evidence_record_id"
        )
        == (
            agreement_id
            + "-primary-record"
        )
    )

    assert (
        normalized_address(
            primary_record.get(
                "authority"
            )
        )
        == account_address(
            primary
        ).lower()
    )

    print(
        "R94_R14C9C_PRIMARY_ATTESTATION_STATE=PASS"
    )

    foreign_now = int(
        time.time()
    )

    foreign_receipt = transact(
        core,
        "attest_evidence_probe",
        [
            agreement_id,
            2,
            (
                agreement_id
                + "-foreign-record"
            ),
            "v1",
            (
                "urn:aegisos:r94:"
                "r14c9a:foreign:v1"
            ),
            h(
                FOREIGN_EVIDENCE
            ),
            h(
                FOREIGN_SOURCE
            ),
            foreign_now - 5,
            foreign_now + 7200,
            1,
        ],
        intruder,
    )

    save_json(
        "candidate-foreign-sender-receipt.json",
        foreign_receipt,
    )

    assert tx_execution_failed(
        foreign_receipt
    )

    error_material = (
        leader_error_text(
            foreign_receipt
        )
    )

    if (
        "BOUND_AUTHORITY_ONLY"
        not in error_material
    ):
        tx_id = receipt_tx_id(
            foreign_receipt
        )

        if tx_id is not None:
            trace = (
                decoded_transaction_error_evidence(client,
                    tx_id
                )
            )

            save_json(
                "candidate-foreign-sender-debug-trace.json",
                trace,
            )

            error_material += (
                "\n"
                + json.dumps(
                    trace,
                    sort_keys=True,
                    default=str,
                )
            )

    assert (
        "BOUND_AUTHORITY_ONLY"
        in error_material
    )

    print(
        "R94_R14C9C_FOREIGN_SENDER_REJECTION=PASS"
    )

    witness = deploy(
        WITNESS_PATH,
        creator,
    )

    relay = deploy(
        RELAY_PATH,
        creator,
    )

    print(
        "R94_R14C9C_STACK_WITNESS_DEPLOY=PASS"
    )

    print(
        "R94_R14C9C_STACK_RELAY_DEPLOY=PASS"
    )

    direct_depth = (
        witness.stack_depth().call()
    )

    direct_depth = int(
        direct_depth
    )

    print(
        "R94_R14C9C_DIRECT_STACK_DEPTH="
        + str(
            direct_depth
        )
    )

    assert (
        direct_depth
        == 0
    )

    nested_depth = (
        relay.nested_stack_depth(
            args=[
                witness.address,
            ]
        ).call()
    )

    nested_depth = int(
        nested_depth
    )

    print(
        "R94_R14C9C_NESTED_STACK_DEPTH="
        + str(
            nested_depth
        )
    )

    assert (
        nested_depth
        > 0
    )

    print(
        "R94_R14C9C_REAL_CALLCONTRACT_STACK_SEMANTICS=PASS"
    )

    source = CORE_PATH.read_text(
        encoding="utf-8"
    )

    exact_guard = (
        'self._x('
        'len(gl.message_raw["stack"]) != 0, '
        "'DIRECT_AUTHORITY_TRANSACTION_REQUIRED'"
        ')'
    )

    assert source.count(
        exact_guard
    ) == 1

    assert direct_depth == 0
    assert nested_depth != 0

    summary = {
        "schema":
            "AEGISOS_R94_R14C9C_RUNTIME_PROOF_V1",

        "candidate_core_sha256":
            EXPECTED_CORE_SHA,

        "helper_sha256":
            EXPECTED_HELPER_SHA,

        "localnet_chain_id":
            61999,

        "direct_primary_authority_attestation":
            "SUCCESS",

        "foreign_sender":
            "REJECTED_BOUND_AUTHORITY_ONLY",

        "top_level_stack_depth":
            direct_depth,

        "nested_callcontract_stack_depth":
            nested_depth,

        "candidate_exact_stack_guard_bound":
            True,

        "leader_only":
            False,
    }

    save_json(
        "runtime-proof-summary.json",
        summary,
    )

    print(
        "R94_R14C9C_CANDIDATE_STACK_GUARD_RUNTIME_BINDING=PASS"
    )

    print(
        "R94_R14C9C_SUPPORTED_RUNTIME_PROOF=PASS"
    )
