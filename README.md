# ttgn.pokedex

[![Build Status](https://travis-ci.org/thetallgrassnet/ttgn.pokedex.svg?branch=master)](https://travis-ci.org/thetallgrassnet/ttgn.pokedex)
[![Coverage Status](https://coveralls.io/repos/github/thetallgrassnet/ttgn.pokedex/badge.svg?branch=master)](https://coveralls.io/github/thetallgrassnet/ttgn.pokedex?branch=master)

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

### Additional requirements

 * Pyenv
   
### Setup

```bash
pyenv install 3.7.0 3.4.9 3.5.6 3.6.6
pyenv local 3.7.0 3.4.9 3.5.6 3.6.6
```

### Running tests

(Prefix commands with `pipenv run` if using Pipenv.)

```bash
tox
```

If a new dependency was added to `requirements.txt`:

```bash
tox -r
```

## Usage

```python
import ttgn.pokedex
pokedex = ttgn.pokedex.Pokedex("postgres://user:pass@host:port/db")
```

## Copyright

Copyright © 2018 Jesse B. Hannah. Licensed under the terms of the MIT License
(see [LICENSE](LICENSE)).

"Pokémon" and all character names and game data are copyright © The Pokémon
Company International, and are used in this project for **information purposes
only**, which is believed to be covered as fair use under US copyright law.
