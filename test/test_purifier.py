import unittest
import time

from core.executors.files.reader import Reader
from core.executors.files.writer import Writer
from core.executors.converters.purifier import Purifier, PureCodes, Constants


class PurifierTest(unittest.TestCase):
    def setUp(self):
        self.script = Reader.read_raw("input.srt")

    def test_remove_ad(self):
        pur = Purifier(PureCodes.ADS)
        self.assertNotIn(r"[German - SDH]", pur.apply(self.script))
        self.assertNotIn("Hier könnte deine Werbung stehen!",
                         pur.apply(self.script))
        self.assertNotIn("Kontaktiere noch heute www.OpenSubtitles.org",
                         pur.apply(self.script))

    def test_remove_script_remarks(self):
        pur = Purifier(PureCodes.REMARKS)
        self.assertNotRegex(pur.apply(self.script), r'\((.*[\n]?.*)\)')

    def test_remove_triple_dots(self):
        pur = Purifier(PureCodes.TRIPLE_DOTS)
        pure = pur.apply(self.script)

        self.assertNotIn("...", pure)
        self.assertNotIn(".?", pure)

    def test_remove_remove_tags(self):
        pur = Purifier(PureCodes.TAGS)
        self.assertNotRegex(pur.apply(self.script), r"</?i>")

    def test_remove_names(self):
        pur = Purifier(PureCodes.NAMES)
        self.assertNotRegex(pur.apply(self.script), r"[A-Z]+:[\s\n]")

    def test_remove_dialog_markers(self):
        pur = Purifier(PureCodes.ADS | PureCodes.DIALOG)
        self.assertNotRegex(pur.apply(self.script), r"\-[\w\s]")

    def test_remove_abbreviations(self):
        pur = Purifier(PureCodes.ABBREVIATIONS)
        for abb in Constants.ABBREVIATIONS:
            self.assertNotIn(abb, pur.apply(self.script))

    def test_parse(self):
        pur = Purifier(PureCodes.DEFAULT | PureCodes.PARSE)

        parsed = pur.apply(self.script)
        self.define_only_for_specified_script()
        self.assertEqual(len(parsed), 1539)

    def test_splitted(self):
        pur = Purifier(PureCodes.DEFAULT | PureCodes.SPLIT_PARSED)
        self.define_only_for_specified_script()
        expected_first_three = [
            "Wenn ein Elektron auf eine Platte mit 2 Spalten geschossen wird, und jeder Spalt beobachtet wird, geht es nicht durch beide hindurch.",
            "Unbeobachtet jedoch schon.",
            "Das heißt, wenn das Elektron vor Auftreffen auf der Platte beobachtet wird, geht es nur durch eine der Spalten."
        ]
        self.assertNotIn("\"", pur.apply(self.script))
        self.assertEqual(expected_first_three, pur.apply(self.script)[:3])

        Writer.write_raw("out", pur.apply(self.script), True)

    # @unittest.skip("Only for measuring")
    def test_measure(self):
        self.define_only_for_specified_script()
        measured = []
        for i in range(5):
            before = time.time()
            Purifier(PureCodes.ALL).apply(self.script)
            after = time.time()

            measured.append(after-before)

        aver = sum(measured)/len(measured)
        print("AVERAGE EXECUTION TIME:", aver)
        self.assertLessEqual(aver, 0.25)

    def define_only_for_specified_script(self):
        self.assertEqual(129607, len(self.script),
                         msg="Test works is defined for .srt combined of 4 first episodes of BBT. The len of test script:")

if __name__ == '__main__':
    unittest.main()
