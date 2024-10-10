cimport cython
from libc.string cimport memcpy
from libc.stdlib cimport malloc 

ctypedef (unsigned long long) U64

cdef U64[2] a = [0, 0]
cdef class test:
    cdef U64[2] b
    def __cinit__(self):
        self.set(a)   

    cdef void set(self, U64[2] param1):
        memcpy(self.b, param1, 16)

    cpdef pri(self):
        print(self.b[0])
        print(self.b[1])

c = test()
c.pri()