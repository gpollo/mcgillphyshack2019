from unittest import TestCase, main
from plot import LineMapper

class TestLineMapper(TestCase):
    def test_get_closests(self):
        series = [
            ([ 1, 2, 3], [7,8,9]),
            ([10,12,13], [6,7,8]),
            ([ 8, 9,10], [4,5,6]),
        ]
        mapper = LineMapper(series)

        result = mapper.get_closests(8.3, 2.4)
        self.assertEqual(len(result), 1)
        self.assertTupleEqual(result[0], (2, 0, 8, 4))

        result = mapper.get_closests(8.7, 2.4)
        self.assertEqual(len(result), 1)
        self.assertTupleEqual(result[0], (2, 0, 8, 4))

        result = mapper.get_closests(10.2, 5.5)
        self.assertEqual(len(result), 2)
        self.assertTupleEqual(result[0], (1, 0, 10, 6))
        self.assertTupleEqual(result[1], (2, 2, 10, 6))

        result = mapper.get_closests(10.2, 5.5, radius=0.001)
        self.assertEqual(result, None)

if __name__ == '__main__':
    main()
