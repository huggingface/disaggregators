import unittest

from disaggregators.disaggregation_modules.random import Random


class TestRandom(unittest.TestCase):
    def test_initialize(self):
        disagg_module = Random(column=None)
        self.assertEqual("random", disagg_module.name)

    @unittest.skip
    def test_call_default_pronouns(self):
        pass


if __name__ == "__main__":
    unittest.main()
