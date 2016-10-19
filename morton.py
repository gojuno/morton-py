
class Morton(object):

    def __init__(self, dimensions=2, bits=32):
        assert dimensions > 0, 'dimensions should be greater than zero'
        assert bits > 0, 'bits should be greater than zero'

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

        shift = flp2(dimensions * (bits - 1))

        masks = []
        lshifts = []
        max_value = (1 << (shift*bits))-1
        while shift > 0:
            mask = 0
            shifted = 0
            for bit in range(bits):
                distance = (dimensions * bit) - bit
                shifted |= shift & distance
                mask |= 1 << bit << (((shift - 1) ^ max_value) & distance)

            if shifted != 0:
                masks.append(mask)
                lshifts.append(shift)

            shift >>= 1

        self.dimensions = dimensions
        self.bits = bits
        self.lshifts = [0] + lshifts
        self.rshifts = lshifts + [0]
        self.masks = [(1 << bits) - 1] + masks

    def __repr__(self):
        return '<Morton dimensions={}, bits={}>'.format(
            self.dimensions, self.bits)

    def split(self, value):
        masks = self.masks
        lshifts = self.lshifts
        for o in range(len(masks)):
            value = (value | (value << lshifts[o])) & masks[o]
        return value

    def compact(self, code):
        masks = self.masks
        rshifts = self.rshifts
        for o in range(len(masks)-1, -1, -1):
            code = (code | (code >> rshifts[o])) & masks[o]
        return code

    def pack(self, *args):
        assert len(args) <= self.dimensions
        assert all([v < (1 << self.bits) for v in args])

        code = 0
        for i in range(self.dimensions):
            code |= self.split(args[i]) << i
        return code

    def unpack(self, code):
        values = []
        for i in range(self.dimensions):
            values.append(self.compact(code >> i))
        return values
