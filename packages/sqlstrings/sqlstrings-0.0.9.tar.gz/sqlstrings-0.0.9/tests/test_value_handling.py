import unittest
from sys import path

path.append("sqlstrings")

import value_handling as vh

class TestValueHandling(unittest.TestCase):

    # value writer tests

    def test_value_writer_float(self):
        self.assertEqual("12.05", vh.value_writer(12.05))
        self.assertEqual("0.0", vh.value_writer(0.0))
        self.assertEqual("-17.0512", vh.value_writer(-17.0512))

    def test_value_writer_int(self):
        self.assertEqual("12", vh.value_writer(12))
        self.assertEqual("0", vh.value_writer(0))
        self.assertEqual("-15", vh.value_writer(-15))

    def test_value_writer_string(self):
        self.assertEqual("\"Hello world\"", vh.value_writer("Hello world"))

    def test_value_writer_null(self):
        self.assertEqual("NULL", vh.value_writer("NULL"))
        self.assertEqual("NULL", vh.value_writer(None))

    # value reader tests

    def test_value_reader_float(self):
        self.assertEqual(12.05, vh.value_reader("12.05"))
        self.assertEqual(1.2098, vh.value_reader("1.2098"))
        self.assertEqual(0, vh.value_reader("0"))
        self.assertEqual(-25.6, vh.value_reader("-25.6"))

    def test_value_reader_int(self):
        self.assertEqual(-1, vh.value_reader("-1"))
        self.assertEqual(0, vh.value_reader("0"))
        self.assertEqual(16, vh.value_reader("16"))

    def test_value_reader_nulls(self):
        self.assertEqual(None, vh.value_reader("NULL"))
        self.assertEqual(None, vh.value_reader("NONE"))
        self.assertEqual(None, vh.value_reader("None"))


if __name__ == '__main__':
    unittest.main()
