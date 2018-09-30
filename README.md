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
pipenv install -d
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

* Pyenv, with all of the supported Python versions installed and locally
  available:

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

### SQLAlchemy integration

If you want to use the Pokédex in a project that already uses SQLAlchemy, and
want the Pokédex tables to belong to the same database as your project's tables,
you can pass a `sqlalchemy.engine.Engine` instance to the `Pokedex` constructor
instead of a database connection string:

```python
engine = create_engine("postgres://user:pass@host:port/your_project_db")
pokedex = Pokedex(engine)
```

### Alembic integration

If you want to use the Pokédex in a project that uses Alembic, you can add the
Pokédex migrations to your existing `alembic.ini` file. This will allow your
migrations to depend on Pokédex migrations, and will run the Pokédex migrations
alongside your own with `alembic upgrade heads`. To do this, add the resource
identifier for the Pokédex migration version location to [`version_locations` in
your
`alembic.ini`](http://alembic.zzzcomputing.com/en/latest/branches.html#setting-up-multiple-version-directories):

```ini
# version location specification; this defaults
# to foo/versions.  When using multiple version
# directories, initial revisions must be specified with --version-path
version_locations = your/alembic/versions ttgn.pokedex:migrations/versions
```

You can then either load and pass your project's Alembic configuration to the
`Pokedex` constructor with the `alembic_cfg` parameter to run the Pokédex
migrations with your own project's configuration at instantiation, or run the
migrations yourself and disable automatic migrations by passing `migrate=False`
to the constructor.

## Copyright

Copyright © 2018 Jesse B. Hannah. Licensed under the terms of the MIT License
(see [LICENSE](LICENSE)).

"Pokémon" and all character names and game data are copyright © The Pokémon
Company International, and are used in this project for **information purposes
only**, which is believed to be covered as fair use under US copyright law.
