# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *


class AegisStackWitness(gl.Contract):

    def __init__(self):
        pass

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def stack_depth(self) -> int:
        return len(gl.message_raw["stack"])
