import requests
import json
import pandas as pd

urlBaseV1_1 = 'https://statsapi.mlb.com/api/v1.1/'

def getPitchers(rawData):
    df = {
        'Team': [],
        'Pitcher': [],
        'Outs': [],
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
    for jugador in data['teams']['away']['players']:
        if jugador['position']['code'] == '1' and len(jugador['stats']['pitching']) > 0:
            df['Team'].append(away)
            df['Pitcher'].append(jugador['person']['fullName'])
            df['Outs'].append(jugador['stats']['pitching']['outs'])
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
    for jugador in data['teams']['home']['players']:
        if jugador['position']['code'] == '1' and len(jugador['stats']['pitching']) > 0:
            df['Team'].append(home)
            df['Pitcher'].append(jugador['person']['fullName'])
            df['Outs'].append(jugador['stats']['pitching']['outs'])
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
    df.to_csv('../data/pitchers.csv', index=False)

if __name__ == "__main__":
    juego_id = 809632
    datosJuegoRaw = requests.get(urlBaseV1_1 + f'game/{juego_id}/feed/live').content
    datosJuegoRaw = json.loads(datosJuegoRaw)
    getPitchers(datosJuegoRaw)