import pytest
from ttgn.pokedex import utils


class TestUtils(object):
    def test_snake_case(self):
        assert utils.snake_case('VersionGroup') == 'version_group'

    def test_import_string(self):
        assert utils.import_string('ttgn.pokedex.utils') == utils

    def test_import_string_invalid_path(self):
        invalid_path = 'some invalid module path'
        with pytest.raises(ImportError) as e:
            utils.import_string(invalid_path)
        assert '{} doesn\'t look like a module path'.format(
            invalid_path) == str(e.value)

    def test_import_string_missing_module(self):
        invalid_module = 'ttgn.nonexistent_module.foobar'
        with pytest.raises(ImportError):
            utils.import_string(invalid_module)

    def test_import_string_missing_class_or_attribute(self):
        valid_module = 'ttgn.pokedex'
        invalid_class = 'NonexistentClass'
        with pytest.raises(ImportError) as e:
            utils.import_string('{}.{}'.format(valid_module, invalid_class))
        assert 'Module {} has no class or attribute {}'.format(
            valid_module, invalid_class) == str(e.value)
