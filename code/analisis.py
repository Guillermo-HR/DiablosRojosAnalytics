import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns

def graficarZonaStrike(ax=None, sz_top=3.5, sz_bot=1.5, vistaCatcher=True):
    if ax is None:
        fig, ax = plt.subplots(figsize=(5, 6))
    sz_left = -0.708
    sz_right = 0.708
    ax.plot([sz_left, sz_right], [sz_bot, sz_bot], 'k-')
    ax.plot([sz_left, sz_left], [sz_bot, sz_top], 'k-')
    ax.plot([sz_right, sz_right], [sz_bot, sz_top], 'k-')
    ax.plot([sz_left, sz_right], [sz_top, sz_top], 'k-')

    if vistaCatcher:
        ax.plot([sz_left, sz_right], [0, 0], 'k-')
        ax.plot([sz_left, sz_left], [0, -0.15], 'k-')
        ax.plot([sz_right, sz_right], [0, -0.15], 'k-')
        ax.plot([sz_left, 0], [-0.15, -0.4], 'k-')
        ax.plot([sz_right, 0], [-0.15, -0.4], 'k-')
    else:
        ax.plot([0, sz_left], [0, -0.25], 'k-')
        ax.plot([0, sz_right], [0, -0.25], 'k-')
        ax.plot([sz_left, sz_left], [-0.25, -0.4], 'k-')
        ax.plot([sz_right, sz_right], [-0.25, -0.4], 'k-')
        ax.plot([sz_left, sz_right], [-0.4, -0.4], 'k-')

    ax.set_xlim(-2.7, 2.7)
    ax.set_ylim(-0.5, 5.7)

    sns.set_style('white')
    sns.despine(right=True, top=True, left=True, bottom=True)
    ax.set_xticks([])
    ax.set_yticks([])
    
    return ax

def graficarDistribucionLanzamientos(dfDist, dfPos, titulo):
    colores = {'FF': '#005F73', 'Curveball': '#94D2BD', 'Splitter': '#EE9B00', 'Slider': '#BB3E03'}
    tipos = dfDist['Tipo lanzamiento'].unique().tolist()
    nTipos = len(tipos)
    columns = 5
    rows = (nTipos//columns) + 1
    fig = plt.figure(figsize=(columns * 3, rows * 3))
    plt.tight_layout()
    gs = GridSpec(rows, columns, figure=fig, 
                width_ratios=[1.7] + [1]*(columns-1), 
                height_ratios=[1]*rows,
                wspace=0.05, hspace=0.05,
                top=0.87
                )
    
    ax1 = fig.add_subplot(gs[0, 0])
    plot = ax1.pie(
        dfDist['Porcentaje'], 
        autopct='%1.1f%%', startangle=90,
        colors=dfDist['Tipo lanzamiento'].map(colores).to_list(),
        wedgeprops=dict(width=0.3),
        radius=0.7,
        pctdistance=1.4
    )
    ax1.text(
        0, 0,
        dfDist['Total'].sum(),
        ha='center', va='center',
        fontsize=12, weight='bold'
    )
    ax1.legend(plot[0], dfDist['Tipo lanzamiento'],
          loc="lower center",
          ncol=3,
          frameon=False,
          fontsize='small'
    )
    
    for i in range(rows):
        for j in range(1, columns):
            if (i * columns + j - 1) >= nTipos:
                continue
            tipo = tipos[(columns-1)*(i)+(j-1)]
            ax = fig.add_subplot(gs[i, j])
            graficarZonaStrike(ax=ax)
            try:
                sns.kdeplot(
                    data=dfPos[dfPos['TaggedPitchType'] == tipo],
                    x=-dfPos['PlateLocSide'],
                    y='PlateLocHeight',
                    color='red',
                    fill=True
                )
            except:
                pass
            sns.scatterplot(
                data=dfPos[dfPos['TaggedPitchType'] == tipo],
                x=-dfPos['PlateLocSide'],
                y='PlateLocHeight'
            )
            ax.set_title(tipo, fontsize=12, y=-0.1)

    fig.suptitle(titulo, fontsize=16, y=0.95)
    fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.9)
    return fig

