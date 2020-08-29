import unittest
import os

from core.executors.files.reader import Reader
from core.executors.files.writer import Writer
from core.data.enums import Files


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.dir = os.path.dirname(os.path.realpath(__file__))

    def test_read_write_raw(self):
        messages = ["\r\r\n\nlovely message\n\n\r\r", "what could go wrong äüöß?", "huh'ä?"]

        for message in messages:
            file = self.file_path("byte")
            self.read_write_raw(message, file)

            self.remove(file)

    def test_read_write_byte(self):
        messages = ["\r\r\n\nlovely message\n\n\r\r", "what could go wrong äüöß?", "huh'ä?"]

        for message in messages:
            file = self.file_path("byte")
            self.read_write_byte(bytes(message, encoding=Files.DEFAULT_ENCODING), file)

            self.remove(file)

    def read_write_raw(self, message, file):
        return_value = Writer.write(file, message, Files.RAW)
        read_value = Reader.read_raw(file)

        self.assertEqual(return_value, message)
        self.assertEqual(read_value, message)

    def read_write_byte(self, message, file):
        return_value = Writer.write(file, message, Files.BYTE)
        read_value = Reader.read_byte(file)

        self.assertEqual(return_value, message)
        self.assertEqual(read_value, message)

    def remove(self, *filenames):
        for f in filenames:
            os.remove(f)

    def file_path(self, name):
        return os.path.join(self.dir, name)


if __name__ == '__main__':
    unittest.main()
