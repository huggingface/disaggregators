import unittest
from disaggregators.disaggregation_modules.pronouns import Pronouns


class TestPronouns(unittest.TestCase):
    def test_initialize(self):
        disagg_module = Pronouns(column=None)
        self.assertEqual(disagg_module.name, "pronouns")

    def test_call_default_pronouns(self):
        data = {"text": "He went to the park."}
        disagg_module = Pronouns(column="text")
        results = disagg_module(data)
        self.assertEqual(results, {"he/him": True, "she/her": False, "they/them": False})


if __name__ == '__main__':
    unittest.main()
