import unittest
import time
import logging

from morton import Morton


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class TestMorton(unittest.TestCase):

    def test_packunpack(self):

        def do_test(dimensions, bits, cases):
            m = Morton(dimensions, bits)
            for values in cases:
                code = m.pack(*values)
                unpacked_values = m.unpack(code)
                assert unpacked_values == values

        do_test(
            dimensions=2, bits=32,
            cases=[
                [1, 2],
                [2, 1],
                [(1 << 32)-1, (1 << 32)-1],
            ])
        do_test(
            dimensions=3, bits=21,
            cases=[
                [1, 2, 4],
                [4, 2, 1],
                [(1 << 21)-1, (1 << 21)-1, (1 << 21)-1],
                [1, 1, 1],
            ])
        do_test(
            dimensions=2, bits=1,
            cases=[
                [1, 1],
                [0, 0],
            ])
        do_test(
            dimensions=4, bits=16,
            cases=[
                [1, 2, 4, 8],
                [8, 4, 2, 1],
                [(1 << 16)-1, (1 << 16)-1, (1 << 16)-1, (1 << 16)-1],
                [1, 1, 1, 1],
            ])
        do_test(
            dimensions=6, bits=10,
            cases=[
                [1, 2, 4, 8, 16, 32],
                [32, 16, 8, 4, 2, 1],
                [1023, 1023, 1023, 1023, 1023, 1023],
            ])
        do_test(
            dimensions=64, bits=1,
            cases=[
                [1]*64,
            ])
        do_test(
            dimensions=2, bits=64,
            cases=[
                [1, 2],
                [2, 1],
                [(1 << 64)-1, (1 << 64)-1],
            ])

    def test_benchmark(self):
        m = Morton()
        t = time.time()
        for _ in range(100000):
            m.pack(3, 6)
        logger.info("time for pack: {}".format(time.time() - t))
        t = time.time()
        code = m.pack(3, 6)
        for _ in range(100000):
            m.unpack(code)
        logger.info("time for unpack: {}".format(time.time() - t))
