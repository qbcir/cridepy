import six

from ._cext import ffi, lib


class RideError(Exception):
    pass


class Compiler(object):
    def __init__(self):
        self._compiler = ffi.new("ride_compiler*")
        if lib.ride_init_compiler(self._compiler) != 0:
            raise RideError("Can't init compiler")
        self._compiler = ffi.gc(self._compiler, lib.ride_destroy_compiler)

    def compile(self, code):
        res = ffi.new("ride_compile_result_t*")
        res = ffi.gc(res, lib.ride_destroy_compile_result)
        if isinstance(code, six.string_types):
            code = code.encode()
        if lib.ride_compile(self._compiler, code, res) != 0:
            raise RideError("Fatal error while compiling code")
        if res.error != ffi.NULL:
            raise RideError(ffi.string(res.error).decode())
        return {
            'base64': ffi.string(res.base64).decode(),
            'complexity': int(res.complexity)
        }


_default_compiler = Compiler()


def compile(code):
    return _default_compiler.compile(code)
