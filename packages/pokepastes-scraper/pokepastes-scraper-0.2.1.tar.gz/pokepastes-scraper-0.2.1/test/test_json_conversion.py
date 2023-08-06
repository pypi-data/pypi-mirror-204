

from pokepastes_scraper import team_from_url, team_from_json

urls = [
    'https://pokepast.es/5c46f9ec443664cb',
    'https://pokepast.es/306eacdf0f3789b3',
    'https://pokepast.es/faa1127c4292d860',
    'https://pokepast.es/403fdb8c4b14b54e',
    'https://pokepast.es/8bbd5d5a5434c61f',
    'https://pokepast.es/6a481bd544cdc477',
    'https://pokepast.es/345ec225c2414bd9',
]

teams = [team_from_url(url) for url in urls]


for team in teams:
    json_rep = team.to_json()

    teamcopy = team_from_json(json_rep)

    assert teamcopy.to_json() == json_rep

    # first_name = team.title.split()[0]
    # filename = f'{first_name.lower()}.json'
    # with open(filename, 'w') as f:
    #     f.write(json)