def leerDatos(rutaTrackman, rutaBateadores, rutaPitchers):
    df = pd.read_csv(rutaTrackman, sep=',', encoding='utf-8')
    df['Pitcher'] = df['Pitcher'].str.split(', ').apply(lambda x: x[1] + ' ' + x[0])
    df['Batter'] = df['Batter'].str.split(', ').apply(lambda x: x[1] + ' ' + x[0])
    df['TaggedPitchType'] = df['TaggedPitchType'].str.replace('FourSeamFastBall', 'FF', regex=True)
    homeAtBats = df[df['Top/Bottom'] == 'Bottom'].copy()
    awayAtBats = df[df['Top/Bottom'] == 'Top'].copy()

    pitchers = pd.read_csv(rutaPitchers, sep=',', encoding='utf-8')
    pitchers['Pitcher'] = pitchers['Pitcher'].str.replace('Á', 'A').str.replace('É', 'E').str.replace('Í', 'I').str.replace('Ó', 'O').str.replace('Ú', 'U')
    pitchers['Pitcher'] = pitchers['Pitcher'].str.replace('á', 'a').str.replace('é', 'e').str.replace('í', 'i').str.replace('ó', 'o').str.replace('ú', 'u')
    pitchers['InningsPitch'] = pitchers['TotalOuts'].apply(lambda x: f'{(x // 3)}.{(x % 3)}')

    bateadores = pd.read_csv(rutaBateadores, sep=',', encoding='utf-8')
    bateadores['Bateador'] = bateadores['Bateador'].str.replace('Á', 'A').str.replace('É', 'E').str.replace('Í', 'I').str.replace('Ó', 'O').str.replace('Ú', 'U')
    bateadores['Bateador'] = bateadores['Bateador'].str.replace('á', 'a').str.replace('é', 'e').str.replace('í', 'i').str.replace('ó', 'o').str.replace('ú', 'u')

    homePitchers = pd.merge(
        awayAtBats['Pitcher'], pitchers,
        on='Pitcher'
    ).drop_duplicates().reset_index(drop=True)
    awayPitchers = pd.merge(
        homeAtBats['Pitcher'], pitchers,
        on='Pitcher'
    ).drop_duplicates().reset_index(drop=True)

    homeBateadores = pd.merge(
        homeAtBats['Batter'], bateadores,
        left_on='Batter', right_on='Bateador'
    ).drop_duplicates().reset_index(drop=True)
    awayBateadores = pd.merge(
        awayAtBats['Batter'], bateadores,
        left_on='Batter', right_on='Bateador'
    ).drop_duplicates().reset_index(drop=True)

    atBats = {'home': homeAtBats, 'away': awayAtBats}
    pitchers = {'home': homePitchers, 'away': awayPitchers}
    bateadores = {'home': homeBateadores, 'away': awayBateadores}
    return atBats, pitchers, bateadores

def saveLineUps(bateadores, rutaCSV):
    bateadores['home'][['Bateador', 'Position', 'seasonAVG', 'seasonOPS']].rename(
        columns={'Bateador': 'Nombre', 'Position': 'Posición', 'seasonAVG': 'AVG', 'seasonOPS': 'OPS'}
    ).to_csv(f'{rutaCSV}/homeLineUp.csv', index=False, encoding='utf-8-sig')

    bateadores['away'][['Bateador', 'Position', 'seasonAVG', 'seasonOPS']].rename(
        columns={'Bateador': 'Nombre', 'Position': 'Posición', 'seasonAVG': 'AVG', 'seasonOPS': 'OPS'}
    ).to_csv(f'{rutaCSV}/awayLineUp.csv', index=False, encoding='utf-8-sig')

