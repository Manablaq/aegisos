from __future__ import annotations

import hashlib
from pathlib import Path

import pytest


# P2A_R1F_R3_FRESH_CANONICAL_FIXTURE_V1
#
# Fresh certification of the Direct Mode helper-routing behavior.
# No historical byte-identity claim is made for this file.

ROOT = Path(__file__).resolve().parents[1]

CORE = (
    ROOT
    / "contracts"
    / "aegis_core.py"
)

HELPER = (
    ROOT
    / "contracts"
    / "aegis_digest_helper.py"
)

EXPECTED_CORE_SHA = (
    "df7f279e651681a24fdb3b0f71079ed"
    "b64ebdf45a0e5c398806804f07fb3d21b"
)

EXPECTED_HELPER_SHA = (
    "624129618401b57c8547e6b4c4b14528"
    "fbce154a9f8e00a621596221b7864d73"
)


def _sha(
    path: Path,
) -> str:
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def _address_bytes(
    value,
) -> bytes:
    if isinstance(
        value,
        bytes,
    ):
        result = value

    elif isinstance(
        value,
        bytearray,
    ):
        result = bytes(
            value
        )

    else:
        as_bytes = getattr(
            value,
            "as_bytes",
            None,
        )

        if callable(
            as_bytes
        ):
            result = bytes(
                as_bytes()
            )

        elif as_bytes is not None:
            result = bytes(
                as_bytes
            )

        else:
            as_hex = getattr(
                value,
                "as_hex",
                None,
            )

            if callable(
                as_hex
            ):
                as_hex = as_hex()

            if isinstance(
                as_hex,
                str,
            ):
                value = as_hex

            if isinstance(
                value,
                str,
            ):
                text = value

                if text.startswith(
                    "0x"
                ):
                    text = text[2:]

                result = bytes.fromhex(
                    text
                )

            else:
                result = bytes(
                    value
                )

    if len(result) != 20:
        raise AssertionError(
            "expected 20-byte address, "
            f"got {len(result)} bytes"
        )

    return result


class _LocalHelperView:
    def __init__(
        self,
        helper,
    ):
        self._helper = helper

    def view(self):
        return self

    def e(
        self,
        *args,
    ):
        return self._helper.e(
            *args
        )

    def g(
        self,
        *args,
    ):
        return self._helper.g(
            *args
        )


@pytest.fixture(
    autouse=True
)
def _r94_route_pure_helper(
    request,
    monkeypatch,
):
    module = request.module

    candidate = getattr(
        module,
        "CANDIDATE",
        None,
    )

    if candidate is None:
        yield
        return

    if (
        Path(
            candidate
        ).resolve()
        !=
        CORE.resolve()
    ):
        yield
        return

    assert (
        _sha(CORE)
        ==
        EXPECTED_CORE_SHA
    )

    assert (
        _sha(HELPER)
        ==
        EXPECTED_HELPER_SHA
    )

    original_deploy = (
        module.deploy_contract
    )

    def wrapped_deploy(
        contract_path,
        vm,
        *args,
        **kwargs,
    ):
        requested = Path(
            contract_path
        ).resolve()

        if (
            requested
            !=
            CORE.resolve()
        ):
            return original_deploy(
                contract_path,
                vm,
                *args,
                **kwargs,
            )

        from glsim.engine import SimEngine

        SimEngine._reset_contract_registry()

        helper = original_deploy(
            HELPER,
            vm,
            sdk_version=kwargs.get(
                "sdk_version"
            ),
        )

        helper_addr_bytes = (
            _address_bytes(
                vm._contract_address
            )
        )

        # Helper deployment initializes the pinned SDK paths.
        # This mirrors gltest.direct.loader itself.
        from genlayer.py.types import Address

        helper_address = Address(
            helper_addr_bytes
        )

        from genlayer import gl

        original_get_contract_at = (
            gl.get_contract_at
        )

        helper_view = (
            _LocalHelperView(
                helper
            )
        )

        def local_get_contract_at(
            address,
        ):
            try:
                target = (
                    _address_bytes(
                        address
                    )
                )

            except Exception:
                return (
                    original_get_contract_at(
                        address
                    )
                )

            if (
                target
                ==
                helper_addr_bytes
            ):
                return helper_view

            return (
                original_get_contract_at(
                    address
                )
            )

        monkeypatch.setattr(
            gl,
            "get_contract_at",
            local_get_contract_at,
        )

        SimEngine._reset_contract_registry()

        return original_deploy(
            CORE,
            vm,
            helper_address,
            *args,
            **kwargs,
        )

    monkeypatch.setattr(
        module,
        "deploy_contract",
        wrapped_deploy,
    )

    yield
