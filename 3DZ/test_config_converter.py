import unittest
import yaml
from config_converter import ConfigConverter

class TestConfigConverter(unittest.TestCase):

    def test_example1(self):
        with open('example1.yaml') as f:
            yaml_data = f.read()
        expected_output = open('expected1.conf').read()

        converter = ConfigConverter(yaml_data)
        output = converter.convert()

        self.assertEqual(output.strip(), expected_output.strip())

    def test_example2(self):
        with open('example2.yaml') as f:
            yaml_data = f.read()
        expected_output = open('expected2.conf').read()

        converter = ConfigConverter(yaml_data)
        output = converter.convert()

        self.assertEqual(output.strip(), expected_output.strip())

if __name__ == '__main__':
    unittest.main()