def savePitchers(pitchers, atBats, rutaCSV):
    ordenColumnas = ['Nombre', 'Entrada de inicio', 'Entradas lanzadas', 'ERA']
    pd.merge(
        pitchers['home'][['Pitcher', 'InningsPitch', 'seasonERA']], atBats['away'].groupby('Pitcher')['Inning'].min(),
        on='Pitcher'
    ).rename(
        columns={'Pitcher': 'Nombre', 'Inning': 'Entrada de inicio', 'InningsPitch':'Entradas lanzadas', 'seasonERA': 'ERA'}
    )[ordenColumnas].to_csv(f'{rutaCSV}/homePitchers.csv', index=False, encoding='utf-8-sig')
    pd.merge(
        pitchers['away'][['Pitcher', 'InningsPitch', 'seasonERA']], atBats['home'].groupby('Pitcher')['Inning'].min(),
        on='Pitcher'
    ).rename(
        columns={'Pitcher': 'Nombre', 'Inning': 'Entrada de inicio', 'InningsPitch':'Entradas lanzadas', 'seasonERA': 'ERA'}
    )[ordenColumnas].to_csv(f'{rutaCSV}/awayPitchers.csv', index=False, encoding='utf-8-sig')

def getLineaPitcheo(pitchers, atBats):
    homeLineaPitcheo = pd.merge(
        pitchers['home'][['Team', 'Pitcher', 'BattersFaced', 'InningsPitch', 'runs', 'earnedRuns']],
        atBats['away'].groupby(['Pitcher', 'BatterSide']).agg(
            NoLanzamientos=pd.NamedAgg(column='PitchNo', aggfunc='count'),
            startInning=pd.NamedAgg(column='Inning', aggfunc='min'),
            Strikes=pd.NamedAgg(column='PitchCall', aggfunc=lambda x: np.where(
                (x.str.startswith('Strike')) | (x.str.startswith('FoulBall')) | (x.str.startswith('InPlay')), 1, 0).sum()),
            SwingStrikes=pd.NamedAgg(column='PitchCall', aggfunc=lambda x: np.where(x == 'StrikeSwinging', 1, 0).sum()),
            Bolas=pd.NamedAgg(column='PitchCall', aggfunc=lambda x: np.where(x.str.startswith('Ball'), 1, 0).sum()),
            Ponches=pd.NamedAgg(column='KorBB', aggfunc=lambda x: np.where(x == 'Strikeout', 1, 0).sum()),
            Walk=pd.NamedAgg(column='KorBB', aggfunc=lambda x: np.where(x == 'Walk', 1, 0).sum())
        ).reset_index(), on='Pitcher'
    ).rename(
        columns={
            'Pitcher': 'Nombre', 'NoLanzamientos': 'No lanzamientos', 'BattersFaced': 'Bateadores enfrentados',
            'startInning': 'Entrada de inicio', 'InningsPitch': 'Entradas lanzadas', 'SwingStrikes': 'Strikes con swing',
            'Walk': 'Bases por bolas', 'runs': 'Carreras', 'earnedRuns': 'Carreras limpias'
        }
    )

    awayLineaPitcheo = pd.merge(
        pitchers['away'][['Team', 'Pitcher', 'BattersFaced', 'InningsPitch', 'runs', 'earnedRuns']],
        atBats['home'].groupby(['Pitcher', 'BatterSide']).agg(
            NoLanzamientos=pd.NamedAgg(column='PitchNo', aggfunc='count'),
            startInning=pd.NamedAgg(column='Inning', aggfunc='min'),
            Strikes=pd.NamedAgg(column='PitchCall', aggfunc=lambda x: np.where(
                (x.str.startswith('Strike')) | (x.str.startswith('FoulBall')) | (x.str.startswith('InPlay')), 1, 0).sum()),
            SwingStrikes=pd.NamedAgg(column='PitchCall', aggfunc=lambda x: np.where(x == 'StrikeSwinging', 1, 0).sum()),
            Bolas=pd.NamedAgg(column='PitchCall', aggfunc=lambda x: np.where(x.str.startswith('Ball'), 1, 0).sum()),
            Ponches=pd.NamedAgg(column='KorBB', aggfunc=lambda x: np.where(x == 'Strikeout', 1, 0).sum()),
            Walk=pd.NamedAgg(column='KorBB', aggfunc=lambda x: np.where(x == 'Walk', 1, 0).sum())
        ).reset_index(), on='Pitcher'
    ).rename(
        columns={
            'Pitcher': 'Nombre', 'NoLanzamientos': 'No lanzamientos', 'BattersFaced': 'Bateadores enfrentados',
            'startInning': 'Entrada de inicio', 'InningsPitch': 'Entradas lanzadas', 'SwingStrikes': 'Strikes con swing',
            'Walk': 'Bases por bolas', 'runs': 'Carreras', 'earnedRuns': 'Carreras limpias'
        }
    )

    lineaPitcheo = {'home': homeLineaPitcheo, 'away': awayLineaPitcheo}

    return lineaPitcheo

