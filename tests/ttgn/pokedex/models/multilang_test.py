"""Test the ttgn.pokedex.models.multilang module."""
# pylint: disable=no-self-use
import pytest

from ttgn.pokedex.models.base import Base
from ttgn.pokedex.models.multilang import (Language, LanguageTranslation,
                                           with_translations)


class TestLanguage:
    """Test the ttgn.pokedex.models.multilang.Language class."""

    def test_migration(self, pokedex):
        """Test that data migrations are run correctly for the model."""
        query = pokedex.query(Language)
        assert query.count() == 17

    def test_str(self, pokedex):
        """Test that the subtag is returned."""
        cn = pokedex.query(Language).get(12)
        assert str(cn) == 'cmn-latn-cn-pinyin'

    class TestSubtag:
        """Test the ttgn.pokedex.models.multilang.Language.subtag
        property."""

        def test_subtag_language_only(self, pokedex):
            """Test that the correct subtag with only the language identifier is
            returned."""
            en = pokedex.query(Language).get(5)
            assert en.subtag == 'en'

        def test_subtag_concatenated(self, pokedex):
            """Test that the concatenated subtag is returned."""
            ja = pokedex.query(Language).get(4)
            assert ja.subtag == 'ja-latn-x-official'

        def test_subtag_query(self, pokedex):
            """Test querying by subtag."""
            fr = pokedex.query(Language).filter(
                Language.subtag == 'fr-fr').one()
            assert fr.id == 14

    class TestTranslations:
        """Test the ttgn.pokedex.models.multilang.Language.translations
        relationship."""

        def test_migration(self, pokedex):
            """Test that the data migrations are run correctly for the model."""
            query = pokedex.query(LanguageTranslation)
            assert query.count() == 129

    class TestName:
        """Test the ttgn.pokedex.models.multilang.Language.name association
        proxy."""

        def test_name(self, pokedex):
            en = pokedex.query(Language).get(5)
            assert set(en.name) == set([
                '英語', 'English', '영어', '英语', '英語', 'Anglaise', 'Inglés',
                'Inglese', 'Englische'
            ])


class TestWithTranslations:
    """Test the ttgn.pokedex.models.multilang.with_translations decorator."""

    def test_with_translation_type_error(self):
        class TestModel(Base):
            pass

        with pytest.raises(TypeError) as error:
            with_translations(name='foobar')(TestModel)
        assert 'name expected to be a sqlalchemy.Column, was foobar' == str(
            error.value)
