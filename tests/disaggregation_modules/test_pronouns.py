import unittest

from disaggregators.disaggregation_modules.pronouns import Pronouns, PronounsLabels


class TestPronouns(unittest.TestCase):
    def test_initialize(self):
        disagg_module = Pronouns(column=None)
        self.assertEqual("pronouns", disagg_module.name)

    def test_call_default_pronouns(self):
        data = {"text": "He went to the park."}
        disagg_module = Pronouns(column="text")
        results = disagg_module(data)
        self.assertEqual(
            {PronounsLabels.HE_HIM: True, PronounsLabels.SHE_HER: False, PronounsLabels.THEY_THEM: False}, results
        )

    def test_get_labels_default(self):
        disagg_module = Pronouns(column="text")
        disagg_set = disagg_module.get_labels()
        self.assertEqual({PronounsLabels.HE_HIM, PronounsLabels.SHE_HER, PronounsLabels.THEY_THEM}, disagg_set)


if __name__ == "__main__":
    unittest.main()
