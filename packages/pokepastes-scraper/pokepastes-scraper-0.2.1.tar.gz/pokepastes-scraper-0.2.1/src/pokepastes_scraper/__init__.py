
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from dataclasses import dataclass
import os, itertools as it
from dataclasses import dataclass
import json


__all__ = [
    "team_from_url"
]


@dataclass
class Stats:
    HP: int = None
    Atk: int = None
    Def: int = None
    SpA: int = None
    SpD: int = None
    Spe: int = None

    def to_dict(self):
        return { k: v for k, v in self.__dict__.items() if v != None }


    # e.g. stat_string = "4 Atk"
    def _add_from_str(self, stat_string):
        val, stat = stat_string.split(' ')
        val = int(val)
        setattr(self, stat, val)


# https://pokepast.es/syntax.html 
# https://github.com/smogon/pokemon-showdown-client/blob/master/js/storage.js#L1291 ()
@dataclass
class PokepastesMon:
    # this should be the order they appear on the team's webpage
    # `None` means "unspecified"
    species: str = None
    nickname: str = None
    gender: str = None
    item: str = None
    ability: str = None
    level: int = None
    shiny: bool = None
    happiness: int = None
    pokeball: str = None
    # hidden_power_type: str = None # unnecessary?
    dynamax_level: int = None
    gigantamax: bool = None
    tera_type: str = None
    evs: Stats = None
    nature: str = None
    ivs: Stats = None
    moveset: list[str] = None

    def to_dict(self):
        '''Returns __dict__, excluding all fields that are `None`.'''
        res = {}
        for k, v in self.__dict__.items():
            if v == None:
                continue
            
            if type(v) == Stats:
                res[k] = v.to_dict()
                continue
            
            res[k] = v

        return res

    @staticmethod
    def _from_pre(tag: Tag):
        # rule of thumb for this function: n = next(tags_iter) whenever you are done with n's current value
        tags_iter = iter(tag.children)
        res = PokepastesMon('asdfasdf')

        firstline = ''
        while True:
            n = next(tags_iter)
            firstline += n.text

            if '\n' in n.text:
                n = next(tags_iter)
                break

        if '@' in firstline:
            firstline, res.item = [s.strip() for s in firstline.split(' @ ')]
        
        # splits into "Nick", "Species)", "Gender)"
        parts = firstline.split(' (')

        if len(parts) == 1:
            res.species = firstline
        else:
            if parts[-1][1] in 'FM':
                res.gender = parts.pop()[1]
            
            if len(parts) == 1:
                res.species = parts[0]
            else:
                res.nickname = parts[0]
                # [1:-1] trims closing parentheses that we haven't trimmed yet
                res.species = parts[1][:-1]


        # iterate through everything before moveset:
        while True:
            curr = n.text.strip()
            match curr:
                case 'Ability:':
                    n = next(tags_iter)
                    res.ability = n.text.strip()
                case 'Level:':
                    n = next(tags_iter)
                    res.level = int(n.text)
                case 'Shiny:':
                    n = next(tags_iter)
                    res.shiny = True
                case 'Happiness:':
                    n = next(tags_iter)
                    res.happiness = n.text.strip()
                case 'Pokeball:':
                    n = next(tags_iter)
                    res.pokeball = n.text.strip()
                case 'Dynamax Level:':
                    n = next(tags_iter)
                    res.dynamax_level = n.text.strip()
                case 'Gigantamax:':
                    n = next(tags_iter)
                    res.gigantamax = True
                case 'Tera Type:':
                    n = next(tags_iter)
                    res.tera_type = n.text.strip()
                # see below match statement for evs: ivs: case
                case '-':
                    break
                case other:
                    if curr.strip().endswith('Nature'):
                        res.nature, _ = curr.split()

            if curr and curr in 'EVs:IVs:':
                if curr == 'IVs:':
                    stats = res.ivs = Stats()
                else:
                    stats = res.evs = Stats()
                
                while True:
                    n = next(tags_iter)
                    stats._add_from_str(n.text.strip())
                    
                    n = next(tags_iter)
                    if n.text != ' / ':
                        break
            
            else:
                n = next(tags_iter)
        
    
        # n is on a '-' before the first move
        res.moveset = []

        # skip '-'
        n = next(tags_iter)

        for _ in range(3):
            res.moveset.append(n.text.strip())
            n = next(tags_iter)
            # skip '-'
            n = next(tags_iter)

        # don't `n = next(tags_iter)` on the last iteration to not raise StopIteration
        res.moveset.append(n.text.strip())
        return res


@dataclass
class PokepastesTeam:
    # IF YOU RENAME THIS FIELD THEN CHECK: to_dict, team_from_json 
    members: list[PokepastesMon] = None

    title: str = None
    author: str = None
    desc: str = None

    def to_dict(self) -> dict:
        '''Returns `__dict__`, excluding all fields that are `None`. Calls `PokepastesMon.to_dict` on each Pokemon in `members`.'''
        res = {}
        for k, v in self.__dict__.items():
            if v == None:
                continue
            if k == 'members':
                res[k] = [mon.to_dict() for mon in self.members]
                continue
            
            res[k] = v

        return res


    def to_json(self) -> str:
        '''Serializes to JSON based on `to_dict` method.'''
        return json.dumps(self.to_dict())



def _mon_from_dict(d: dict):
    res = PokepastesMon()

    for k,v in d.items():
        if k in ('evs', 'ivs'):
            if k == 'evs':
                stat = res.evs = Stats()
            else:
                stat = res.ivs = Stats()

            for statname, value in v.items():
                setattr(stat, statname, value)
        else:
            try:
                setattr(res, k, v)
            except AttributeError:
                print('WARN: skipping unknown field', k)
    
    return res


def team_from_dict(d: dict):
    '''Returns a team given a `dict` representation of the JSON generated with `PokepastesTeam.to_json()`.'''
    res = PokepastesTeam()
    
    for k,v in d.items():
        if k == 'members':
            res.members = [_mon_from_dict(mon) for mon in v]
        else:
            try:
                setattr(res, k, v)
            except AttributeError:
                print('WARN: skipping unknown field', k)
    
    return res

def team_from_json(json_string: str | bytes | bytearray):
    '''Returns a team given a JSON that was generated with `PokepastesTeam.to_json()`.'''
    return team_from_dict(json.loads(json_string))


def team_from_url(url: str):
    page = requests.get(url)
    return team_from_html(page.text)

def team_from_html(text: str):
    res = PokepastesTeam()
    soup = BeautifulSoup(text, 'html.parser')

    sidebar: Tag = soup.find('aside')
    sidebar_iter = iter(sidebar.children)

    # get first six elements, and save three meaningful ones
    _, res.title, _, author_line, _, res.desc = \
        [i.text.strip() or None for i in it.islice(sidebar_iter, 6)]

    # get stuff right of first 'by' (there must be a better way)
    res.author = ''.join(author_line.split('by')[1:]).strip()

    html_mons = soup.find_all('pre')    
    res.members = [PokepastesMon._from_pre(mon) for mon in html_mons]

    return res