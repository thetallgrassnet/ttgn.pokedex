import os

import pytest
import ttgn
import ttgn.pokedex


@pytest.fixture(scope='session')
def pokedex():
    path = os.path.realpath(
        os.path.join(ttgn.__path__[0], '..', 'tests', 'pokedex_test.sqlite3'))
    uri = 'sqlite:///{}'.format(path)
    yield ttgn.pokedex.Pokedex(uri)
    os.remove(path)
