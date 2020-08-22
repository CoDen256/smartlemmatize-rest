import unittest
import gzip
import os

from core.executors.files.unzipper import Gzipper


class GzipperTest(unittest.TestCase):

    def setUp(self):
        self.gzipper = Gzipper()
        self.dir = os.path.dirname(os.path.realpath(__file__))
        self.file = os.path.join(self.dir, "test.gz")
        open(self.file, "a").close()

    def test_wrong_data(self):
        self.assertRaises(TypeError, lambda: self.gzipper.unzip("wrongdata"))
        self.assertRaises(OSError, lambda: self.gzipper.unzip(b"wrongbytedata"))

    def test_unzipping_on_fly(self):
        message = b"Pretty good data\r\nReally good data"
        data = gzip.compress(message)
        self.assertEqual(self.gzipper.unzip(data), message)

    def test_unzipping_from_file(self):
        message = b"Pretty good data\r\nWould be bad if someone writes it to file"
        with gzip.open(self.file, mode="wb") as f:
            f.write(message)
        with open(self.file, mode="rb") as f:
            self.assertEqual(self.gzipper.unzip(f.read()), message)

    def tearDown(self):
        os.remove(self.file)


if __name__ == '__main__':
    unittest.main()
