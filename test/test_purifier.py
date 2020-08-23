import unittest

from core.executors.files.reader import Reader
from core.executors.converters.purifier import Purifier, PureCodes


class PurifierTest(unittest.TestCase):
    def setUp(self):
        self.script = Reader.read("test.srt")

    def test_remove_carriage(self):
        message = "Simple line \n\r\r\n another simple line"
        pur = Purifier(PureCodes.CARRIAGE)

        self.assertEqual("Simple line \n\n another simple line",
                         pur.purify(message))
        self.assertNotIn("\r", pur.purify(self.script))

    def test_remove_time_codes(self):
        message = "1\n00:00:02,128 --> 00:00:04,839\nSimple line\n"
        pur = Purifier(PureCodes.TIME_CODES)

        self.assertEqual("Simple line\n", pur.purify(message))
        self.assertNotRegex(r"\d+[\n]\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}[\n]",
                            pur.purify(self.script))

    def test_remove_ad(self):
        pur = Purifier(PureCodes.ADS)
        self.assertNotRegex(r".\[German - SDH\].*OpenSubtitles.*", pur.purify(self.script))
        self.assertNotRegex("\nHier könnte deine Werbung stehen!\nKontaktiere noch heute www.OpenSubtitles.org\n",
                            pur.purify(self.script))

    def test_remove_script_remarks(self):
        message = "(NEW LINE)"
        pur = Purifier(PureCodes.REMARKS)

        self.assertEqual("new line.", pur.purify(message))
        self.assertNotRegex(r'\((.*[\n]?.*)\)', pur.purify(self.script))

    def test_remove_triple_dots(self):
        message = "New line...Probably new sentence"
        message_question = "Are you sure ...? Yes"
        pur = Purifier(PureCodes.TRIPLE_DOTS)

        self.assertEqual("New line.Probably new sentence", pur.purify(message))
        self.assertEqual("Are you sure ? Yes", pur.purify(message_question))
        self.assertNotIn("...", pur.purify(self.script))
        self.assertNotIn(".?", pur.purify(self.script))

    def test_remove_remove_tags(self):
        message = "</i>Wow gut who made this is really cool!<i>"
        pur = Purifier(PureCodes.TAGS)

        self.assertEqual("Wow gut who made this is really cool!", pur.purify(message))
        self.assertNotRegex(r"</?i>", pur.purify(self.script))

    def test_remove_names(self):
        message = "SOMEONE:\nSOMETHING\n\nPlan A:\nNAME: INFO"
        pur = Purifier(PureCodes.NAMES)

        self.assertEqual("SOMETHING\n\nPlan A:\nINFO", pur.purify(message))
        self.assertNotRegex(r"[A-Z]{2,}:[\s\n]", pur.purify(self.script))

    def test_remove_dialog_markers(self):
        message = "- Huh?\n- Huh!\n- Oh really? Are you sure you want a-b thing"
        pur = Purifier(PureCodes.DIALOG)

        self.assertEqual("Huh?\nHuh!\nOh really? Are you sure you want a-b thing", pur.purify(message))
        self.assertNotRegex(r"^- ", pur.purify(self.script))

    def test_remove_new_lines(self):
        message = "Huh?\nHuh!\nOh really? Are you sure\nyou want a-b thing."
        pur = Purifier(PureCodes.NEW_LINES)

        self.assertEqual("Huh? Huh! Oh really? Are you sure you want a-b thing.", pur.purify(message))
        self.assertNotRegex(r"[\n]", pur.purify(self.script))

    def test_new_line_per_sentence(self):
        message = "Huh? Huh! Oh really? Are you sure you want a-b thing."
        pur = Purifier(PureCodes.SPLIT)

        self.assertEqual("Huh?\n Huh!\n Oh really?\n Are you sure you want a-b thing.\n", pur.purify(message))
        #self.assertRegexpMatches("(\.[\n]|\?[\n]|)")


    def test_strip_lines(self):
        self.assertEqual(True, False)

    def test_full_script(self):
        # test on different artifacts, like .., .? etc..
        #self.assertNotIn("..", pur.purify(self.script))
        self.assertEqual(True, False)

    def test_full_message(self):
        # just testt equality of message and expected
        self.assertEqual(True, False)

if __name__ == '__main__':
    unittest.main()