def getDistribucionLanzamientos(lineaPitcheo, atBats):
    homeDistribucionLanzamientos = pd.merge(
        lineaPitcheo['home'][['Team', 'Nombre', 'BatterSide', 'No lanzamientos', 'Strikes', 'Strikes con swing', 'Bolas', 'Ponches', 'Bases por bolas']],
        atBats['away'].groupby(['Pitcher', 'BatterSide', 'TaggedPitchType']).agg(
            Uso=pd.NamedAgg(column='PitchNo', aggfunc='count'),
            MaxSpeed= pd.NamedAgg(column='RelSpeed', aggfunc=lambda x: round(x.max(), 1)),
            AvgSpeed=pd.NamedAgg(column='RelSpeed', aggfunc=lambda x:round(x.mean(), 1)),
            StrikesPorTipo=pd.NamedAgg(column='PitchCall', aggfunc=lambda x: np.where(
                (x.str.startswith('Strike')) | (x.str.startswith('FoulBall')) | (x.str.startswith('InPlay')), 1, 0).sum()),
            SwingStrikesPorTipo=pd.NamedAgg(column='PitchCall', aggfunc=lambda x: np.where(x == 'StrikeSwinging', 1, 0).sum()),
            BolasPorTipo=pd.NamedAgg(column='PitchCall', aggfunc=lambda x: np.where(x.str.startswith('Ball'), 1, 0).sum()),
            PonchesPorTipo=pd.NamedAgg(column='KorBB', aggfunc=lambda x: np.where(x == 'Strikeout', 1, 0).sum())
        ).reset_index(), left_on=['Nombre', 'BatterSide'], right_on=['Pitcher', 'BatterSide']
    ).rename(columns={'TaggedPitchType': 'Tipo lanzamiento', 'MaxSpeed': 'Velocidad maxima', 'AvgSpeed': 'Velocidad promedio'})

    awayDistribucionLanzamientos = pd.merge(
        lineaPitcheo['away'][['Team', 'Nombre', 'BatterSide', 'No lanzamientos', 'Strikes', 'Strikes con swing', 'Bolas', 'Ponches', 'Bases por bolas']],
        atBats['home'].groupby(['Pitcher', 'BatterSide', 'TaggedPitchType']).agg(
            Uso=pd.NamedAgg(column='PitchNo', aggfunc='count'),
            MaxSpeed= pd.NamedAgg(column='RelSpeed', aggfunc=lambda x: round(x.max(), 1)),
            AvgSpeed=pd.NamedAgg(column='RelSpeed', aggfunc=lambda x:round(x.mean(), 1)),
            StrikesPorTipo=pd.NamedAgg(column='PitchCall', aggfunc=lambda x: np.where(
                (x.str.startswith('Strike')) | (x.str.startswith('FoulBall')) | (x.str.startswith('InPlay')), 1, 0).sum()),
            SwingStrikesPorTipo=pd.NamedAgg(column='PitchCall', aggfunc=lambda x: np.where(x == 'StrikeSwinging', 1, 0).sum()),
            BolasPorTipo=pd.NamedAgg(column='PitchCall', aggfunc=lambda x: np.where(x.str.startswith('Ball'), 1, 0).sum()),
            PonchesPorTipo=pd.NamedAgg(column='KorBB', aggfunc=lambda x: np.where(x == 'Strikeout', 1, 0).sum())
        ).reset_index(), left_on=['Nombre', 'BatterSide'], right_on=['Pitcher', 'BatterSide']
    ).rename(columns={'TaggedPitchType': 'Tipo lanzamiento', 'MaxSpeed': 'Velocidad maxima', 'AvgSpeed': 'Velocidad promedio'})

    distribucionLanzamientos = pd.concat([homeDistribucionLanzamientos, awayDistribucionLanzamientos], ignore_index=True)
    distribucionLanzamientos=pd.concat(
        [
        distribucionLanzamientos, 
        distribucionLanzamientos.groupby(['Team', 'Nombre', 'Tipo lanzamiento']).agg({
            'BatterSide': lambda x: 'Total',
            'No lanzamientos': 'sum',
            'Strikes': 'sum',
            'Strikes con swing': 'sum',
            'Bolas': 'sum',
            'Ponches': 'sum',
            'Bases por bolas': 'sum',
            'Uso': 'sum',
            'Velocidad maxima': 'max',
            'Velocidad promedio': 'mean',
            'StrikesPorTipo': 'sum',
            'SwingStrikesPorTipo': 'sum',
            'BolasPorTipo': 'sum',
            'PonchesPorTipo': 'sum'
        }).reset_index()
        ]).drop(columns=['Pitcher'])
    distribucionLanzamientos['Porcentaje de uso'] = round(
        (100*distribucionLanzamientos['Uso'])/distribucionLanzamientos['No lanzamientos'], 1)
    distribucionLanzamientos['Strikes %'] = round(
        (100*distribucionLanzamientos['StrikesPorTipo'])/distribucionLanzamientos['Strikes'], 1)
    distribucionLanzamientos['Swing Strikes %'] = round(
        (100*distribucionLanzamientos['SwingStrikesPorTipo'])/distribucionLanzamientos['Strikes con swing'], 1)
    distribucionLanzamientos['Bolas %'] = round(
        (100*distribucionLanzamientos['BolasPorTipo'])/distribucionLanzamientos['Bolas'], 1)
    distribucionLanzamientos['Ponches %'] = round(
        (100*distribucionLanzamientos['PonchesPorTipo'])/distribucionLanzamientos['Ponches'], 1)
    
    return distribucionLanzamientos.fillna(0)

if __name__ == '__main__':
    rutaTrackman = 'data/20250617-EstadioAlfredo-1.csv'
    rutaBateadores = 'data/bateadores.csv'
    rutaPitchers = 'data/pitchers.csv'
    rutaCSV = 'reporte/csv'
    atBats, pitchers, bateadores = leerDatos(rutaTrackman, rutaBateadores, rutaPitchers)
    #saveLineUps(bateadores, rutaCSV)
    #savePitchers(pitchers, atBats, rutaCSV)
    lineaPitcheo = getLineaPitcheo(pitchers, atBats)
    distribucionLanzamientos = getDistribucionLanzamientos(lineaPitcheo, atBats)
    lineaPitcheo['home'].to_csv('lineaPitcheoHome.csv', index=False, encoding='utf-8-sig')
    distribucionLanzamientos.to_csv('distribucionLanzamientos.csv', index=False, encoding='utf-8-sig')