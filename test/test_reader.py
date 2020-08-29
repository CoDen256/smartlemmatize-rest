import unittest
import os

from core.executors.files.reader import Reader
from core.data.enums import Files


class ReaderTest(unittest.TestCase):

    def setUp(self):
        self.dir = os.path.dirname(os.path.realpath(__file__))

    def test_read_custom(self):
        message = "lovely message äüöß?\n"

        file = self.create_and_write(message, mode="w", encoding=Files.DEFAULT_ENCODING)

        self.assertEqual(Reader.read(file, mode="r", encoding=Files.DEFAULT_ENCODING), message)

        self.remove(file)

    def test_read_text(self):
        message = "lovely message äüöß?\n\r"

        file = self.create_and_write(message, mode="w", encoding=Files.DEFAULT_ENCODING, newline='')

        self.assertEqual(Reader.read_raw(file), message)

        self.remove(file)

    def test_read_binary(self):
        message = bytes("lovely message äüöß?\n\r", encoding=Files.DEFAULT_ENCODING)

        file = self.create_and_write(message, mode="wb")

        self.assertEqual(Reader.read_byte(file), message)

        self.remove(file)

    def create_and_write(self, message, **kwargs):
        filename = self.file_path("test_file")
        with open(filename, **kwargs) as f:
            f.write(message)
        return filename

    def remove(self, *filenames):
        for f in filenames:
            os.remove(f)

    def file_path(self, name):
        return os.path.join(self.dir, name)

if __name__ == '__main__':
    unittest.main()
