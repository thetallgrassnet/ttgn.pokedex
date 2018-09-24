# ttgn.pokedex

[![Build Status](https://travis-ci.org/thetallgrassnet/ttgn.pokedex.svg?branch=master)](https://travis-ci.org/thetallgrassnet/ttgn.pokedex)
[![Coverage Status](https://coveralls.io/repos/github/thetallgrassnet/ttgn.pokedex/badge.svg?branch=master)](https://coveralls.io/github/thetallgrassnet/ttgn.pokedex?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/1036c05a50abb42d3335/maintainability)](https://codeclimate.com/github/thetallgrassnet/ttgn.pokedex/maintainability)

A database of Pokémon information.

## Development

### Requirements

 * Python 3.4+
 * Pip

### Setup

```bash
python3 -m venv ./venv
. venv/bin/activate
pip install -e .[development,testing]
```

Or with Pipenv (recommended):

```bash
pipenv install
pipenv run python
```

## Testing

### Against a single Python version

(Prefix commands with `pipenv run` if using Pipenv.)

```bash
py.test
```

### Against all supported Python versions

#### Additional requirements

 * Pyenv
   
#### Setup

```bash
pyenv install 3.4.9
pyenv install 3.5.6
pyenv install 3.6.6
pyenv install 3.7.0
pyenv install pypy3.5-6.0.0
pyenv local 3.7.0 3.4.9 3.5.6 3.6.6 pypy3.5-6.0.0
```

#### Running tests

```bash
tox
```

If a new dependency was added to `requirements.txt`:

```bash
tox -r
```

## Usage

```python
from ttgn.pokedex import Pokedex
from ttgn.pokedex.models.versions import Version
pokedex = Pokedex("postgres://user:pass@host:port/db")
red = pokedex.query(Version).where(Version.name == 'Red')
```

The database will be initialized or migrated when the Pokédex is instantiated.
One Pokédex instance should be shared for the lifetime of the running
application that uses it, with operations either using the `pokedex.query`
method to wrap individual `SELECT` queries in transactions, or using the
`pokedex.session_scope` method to wrap multiple queries in a transactional
scope:

```python
with pokedex.session_scope() as session:
    red = session.query(Version).where(Version.name == 'Red')
    charmander = session.query(Species).where(Species.name == 'Charmander')
```

## Copyright

Copyright © 2018 Jesse B. Hannah. Licensed under the terms of the MIT License
(see [LICENSE](LICENSE)).

"Pokémon" and all character names and game data are copyright © The Pokémon
Company International, and are used in this project for **information purposes
only**, which is believed to be covered as fair use under US copyright law.
