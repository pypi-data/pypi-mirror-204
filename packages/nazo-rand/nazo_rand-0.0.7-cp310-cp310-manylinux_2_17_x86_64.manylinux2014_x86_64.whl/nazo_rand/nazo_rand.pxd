# cython: language_level=3
# distutils: language = c++
from libc.stdint cimport int64_t
#cpdef void seed(int rseed = ?)
cpdef void shuffle(list array)
cpdef int random_integer_noargs()
cpdef object random_choice(object container)
cpdef list[object] random_choices(object container, Py_ssize_t count)
cpdef list[object] random_sample(object container, Py_ssize_t count)
# def int randbelow(int a)
# def int randint(int a,int b)
cdef int64_t cy_random_below(int64_t number) nogil
cdef int64_t cy_uniform_int_variate(int64_t a, int64_t b) nogil
cpdef int randrange(int start,int stop=?,int step=?)
cpdef double random_double(double a, double b)
cpdef double random_double_noargs()