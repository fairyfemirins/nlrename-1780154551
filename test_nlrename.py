#!/usr/bin/env python3
"""
Test cases for nlrename.py
"""

import os
import tempfile
import unittest
from datetime import datetime
from unittest.mock import patch

from nlrename import parse_expression, rename_file


class TestNLrename(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = os.path.join(self.temp_dir.name, "test.txt")
        with open(self.test_file, "w") as f:
            f.write("test")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_parse_expression_date(self):
        func = parse_expression("today's date + original name")
        self.assertEqual(func("test.txt"), f"{datetime.now().strftime('%Y-%m-%d')}_test.txt")

    def test_parse_expression_regex(self):
        func = parse_expression("s/txt/log/")
        self.assertEqual(func("test.txt"), "test.log")

    def test_parse_expression_lowercase(self):
        func = parse_expression("lowercase all")
        self.assertEqual(func("TEST.TXT"), "test.txt")

    def test_parse_expression_uppercase(self):
        func = parse_expression("uppercase all")
        self.assertEqual(func("test.txt"), "TEST.TXT")

    def test_rename_file_dry_run(self):
        new_path = rename_file(self.test_file, "new.txt", dry_run=True)
        self.assertIsNotNone(new_path)
        if new_path:
            self.assertTrue(new_path.endswith("new.txt"))
        self.assertTrue(os.path.exists(self.test_file))
        self.assertFalse(os.path.exists(new_path) if new_path else True)

    def test_rename_file_actual(self):
        new_path = rename_file(self.test_file, "new.txt")
        self.assertIsNotNone(new_path)
        if new_path:
            self.assertTrue(os.path.exists(new_path))
            self.assertFalse(os.path.exists(self.test_file))


if __name__ == "__main__":
    unittest.main()