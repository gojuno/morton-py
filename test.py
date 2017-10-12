import unittest
import time
import logging

from morton import _PyMorton
from morton import _Morton

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

FIXTURE_PACKUNPACK = [
    dict(
        dimensions=2, bits=32,
        cases=[
            [1, 2],
            [2, 1],
            [(1 << 32)-1, (1 << 32)-1],
    ]),
    dict(
        dimensions=3, bits=21,
        cases=[
            [1, 2, 4],
            [4, 2, 1],
            [(1 << 21)-1, (1 << 21)-1, (1 << 21)-1],
            [1, 1, 1],
    ]),
    dict(
        dimensions=2, bits=1,
        cases=[
            [1, 1],
            [0, 0],
    ]),
    dict(
        dimensions=4, bits=16,
        cases=[
            [1, 2, 4, 8],
            [8, 4, 2, 1],
            [(1 << 16)-1, (1 << 16)-1, (1 << 16)-1, (1 << 16)-1],
            [1, 1, 1, 1],
    ]),
    dict(
        dimensions=6, bits=10,
        cases=[
            [1, 2, 4, 8, 16, 32],
            [32, 16, 8, 4, 2, 1],
            [1023, 1023, 1023, 1023, 1023, 1023],
    ]),
    dict(
        dimensions=64, bits=1,
        cases=[
            [1]*64,
    ]),
    dict(
        dimensions=2, bits=64,
        cases=[
            [1, 2],
            [2, 1],
            [(1 << 64)-1, (1 << 64)-1],
    ])
]

FIXTURE_SPACKSUNPACK = [
    dict(
        dimensions=2, bits=32,
        cases=[
            [1, 2],
            [2, 1],
            [(1<<31)-1, (1<<31)-1],
            [1, 1],
            [-1, -2],
            [-2, -1],
            [-((1 << 31) - 1), -((1 << 31) - 1)],
            [-1, -1],
    ]),
    dict(
        dimensions=4, bits=16,
        cases=[
            [1, 2, 4, 8],
            [8, 4, 2, 1],
            [(1<<15)-1, (1<<15)-1, (1<<15)-1, (1<<15)-1],
            [-1, -2, -4, -8],
            [-8, -4, -2, -1],
            [-((1 << 15) - 1), -((1 << 15) - 1), -((1 << 15) - 1), -((1 << 15) - 1)],
    ])
]

class Test_PyMorton(unittest.TestCase):

    def test_packunpack(self):

        def do_test(dimensions, bits, cases):
            m = _PyMorton(dimensions, bits)
            for values in cases:
                code = m.pack(*values)
                unpacked_values = m.unpack(code)
                assert unpacked_values == values, (unpacked_values, values)

        for cases in FIXTURE_PACKUNPACK:
            do_test(**cases)

    def test_spacksunpack(self):

        def do_test(dimensions, bits, cases):
            m = _PyMorton(dimensions, bits)
            for values in cases:
                code = m.spack(*values)
                unpacked_values = m.sunpack(code)
                assert unpacked_values == values, (unpacked_values, values)

        for cases in FIXTURE_SPACKSUNPACK:
            do_test(**cases)

    def test_benchmark(self):
        m = _PyMorton()
        t = time.time()
        for _ in range(100000):
            m.pack(3, 6)
        logger.info("(native) time for pack: {}".format(time.time() - t))
        t = time.time()
        code = m.pack(3, 6)
        for _ in range(100000):
            m.unpack(code)
        logger.info("(native) time for unpack: {}".format(time.time() - t))


class Test_Morton(unittest.TestCase):

    def test_packunpack(self):

        def do_test(dimensions, bits, cases):
            m = _Morton(dimensions, bits)
            for values in cases:
                code = m.pack(*values)
                unpacked_values = m.unpack(code)
                assert unpacked_values == values, (unpacked_values, values)

        # except last for avoiding
        # `OverflowError: Python int too large to convert to C unsigned long`
        for cases in FIXTURE_PACKUNPACK[:-1]:
            do_test(**cases)

    # def test_spacksunpack(self):

    #     def do_test(dimensions, bits, cases):
    #         m = _Morton(dimensions, bits)
    #         for values in cases:
    #             code = m.spack(*values)
    #             unpacked_values = m.sunpack(code)
    #             assert unpacked_values == values, (unpacked_values, values)

    #     for cases in FIXTURE_SPACKSUNPACK[1:]:
    #         do_test(**cases)

    def test_benchmark(self):
        m = _Morton()
        t = time.time()
        for _ in range(100000):
            m.pack(3, 6)
        logger.info("time for pack: {}".format(time.time() - t))
        t = time.time()
        code = m.pack(3, 6)
        for _ in range(100000):
            m.unpack(code)
        logger.info("time for unpack: {}".format(time.time() - t))
