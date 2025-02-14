import unittest
from check_variables import extract_variables, extract_variable_names

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

class TestExtractVariableNames(unittest.TestCase):
    def test_basic_variable_names(self):
        content = """
        ## - SIMPLE_VAR
        ## - BUILD_ID
        ## - system.defaultWorkingDirectory
        """
        expected = {'SIMPLE_VAR', 'BUILD_ID', 'system.defaultWorkingDirectory'}
        self.assertEqual(extract_variable_names(content), expected)

    def test_with_spaces_and_empty_lines(self):
        content = """
        Some other content
          ## - SPACED_VAR
        
        ## - NO_SPACE_VAR
             ## - INDENTED_VAR
        Not a variable line
        """
        expected = {'SPACED_VAR', 'NO_SPACE_VAR', 'INDENTED_VAR'}
        self.assertEqual(extract_variable_names(content), expected)

    def test_with_additional_content(self):
        content = """
        ## - VAR1 # with comment
        ## - VAR2 (some description)
        ## - VAR3:
        ## - system.path.variable with spaces after
        """
        expected = {'VAR1', 'VAR2', 'VAR3', 'system.path.variable'}
        self.assertEqual(extract_variable_names(content), expected)

    def test_empty_and_invalid(self):
        content = """
        ##- not_valid
        # - also_not_valid
        ## -invalid_no_space
        ## - 
        """
        expected = set()
        self.assertEqual(extract_variable_names(content), expected)

if __name__ == '__main__':
    unittest.main()