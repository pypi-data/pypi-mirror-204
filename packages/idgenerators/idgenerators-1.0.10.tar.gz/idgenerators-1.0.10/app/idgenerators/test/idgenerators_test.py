import unittest

from ..src import (
    generate_Id
)

class GeneratorTest(unittest.TestCase):
    def test_generate_Id(self) -> None:
        id = generate_Id(length=5)
        print("Hi")
        self.assertTrue(len(id) == 5)