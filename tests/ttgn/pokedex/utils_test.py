# pylint: disable=no-self-use
"""Test the ttgn.pokedex.utils module."""
import pytest

from ttgn.pokedex import utils


class TestSnakeCase:
    """Test the ttgn.pokedex.utils.snake_case function."""

    def test_snake_case(self):
        """Tests that the input string is correctly converted to
        snake_case."""
        assert utils.snake_case('VersionGroup') == 'version_group'


class TestImportString:
    """Test the ttgn.pokedex.utils.import_string function."""

    def test_import_string(self):
        """Tests that the correct module is imported for the given fully-
        qualified module path."""
        assert utils.import_string('ttgn.pokedex.utils') == utils

    def test_import_string_invalid_path(self):
        """Test that an ImportError with the correct message is raised given
        an invalid module path."""
        invalid_path = 'some invalid module path'
        with pytest.raises(ImportError) as error:
            utils.import_string(invalid_path)
        assert '{} doesn\'t look like a module path'.format(
            invalid_path) == str(error.value)

    def test_import_string_missing_module(self):
        """Test that an ImportError with the correct message is raised given
        a name that does not correspond to an importable module."""
        invalid_module = 'ttgn.nonexistent_module.foobar'
        with pytest.raises(ImportError):
            utils.import_string(invalid_module)

    def test_import_string_missing_class_or_attribute(self):
        """Test that an ImportError with the correct message is raised given
        a name that does not correspond to an importable class or attribute
        on an importable module."""
        valid_module = 'ttgn.pokedex'
        invalid_class = 'NonexistentClass'
        with pytest.raises(ImportError) as error:
            utils.import_string('{}.{}'.format(valid_module, invalid_class))
        assert 'Module {} has no class or attribute {}'.format(
            valid_module, invalid_class) == str(error.value)
