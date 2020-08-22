import unittest
from core.executors.files.decoder import Decoder
from core.data.enums import Files

class DecoderTest(unittest.TestCase):

    def test_decoding(self):
        data = "Random data"
        encoded = data.encode(Files.DEFAULT_ENCODING)
        decoder = Decoder(Files.DEFAULT_ENCODING)

        self.assertEqual(decoder.decode(encoded), data)


if __name__ == '__main__':
    unittest.main()
