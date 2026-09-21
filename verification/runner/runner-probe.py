# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *


class RunnerProbe(gl.Contract):
    value: u32

    def __init__(self):
        self.value = u32(0)

    @gl.public.write
    def set_value(self, value: u32):
        self.value = value

    @gl.public.view
    def get_value(self) -> int:
        return int(self.value)
