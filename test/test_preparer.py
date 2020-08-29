import unittest
import unittest

from core.executors.converters.preparer import Preparer


class preparerTest(unittest.TestCase):
    def test_splitting_no_longer_then_specified(self):
        lines_to_split = ["sup", "lines", "this one", "is ", "really big",
                          "yeees", "noooo", "oh yeah", "oh noo"]

        preparer = Preparer(10)
        splited = preparer.split_and_prepare(lines_to_split)

        self.assertTrue(all([len(chunk) <= 10 for chunk in splited]))

    def test_splited_correct(self):
        lines_to_split = ["like", "hell", "oops", "its", "Me", "my", "Fried"]

        preparer = Preparer(5)
        self.assertEqual(["like", "hell", "oops", "itsMe", "my", "Fried"],
                         preparer.split_and_prepare(lines_to_split))

    def test_consistency(self):
        lines_to_split = ["ab", "bc", "de", "fghijk"]

        preparer = Preparer(6)

        self.assertEqual("".join(lines_to_split),
                         "".join(preparer.split_and_prepare(lines_to_split)))

    def test_splitting_too_long_line(self):
        lines_to_split = ["alpha", "really, really long line"]

        preparer = Preparer(23)

        self.assertRaises(Preparer.LineLengthExceededException,
                          lambda: preparer.split_and_prepare(lines_to_split))

    def test_splitting_no_lines(self):
        lines_to_split = []

        preparer = Preparer(5)

        self.assertRaises(Preparer.NothingToSplitException,
                          lambda: preparer.split_and_prepare(lines_to_split))

    def test_decapitalization(self):
        lines_to_split = ["Something WRONG", "I can feel", "IT", "ONEHUNDRED ASF", "Es ", "Der Percent"]

        preparer = Preparer(15, decapitalize=True)

        self.assertEqual(["something WRONG", "i can feelit", "onehundred ASF", "esder Percent"],
                         preparer.split_and_prepare(lines_to_split))

    def test_stripping(self):
        lines_to_split = ["hello ", " too much of ", " whitespaces \n"]

        preparer = Preparer(13, decapitalize=True)

        self.assertEqual(["hello", "too much of", "whitespaces"],
                         preparer.split_and_prepare(lines_to_split))

    def test_no_limit(self):
        self.assertRaises(ValueError, lambda: Preparer(0))
        self.assertRaises(ValueError, lambda: Preparer(None))
        self.assertRaises(ValueError, lambda: Preparer(-1))

    def test_one_char_lines(self):
        self.assertEqual([], Preparer(5).split_and_prepare(["a", "b", "", "c", "d"]))

if __name__ == '__main__':
    unittest.main()