"""py.test configuration and fixtures."""
import os

from pytest import fixture

from ttgn.pokedex import Pokedex


@fixture(scope='session')
def pokedex():
    """Yield a ttgn.pokedex.Pokedex instance to the session, using and deleting
    a sqlite3 database for data storage."""
    path = os.path.realpath(
        os.path.join(os.path.dirname(__file__), 'pokedex_test.sqlite3'))
    uri = 'sqlite:///{}'.format(path)
    yield Pokedex(uri)
    os.remove(path)
