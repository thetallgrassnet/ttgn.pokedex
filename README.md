# ttgn.pokedex

A database of Pokémon information.

## Development

### Requirements

 * Python 3.5+
 * Pipenv

### Setup

```bash
pipenv install
pipenv run python
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
