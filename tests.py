import unittest
from config_lang import ConfigLangParser

class TestConfigLang(unittest.TestCase):
    def test_constants(self):
        parser = ConfigLangParser()
        parser.parse("def a = 5;")
        self.assertEqual(parser.constants["a"], 5)

    def test_reserved_operator(self):
        parser = ConfigLangParser()
        with self.assertRaises(SyntaxError) as context:
            parser.parse("!(5 < 3)")
        self.assertIn("Operator '<' is reserved for future use", str(context.exception))

    def test_expression(self):
        parser = ConfigLangParser()
        parser.parse("def a = 10;")
        result = parser.parse("!(a 5 +)")
        self.assertEqual(result, 15)

    def test_array(self):
        parser = ConfigLangParser()
        result = parser.parse("{ 1. 2. 3. }")
        self.assertEqual(result, [1, 2, 3])

if __name__ == "__main__":
    unittest.main()