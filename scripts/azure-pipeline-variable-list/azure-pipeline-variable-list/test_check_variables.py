import unittest
from check_variables import extract_variables

class TestExtractVariables(unittest.TestCase):
    def test_basic_variables(self):
        content = """
        $(SIMPLE_VAR)
        $(simple_var)
        $(myVariable)
        $(MY_VARIABLE_123)
        """
        expected = {'SIMPLE_VAR', 'simple_var', 'myVariable', 'MY_VARIABLE_123'}
        self.assertEqual(extract_variables(content), expected)

    def test_ignore_commands(self):
        content = """
        $(VALID_VAR)
        $(echo hello)
        $(curl http://example.com)
        $(MY_VAR)
        """
        expected = {'VALID_VAR', 'MY_VAR'}
        self.assertEqual(extract_variables(content), expected)

    def test_mixed_content(self):
        content = """
        steps:
        - script: |
            echo "Using $(BUILD_ID)"
            echo "Path: $(system.defaultWorkingDirectory)"
            echo "Invalid $( space in var )"
            echo "$(MY-INVALID-VAR)"
        """
        expected = {'BUILD_ID', 'system.defaultWorkingDirectory'}
        self.assertEqual(extract_variables(content), expected)

    def test_empty_and_invalid(self):
        content = """
        $()
        $(123invalid)
        $(-invalid)
        $(VALID_123)
        """
        expected = {'VALID_123'}
        self.assertEqual(extract_variables(content), expected)

    def test_nested_variables(self):
        content = """
        $(VAR1)$(VAR2)
        $(nested.variable)
        $(deeply.nested.variable)
        """
        expected = {
            'VAR1', 'VAR2',
            'nested.variable',
            'deeply.nested.variable'
        }
        self.assertEqual(extract_variables(content), expected)

if __name__ == '__main__':
    unittest.main() 