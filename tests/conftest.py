import os

from pytest import fixture
from ttgn.pokedex import Pokedex


@fixture(scope='session')
def pokedex():
    path = os.path.realpath(
        os.path.join(os.path.dirname(__file__), 'pokedex_test.sqlite3'))
    uri = 'sqlite:///{}'.format(path)
    yield Pokedex(uri)
    os.remove(path)
