import requests
import json
import pandas as pd

urlBaseV1_1 = 'https://statsapi.mlb.com/api/v1.1/'

def getPitchers(rawData):
    df = {
        'Team': [],
        'Pitcher': [],
        'BattersFaced': [],
        'TotalOuts': [],
        'Singles': [],
        'Doubles': [],
        'Triples': [],
        'HomeRuns': [],
        'Walks': [],
        'HP': [],
        'atBats': [],
        'runs': [],
        'earnedRuns': [],
        'seasonERA': []
    }
    data = rawData['liveData']['boxscore']
    away = data['teams']['away']['team']['name']
    for jugador in data['teams']['away']['players'].values():
        if jugador['position']['code'] != '1' or len(jugador['stats']['pitching']) == 0:
            continue
        df['Team'].append(away)
        df['Pitcher'].append(jugador['person']['fullName'])
        df['BattersFaced'].append(jugador['stats']['pitching']['battersFaced'])
        df['TotalOuts'].append(jugador['stats']['pitching']['outs'])
        df['Doubles'].append(jugador['stats']['pitching']['doubles'])
        df['Triples'].append(jugador['stats']['pitching']['triples'])
        df['HomeRuns'].append(jugador['stats']['pitching']['homeRuns'])
        df['Singles'].append(jugador['stats']['pitching']['hits'] - df['Doubles'][-1] - df['Triples'][-1] - df['HomeRuns'][-1])
        df['Walks'].append(jugador['stats']['pitching']['baseOnBalls'] + jugador['stats']['pitching']['intentionalWalks'])
        df['HP'].append(jugador['stats']['pitching']['hitByPitch'])
        df['atBats'].append(jugador['stats']['pitching']['atBats'])
        df['runs'].append(jugador['stats']['pitching']['runs'])
        df['earnedRuns'].append(jugador['stats']['pitching']['earnedRuns'])
        df['seasonERA'].append(float(jugador['seasonStats']['pitching']['era']))

    home = data['teams']['home']['team']['name']
    for jugador in data['teams']['home']['players'].values():
        if jugador['position']['code'] != '1' or len(jugador['stats']['pitching']) == 0:
            continue
        df['Team'].append(home)
        df['Pitcher'].append(jugador['person']['fullName'])
        df['BattersFaced'].append(jugador['stats']['pitching']['battersFaced'])
        df['TotalOuts'].append(jugador['stats']['pitching']['outs'])
        df['Doubles'].append(jugador['stats']['pitching']['doubles'])
        df['Triples'].append(jugador['stats']['pitching']['triples'])
        df['HomeRuns'].append(jugador['stats']['pitching']['homeRuns'])
        df['Singles'].append(jugador['stats']['pitching']['hits'] - df['Doubles'][-1] - df['Triples'][-1] - df['HomeRuns'][-1])
        df['Walks'].append(jugador['stats']['pitching']['baseOnBalls'] + jugador['stats']['pitching']['intentionalWalks'])
        df['HP'].append(jugador['stats']['pitching']['hitByPitch'])
        df['atBats'].append(jugador['stats']['pitching']['atBats'])
        df['runs'].append(jugador['stats']['pitching']['runs'])
        df['earnedRuns'].append(jugador['stats']['pitching']['earnedRuns'])
        df['seasonERA'].append(float(jugador['seasonStats']['pitching']['era']))

    df = pd.DataFrame(df)
    df.to_csv('data/pitchers.csv', index=False)

def getBatters(rawData):
    df = {
        'Team': [],
        'Bateador': [],
        'Position': [],
        'Singles': [],
        'Doubles': [],
        'Triples': [],
        'HomeRuns': [],
        'Walks': [],
        'HP': [],
        'atBats': [],
        'runs': [],
        'rbi': [],
        'seasonAVG': [],
        'seasonOPS': [],
    }
    data = rawData['liveData']['boxscore']
    away = data['teams']['away']['team']['name']
    for jugador in data['teams']['away']['players'].values():
        if len(jugador['stats']['batting']) == 0:
            continue
        df['Team'].append(away)
        df['Bateador'].append(jugador['person']['fullName'])
        df['Position'].append(jugador['position']['abbreviation'])
        df['Doubles'].append(jugador['stats']['batting']['doubles'])
        df['Triples'].append(jugador['stats']['batting']['triples'])
        df['HomeRuns'].append(jugador['stats']['batting']['homeRuns'])
        df['Singles'].append(jugador['stats']['batting']['hits'] - df['Doubles'][-1] - df['Triples'][-1] - df['HomeRuns'][-1])
        df['Walks'].append(jugador['stats']['batting']['baseOnBalls'] + jugador['stats']['batting']['intentionalWalks'])
        df['HP'].append(jugador['stats']['batting']['hitByPitch'])
        df['atBats'].append(jugador['stats']['batting']['atBats'])
        df['runs'].append(jugador['stats']['batting']['runs'])
        df['rbi'].append(jugador['stats']['batting']['rbi'])
        df['seasonAVG'].append(float(jugador['seasonStats']['batting']['avg']))
        df['seasonOPS'].append(float(jugador['seasonStats']['batting']['ops']))

    home = data['teams']['home']['team']['name']
    for jugador in data['teams']['home']['players'].values():
        if len(jugador['stats']['batting']) == 0:
            continue
        df['Team'].append(home)
        df['Bateador'].append(jugador['person']['fullName'])
        df['Position'].append(jugador['position']['abbreviation'])
        df['Doubles'].append(jugador['stats']['batting']['doubles'])
        df['Triples'].append(jugador['stats']['batting']['triples'])
        df['HomeRuns'].append(jugador['stats']['batting']['homeRuns'])
        df['Singles'].append(jugador['stats']['batting']['hits'] - df['Doubles'][-1] - df['Triples'][-1] - df['HomeRuns'][-1])
        df['Walks'].append(jugador['stats']['batting']['baseOnBalls'] + jugador['stats']['batting']['intentionalWalks'])
        df['HP'].append(jugador['stats']['batting']['hitByPitch'])
        df['atBats'].append(jugador['stats']['batting']['atBats'])
        df['runs'].append(jugador['stats']['batting']['runs'])
        df['rbi'].append(jugador['stats']['batting']['rbi'])
        df['seasonAVG'].append(float(jugador['seasonStats']['batting']['avg']))
        df['seasonOPS'].append(float(jugador['seasonStats']['batting']['ops']))

    df = pd.DataFrame(df)
    df.to_csv('data/bateadores.csv', index=False)


if __name__ == "__main__":
    juego_id = 809632
    datosJuegoRaw = requests.get(urlBaseV1_1 + f'game/{juego_id}/feed/live').content
    datosJuegoRaw = json.loads(datosJuegoRaw)
    getPitchers(datosJuegoRaw)
    getBatters(datosJuegoRaw)