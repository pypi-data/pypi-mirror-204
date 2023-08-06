
# pokepastes-scraper

A simple library that converts a Pokemon team from https://pokepast.es to a object in Python. Supports conversion to and from JSON.

### Installation

```
pip install -U pokepastes-scraper
```

### Usage 

Let's say we want to parse [this team](https://pokepast.es/5c46f9ec443664cb) which Gavin Michaels used to win the [Oceania World Championships](https://victoryroadvgc.com/2023-ocic/). Simply call `team_from_url`:

```python
import pokepastes_scraper as pastes

team = pastes.team_from_url("https://pokepast.es/5c46f9ec443664cb")

for mon in team.members:
    print(f'{mon.species} with {mon.item or "no item"} (Tera: {mon.tera_type})')
```

Output: 

```
Iron Hands with Assault Vest (Tera: Grass)
Amoonguss with Sitrus Berry (Tera: Steel)
Pelipper with Focus Sash (Tera: Flying)
Palafin with Mystic Water (Tera: Water)
Baxcalibur with Dragon Fang (Tera: Poison)
Dragonite with Lum Berry (Tera: Flying)
```

For a detailed example output of `team_from_url`, see `example/example.py` and its output `example/example_team.json`.

Tested in python 3.11, but likely compatible with 3.10+. Feel free to contact me: myapaulogies@tuta.io