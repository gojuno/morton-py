from libcpp.vector cimport vector
from libc.stdint cimport uint64_t


def flp2(x):
    '''Greatest power of 2 less than or equal to x, branch-free.'''
    x |= x >> 1
    x |= x >> 2
    x |= x >> 4
    x |= x >> 8
    x |= x >> 16
    x |= x >> 32
    x -= x >> 1
    return x


cdef class _Morton(object):

    cdef uint64_t dimensions
    cdef uint64_t bits
    cdef vector[uint64_t] _lshifts
    cdef vector[uint64_t] _rshifts
    cdef vector[uint64_t] _masks

    def __init__(self, dimensions=2, bits=32):
        assert dimensions > 0, 'dimensions should be greater than zero'
        assert bits > 0, 'bits should be greater than zero'

        shift = flp2(dimensions * (bits - 1))

        cdef uint64_t mask = 0
        cdef uint64_t shifted = 0

        self._lshifts.push_back(0)
        self._masks.push_back((1 << bits) - 1)

        max_value = (1 << (shift * bits)) - 1
        while shift > 0:
            mask = 0
            shifted = 0
            for bit in range(bits):
                distance = (dimensions * bit) - bit
                shifted |= shift & distance
                mask |= 1 << bit << (((shift - 1) ^ max_value) & distance)

            if shifted != 0:
                self._masks.push_back(mask)
                self._lshifts.push_back(shift)

            shift >>= 1

        self.dimensions = dimensions
        self.bits = bits
        # self._rshifts = self._lshifts[1:] + [0]
        for i in range(self._lshifts.size()-1):
            self._rshifts.push_back(self._lshifts[i+1])
        self._rshifts.push_back(0)

    def __repr__(self):
        return '<Morton dimensions={}, bits={}>'.format(
            self.dimensions, self.bits)

    def split(self, value):
        # type: (int) -> int
        masks = self._masks
        lshifts = self._lshifts
        for o in range(masks.size()):
            value = (value | (value << lshifts[o])) & masks[o]
        return value

    def compact(self, code):
        # type: (int) -> int
        masks = self._masks
        rshifts = self._rshifts

        for o in range(masks.size()-1, -1, -1):
            code = (code | (code >> rshifts[o])) & masks[o]
        return code

    # def shift_sign(self, value):
    #     # type: (int) -> int
    #     assert not(
    #         value >= (<uint64_t>1 << (self.bits - 1)) or
    #         value <= -(<uint64_t>1 << (self.bits - 1))), (value, self.bits)

    #     if value < 0:
    #         value = -value
    #         value |= <uint64_t>1 << (self.bits - 1)
    #     return value

    # def unshift_sign(self, value):
    #     # type: (int) -> int
    #     cdef uint64_t sign = 0
    #     sign = value & (<uint64_t>1 << (self.bits - 1))
    #     value &= (<uint64_t>1 << (self.bits - 1)) - 1
    #     if sign != 0:
    #         value = -value
    #     return value

    def pack(self, *args):
        # type: (List[int]) -> int
        assert isinstance(args, (list,tuple))
        assert len(args) <= self.dimensions
        assert all([v < (<uint64_t> 1 << self.bits) for v in args])

        cdef uint64_t code = 0
        for i in range(self.dimensions):
            code |= self.split(args[i]) << i
        return code

    def unpack(self, code):
        # type: (int) -> List[int]
        values = []
        for i in range(self.dimensions):
            values.append(self.compact(code >> i))
        return values

    # def spack(self, *args):
    #     # type: (List[int]) -> int
    #     return self.pack(*map(self.shift_sign, args))

    # def sunpack(self, code):
    #     # type: (int) -> List[int]
    #     values = self.unpack(code)
    #     return list(map(self.unshift_sign, values))

    def __cmp__(self, other):
        return (
            self.dimensions == other.dimensions and
            self.bits == other.bits
        )
