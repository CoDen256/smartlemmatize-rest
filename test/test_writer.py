import unittest
import os
import pprint

from core.executors.files.writer import Writer
from core.data.enums import Files


class WriterTest(unittest.TestCase):

    def setUp(self):
        self.dir = os.path.dirname(os.path.realpath(__file__))

    def test_write_raw(self):
        message = "\r\nSuch a lovely message äüöß?\r\n"
        file1 = self.file_path("file1")
        file2 = self.file_path("file2")
        file3 = self.file_path("file3")

        ret1 = Writer.write(file1, message, Files.RAW)
        ret2 = Writer.write(file2, message)
        ret3 = Writer.write_raw(file3, message, False)

        infile4 = self.read_default(file1, mode="r", encoding=Files.DEFAULT_ENCODING, newline='')
        infile5 = self.read_default(file2, mode="r", encoding=Files.DEFAULT_ENCODING, newline='')
        infile6 = self.read_default(file3, mode="r", encoding=Files.DEFAULT_ENCODING, newline='')

        self.assertEqual(ret1, message)
        self.assertEqual(ret2, message)
        self.assertEqual(ret3, message)
        self.assertEqual(infile4, message)
        self.assertEqual(infile5, message)
        self.assertEqual(infile6, message)

        self.remove(file1, file2, file3)

    def test_write_raw_array(self):
        # ARRAY #
        array = [1, 2, 3]
        str_array = str(array)
        file_array = self.file_path("file_array")

        ret1 = Writer.write_raw(file_array, [1, 2, 3], pretty=False)
        infile1 = self.read_default(file_array, mode="r", encoding=Files.DEFAULT_ENCODING, newline='')

        self.assertEqual(ret1, array)
        self.assertEqual(infile1, str_array)

        self.remove(file_array)

    def test_write_raw_dict(self):
        # DICT #
        dic = {1: 3, 4: 5, 6: 7}
        str_dic = str(dic)
        file_dic = self.file_path("file_dic")

        ret3 = Writer.write(file_dic, {1: 3, 4: 5, 6: 7})
        infile2 = self.read_default(file_dic, mode="r", encoding=Files.DEFAULT_ENCODING, newline='')

        self.assertEqual(ret3, dic)
        self.assertEqual(infile2, str_dic)

        self.remove(file_dic)

    def test_write_byte_string(self):
        # String #
        string = bytes("Lovely message äüöß?", encoding=Files.DEFAULT_ENCODING)
        file_string = self.file_path("bytes_str")

        ret = Writer.write(file_string, string, Files.BYTE)
        infile = self.read_default(file_string, mode="rb")

        self.assertEqual(ret, string)
        self.assertEqual(infile, string)

        self.remove(file_string)

    def test_write_byte_dict(self):
        # Dict #
        dic = bytes(str({1: 3, 4: 5, 6: 7}), encoding=Files.DEFAULT_ENCODING)
        file_dic = self.file_path("bytes_dict")

        ret = Writer.write(file_dic, dic, Files.BYTE)
        infile = self.read_default(file_dic, mode="rb")

        self.assertEqual(ret, dic)
        self.assertEqual(infile, dic)

        self.remove(file_dic)

    def test_write_byte_array(self):
        # Array #
        array = bytes(str([1, 2, 3, 4, 5]), encoding=Files.DEFAULT_ENCODING)
        file_array = self.file_path("bytes_array")

        ret = Writer.write(file_array, array, Files.BYTE)
        infile = self.read_default(file_array, mode="rb")

        self.assertEqual(ret, array)
        self.assertEqual(infile, array)

        self.remove(file_array)

    def test_write_custom(self):
        message = "Another lovely test message äüöß?"
        additional = "One more, didn't expected, didn't ya äüöß??"

        res_message = Writer.write_custom("file1", message, mode="a", encoding=Files.DEFAULT_ENCODING)
        res_additional = Writer.write_custom("file1", additional, mode="a", encoding=Files.DEFAULT_ENCODING)

        self.assertEqual(message, res_message)
        self.assertEqual(additional, additional)

        infile = self.read_default("file1", mode="r", encoding=Files.DEFAULT_ENCODING)
        self.assertEqual(message + additional, infile)

        self.remove("file1")

    def test_write_pretty_string(self):
        # String #
        string = "\r\n\r\n lovely öaü?"
        pretty = pprint.pformat(string)

        file = self.file_path("pretty_array")

        ret = Writer.write(file, string, Files.PRETTY)
        infile = self.read_default(file, mode="r", encoding=Files.DEFAULT_ENCODING)

        self.assertEqual(ret, string)
        self.assertEqual(infile, pretty)

        self.remove(file)

    def test_write_pretty_array(self):
        # Array #
        array = [1, 2, 3, 4, 5]
        pretty = pprint.pformat(array)

        file = self.file_path("pretty_array")

        ret = Writer.write(file, array, Files.PRETTY)
        infile = self.read_default(file, mode="r", encoding=Files.DEFAULT_ENCODING)

        self.assertEqual(ret, array)
        self.assertEqual(infile, pretty)

        self.remove(file)



    def test_write_undefined(self):
        self.assertRaises(TypeError, lambda: Writer.write("_", "", "RANDOM TYPE"))

    def test_write_not_byte(self):
        self.assertRaises(TypeError, lambda: Writer.write_byte("_", "notbyte"))

    def read_default(self, file, **kwargs):
        with open(file, **kwargs) as f:
            result = f.read()
        return result

    def write_default(self, file, content, **kwargs):
        with open(file, **kwargs) as f:
            f.write(content)

    def remove(self, *filename):
        for f in filename:
            os.remove(f)

    def file_path(self, name):
        return os.path.join(self.dir, name)



if __name__ == '__main__':
    unittest.main()
