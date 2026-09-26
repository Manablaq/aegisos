# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

import typing

from genlayer import *


class AegisStackRelay(gl.Contract):

    def __init__(self):
        pass

    def _target(
        self,
        target: Address,
    ) -> typing.Any:
        return gl.get_contract_at(
            target
        ).view()  # pyright: ignore[reportUnknownMemberType,reportUnknownVariableType]

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def nested_stack_depth(
        self,
        target: str,
    ) -> int:
        return int(
            self._target(
                Address(
                    target
                )
            ).stack_depth()
        )
