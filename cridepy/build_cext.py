from cffi import FFI


ffi = FFI()

ffi.cdef("""

typedef struct ride_compiler_s {
    void* _ctx;
} ride_compiler;

typedef struct ride_compile_result_s {
    char* error;
    char* base64;
    int complexity;
} ride_compile_result_t;

int ride_init_compiler(ride_compiler* compiler);
int ride_compile(ride_compiler* compiler, const char* code, ride_compile_result_t* result);
int ride_destroy_compiler(ride_compiler* compiler);
void ride_destroy_compile_result(ride_compile_result_t* result);

""")

ffi.set_source("cridepy._cext",
"""
     #include "ride_c/ride.h"
""",
     libraries=['ride_c', 'mozjs-52'], library_dirs=['/usr/local/lib/ride_c'])


if __name__ == "__main__":
    ffi.compile(verbose=True)
