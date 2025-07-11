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
    if dfDist.empty:
        return None
    if dfDist['Porcentaje'].sum() == 0:
        return None
    colores = {'FF': '#001219', 'Sinker': '#005F73', 'Cutter': '#0A9396', 'Slider': '#94D2BD',
               'ChangeUp': '#E9D8A6', 'Splitter': '#EE9B00', 'Curveball': '#CA6702', 'Fastball': '#BB3E03',
               'Sweeper': '#9B2226'}
    dfDist = dfDist[dfDist['Porcentaje'] > 0].reset_index(drop=True)
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
        startangle=90,
        colors=dfDist['Tipo lanzamiento'].map(colores).to_list(),
        wedgeprops=dict(width=0.3),
        radius=0.7,
        pctdistance=1.4,
        labels=None
    )
    ax1.text(
        0, 0,
        dfDist['Total'].sum(),
        ha='center', va='center',
        fontsize=12, weight='bold'
    )
    ax1.legend(
        plot[0], 
        [f"{l} ({p:.1f}%)" for l, p in zip(dfDist['Tipo lanzamiento'], dfDist['Porcentaje'])],
        loc="lower center",
        ncol=2,
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
            if len(dfPos[dfPos['TaggedPitchType'] == tipo]) > 5:
                sns.kdeplot(
                    data=dfPos[dfPos['TaggedPitchType'] == tipo],
                    x=-dfPos['PlateLocSide'],
                    y='PlateLocHeight',
                    color='red',
                    fill=True
                )
            sns.scatterplot(
                data=dfPos[dfPos['TaggedPitchType'] == tipo],
                x=-dfPos['PlateLocSide'],
                y='PlateLocHeight'
            )
            ax.set_title(tipo, fontsize=12, y=-0.1)

    fig.suptitle(titulo, fontsize=16, y=0.95, x=0.2)
    fig.subplots_adjust(left=0.05, right=0.95, bottom=0.03, top=0.9)

    plt.close()
    return fig

def graficarSituacionPitcher(df, total, titulo):
    colores = {'Ponche': '#001219', 'Base por bolas': '#005F73', 'Base por golpe': '#0A9396', 
               'Hit': '#94D2BD', 'Out': '#E9D8A6', 'Error': '#EE9B00', 'Bola ocupada': '#CA6702', 
               'Sacrificio': '#BB3E03', 'Otro': '#9B2226'}
    fig, ax = plt.subplots(figsize=(3, 3))
    plot = ax.pie(
        df['Porcentaje'], 
        startangle=90,
        colors=df['index'].map(colores).to_list(),
        wedgeprops=dict(width=0.3),
        radius=0.7,
        pctdistance=1.4,
        labels=None
    )
    ax.text(
        0, 0,
        total,
        ha='center', va='center',
        fontsize=12, weight='bold'
    )
    ax.legend(
        plot[0], 
        [f"{l} ({p:.1f}%)" for l, p in zip(df['index'], df['Porcentaje'])],
        loc="lower center",
        ncol=2,
        frameon=False,
        fontsize='small'
    )

    fig.suptitle(titulo, fontsize=16, y=0.95, x=0.2)
    plt.subplots_adjust(left=0.3)

    plt.close()

    return fig

def graficarCampo(ax=None, rightField=325, centerField = 400, leftField=325):
    if ax is None:
        fig, ax = plt.subplots(figsize=(5, 6))
    firstBaseX = 90 * np.cos(np.radians(45))
    firstBaseY = 90 * np.sin(np.radians(45))
    secondBaseY = np.sqrt(2*(90**2))
    thirdBaseX = -firstBaseX
    thirdBaseY = firstBaseY
    x = [0, firstBaseX, 0, thirdBaseX, 0]
    y = [0, firstBaseY, secondBaseY, thirdBaseY, 0]
    rightFieldX = rightField * np.cos(np.radians(45))
    righttFieldY = rightField * np.sin(np.radians(45))
    leftFieldX = leftField * np.cos(np.radians(135))
    leftFieldY = leftField * np.sin(np.radians(135))
    
    
    plt.plot(x, y, color='black', lw=2, marker=(4, 0, 90), markersize=10)
    plt.plot([0, rightFieldX], [0, righttFieldY], color='black', lw=2)
    plt.plot([0, leftFieldX], [0, leftFieldY], color='black', lw=2)

    curva = np.poly1d(np.polyfit([leftFieldX, 0, rightFieldX], [leftFieldY, centerField, righttFieldY], 2))
    x_curve = np.linspace(leftFieldX, rightFieldX, 100)
    y_curve = curva(x_curve)
    plt.plot(x_curve, y_curve, color='black', lw=2)

    ylim = centerField * 1.2
    xlim = (ylim + 10) / 2
    ax.set_xlim(-xlim, xlim)
    ax.set_ylim(-10, ylim)

    sns.set_style('white')
    sns.despine(right=True, top=True, left=True, bottom=True)
    ax.set_xticks([])
    ax.set_yticks([])
    return ax

def getZonaPitcheo(x, y, sz_top=3.5, sz_bot=1.5):
    sz_right = 0.708
    sz_left = -sz_right
    sz_midle = (sz_top - sz_bot) / 2 + sz_bot
    hor_delta = (sz_right * 2) / 3
    vert_delta = (sz_top - sz_bot) / 3

    if ((y >= sz_top and x < 0) or (y >= sz_midle and x < sz_left)): return 11
    if ((y >= sz_top and x >= 0) or (y >= sz_midle and x >= sz_right)): return 12
    if ((y < sz_bot and x < 0) or (y < sz_midle and x < sz_left)): return 13
    if ((y < sz_bot and x >= 0) or (y < sz_midle and x >= sz_right)): return 14

    if (y >= (sz_top - vert_delta)): zona = 0
    elif (y >= (sz_bot + vert_delta)): zona = 3
    else: zona = 6

    if (x < (sz_left + hor_delta)): zona += 1
    elif (x < (sz_right - hor_delta)): zona += 2
    else: zona += 3
    return zona

def leerDatos(rutaTrackman, rutaBateadores, rutaPitchers):
    df = pd.read_csv(rutaTrackman, sep=',', encoding='utf-8')
    df['Pitcher'] = df['Pitcher'].str.split(', ').apply(lambda x: x[1] + ' ' + x[0])
    df['Batter'] = df['Batter'].str.split(', ').apply(lambda x: x[1] + ' ' + x[0])
    df['TaggedPitchType'] = df['TaggedPitchType'].str.replace('FourSeamFastBall', 'FF', regex=True)
    df['HomeScore'] = np.where(df['Top/Bottom'] == 'Bottom', df['RunsScored'], 0)
    df['AwayScore'] = np.where(df['Top/Bottom'] == 'Top', df['RunsScored'], 0)
    df['HomeScore'] = df['HomeScore'].cumsum().shift(1).fillna(0)
    df['AwayScore'] = df['AwayScore'].cumsum().shift(1).fillna(0)
    df['RunDif'] = np.where(df['Top/Bottom'] == 'Top', df['HomeScore'] - df['AwayScore'], df['AwayScore'] - df['HomeScore'])
    df['PitchZone'] = df.apply(lambda row: getZonaPitcheo(row['PlateLocSide'], row['PlateLocHeight']), axis=1).astype('Int64')
    df['PAResult'] = np.where(
        df['KorBB'] == 'Strikeout', 'Ponche',
        np.where(df['KorBB'] == 'Walk', 'Base por bolas',
        np.where(df['PitchCall'] == 'HitByPitch', 'Base por golpe', 
        np.where((df['PlayResult'] == 'Single') |
                (df['PlayResult'] == 'Double') |
                (df['PlayResult'] == 'Triple') |
                (df['PlayResult'] == 'HomeRun'), 'Hit',
        np.where(df['PlayResult'] == 'Out', 'Out',
        np.where(df['PlayResult'] == 'Error', 'Error', 
        np.where(df['PlayResult'] == 'FieldersChoice', 'Bola ocupada', 
        np.where(df['PlayResult'] == 'Sacrifice', 'Sacrificio', pd.NA)
        ))))))
    )
    df['PAResult'] = df.groupby(['Inning', 'Top/Bottom', 'PAofInning'])['PAResult'].transform('last')

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

def saveLineUp(bateadores, rutaCSV, name):
    bateadores[['Bateador', 'Position', 'seasonAVG', 'seasonOPS']].rename(
        columns={'Bateador': 'Nombre', 'Position': 'Posición', 'seasonAVG': 'AVG', 'seasonOPS': 'OPS'}
    ).to_csv(f'{rutaCSV}/lineUp/{name}LineUp.csv', index=False, encoding='utf-8-sig')

def savePitchers(pitchers, atBats, rutaCSV, name):
    ordenColumnas = ['Nombre', 'Entrada de inicio', 'Entradas lanzadas', 'ERA']
    pd.merge(
        pitchers[['Pitcher', 'InningsPitch', 'seasonERA']], atBats.groupby('Pitcher')['Inning'].min(),
        on='Pitcher'
    ).rename(
        columns={'Pitcher': 'Nombre', 'Inning': 'Entrada de inicio', 'InningsPitch':'Entradas lanzadas', 'seasonERA': 'ERA'}
    )[ordenColumnas].to_csv(f'{rutaCSV}/pitchers/{name}Pitchers.csv', index=False, encoding='utf-8-sig')

def getLineaPitcheo(pitchers, atBats):
    lineaPitcheo = pd.merge(
        pitchers[['Team', 'Pitcher', 'BattersFaced', 'InningsPitch', 'runs', 'earnedRuns']],
        atBats.groupby(['Pitcher', 'BatterSide']).agg(
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

    return lineaPitcheo

def saveLineaPitcheo(lineaPitcheo, rutaCSV):
    temp = lineaPitcheo.groupby('Nombre').agg({
            'No lanzamientos': 'sum', 
            'Bateadores enfrentados': 'min',
            'Entrada de inicio': 'min',
            'Entradas lanzadas': 'min',
            'Strikes': 'sum',
            'Strikes con swing': 'sum',
            'Bolas': 'sum',
            'Ponches': 'sum',
            'Bases por bolas': 'sum',
            'Carreras': 'min',
            'Carreras limpias': 'min'
        })
    for index, row in temp.iterrows():
        row.to_frame().T.to_csv(f'{rutaCSV}/lineaPitcheo/linea{index}.csv', encoding='utf-8-sig')

def getDistribucionLanzamientos(lineaPitcheo, atBats):
    distribucionLanzamientos = pd.merge(
        lineaPitcheo[['Team', 'Nombre', 'BatterSide', 'No lanzamientos', 'Strikes', 'Strikes con swing', 'Bolas', 'Ponches', 'Bases por bolas']],
        atBats.groupby(['Pitcher', 'BatterSide', 'TaggedPitchType']).agg(
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
    distribucionLanzamientos = distribucionLanzamientos.fillna(0)

    return distribucionLanzamientos

def saveDistribucionLanzamientos(distribucionLanzamientos, atBats, rutaCSV, rutaIMG):
    columnas = ['Tipo lanzamiento', 'Uso', 'Porcentaje de uso', 'Velocidad maxima', 'Velocidad promedio', 
                'Strikes %', 'Swing Strikes %', 'Bolas %', 'Ponches %']
    
    pitchers = distribucionLanzamientos['Nombre'].unique().tolist()

    for pitcher in pitchers:
        lados = distribucionLanzamientos[distribucionLanzamientos['Nombre'] == pitcher]['BatterSide'].unique().tolist()
        for lado in lados:
            nombre = pitcher.replace(' ', '').replace('.', '').strip()
            if lado == 'Total':
                subRuta = '/distribucionPitcheo/total/distribucion{0}{1}'
                titulo = 'Distribución de {0}'
                dfPos = atBats[(atBats['Pitcher'] == pitcher)]
            elif lado == 'Left':
                subRuta = '/distribucionPitcheo/left/distribucionVsZurdos{0}{1}'
                titulo = 'Distribución de {0} vs bateadores izquierdos'
                dfPos = atBats[(atBats['Pitcher'] == pitcher) & (atBats['BatterSide'] == 'Left')]
            else:
                subRuta = '/distribucionPitcheo/right/distribucionVsDerechos{0}{1}'
                titulo = 'Distribución de {0} vs bateadores derechos'
                dfPos = atBats[(atBats['Pitcher'] == pitcher) & (atBats['BatterSide'] == 'Right')]

            df = distribucionLanzamientos[
                (distribucionLanzamientos['Nombre'] == pitcher) &
                (distribucionLanzamientos['BatterSide'] == lado)
            ].sort_values(by='Uso', ascending=False).reset_index(drop=True)
            df[columnas].to_csv(f'{rutaCSV}{subRuta.format('', nombre)}.csv', index=False, encoding='utf-8-sig')

            distribucionImg = graficarDistribucionLanzamientos(
                dfDist=df.rename(columns={'Porcentaje de uso': 'Porcentaje', 'Uso': 'Total'}),
                dfPos=dfPos,
                titulo=titulo.format('Lanzamientos')
            )
            if distribucionImg is not None:
                distribucionImg.savefig(f'{rutaIMG}{subRuta.format('', nombre)}.png', bbox_inches='tight', dpi=300)

            distribucionStrikesImg = graficarDistribucionLanzamientos(
                dfDist=df.rename(columns={'Strikes %': 'Porcentaje', 'StrikesPorTipo': 'Total'}),
                dfPos=dfPos[(dfPos['PitchCall'].str.startswith('Strike')) |
                            (dfPos['PitchCall'].str.startswith('FoulBall')) |
                            (dfPos['PitchCall'].str.startswith('InPlay'))],
                titulo=titulo.format('Strikes')
            )
            if distribucionStrikesImg is not None:
                distribucionStrikesImg.savefig(f'{rutaIMG}{subRuta.format('Strikes', nombre)}.png', bbox_inches='tight', dpi=300)

            distribucionPonchesImg = graficarDistribucionLanzamientos(
                dfDist=df.rename(columns={'Ponches %': 'Porcentaje', 'PonchesPorTipo': 'Total'}),
                dfPos=dfPos[dfPos['KorBB'].str.startswith('Strikeout')],
                titulo=titulo.format('Ponches')
            )
            if distribucionPonchesImg is not None:
                distribucionPonchesImg.savefig(f'{rutaIMG}{subRuta.format('Ponches', nombre)}.png', bbox_inches='tight', dpi=300)

            distribucionBolasImg = graficarDistribucionLanzamientos(
                dfDist=df.rename(columns={'Bolas %': 'Porcentaje', 'BolasPorTipo': 'Total'}),
                dfPos=dfPos[dfPos['PitchCall'].str.startswith('Ball')],
                titulo=titulo.format('Bolas')
            )
            if distribucionBolasImg is not None:
                distribucionBolasImg.savefig(f'{rutaIMG}{subRuta.format('Bolas', nombre)}.png', bbox_inches='tight', dpi=300)

def getSituacionPitcher(atBats, tipo):
    if tipo == 'Riesgo':
        bolas = 3
        strikes = 0
    else:
        bolas = 0
        strikes = 2
    resultadoSituacionPitcher = atBats[(atBats['Balls'] == bolas) & (atBats['Strikes'] == strikes)][['Inning', 'PAofInning', 'Pitcher', 'PAResult']]
    resultadoSituacionPitcher = resultadoSituacionPitcher.groupby(['Inning', 'PAofInning']).last()

    resultadoSituacionPitcher = pd.get_dummies(resultadoSituacionPitcher, columns=['PAResult'], dtype=int)
    resultadoSituacionPitcher['Total'] = resultadoSituacionPitcher.groupby(['Pitcher'])['Pitcher'].transform('count')
    resultadoSituacionPitcher = resultadoSituacionPitcher.groupby('Pitcher').apply(lambda x: round(x.mean()*100, 1)).reset_index()
    resultadoSituacionPitcher['Total'] = resultadoSituacionPitcher['Total']/100
    newColumns = [x.replace('PAResult_', '') for x in resultadoSituacionPitcher.columns]
    resultadoSituacionPitcher = resultadoSituacionPitcher.rename(columns=dict(zip(resultadoSituacionPitcher.columns, newColumns)))

    return resultadoSituacionPitcher

def saveSituacionPitcher(situacion, rutaIMG, tipo):
    pitchers = situacion['Pitcher'].unique().tolist()
    for pitcher in pitchers:
        nombre = pitcher.replace(' ', '').replace('.', '').strip()
        subRuta = f'/situacion{tipo}/situacion{tipo}{nombre}.png'
        titulo = f'Control situaciones de {tipo}'
        temp = situacion[situacion['Pitcher'] == pitcher].reset_index(drop=True)
        total = int(temp['Total'].to_numpy()[0])
        temp = temp.drop(columns=['Total', 'Pitcher']).T.rename(columns={0: 'Porcentaje'})
        temp = temp[temp['Porcentaje'] > 0].reset_index()

        fig = graficarSituacionPitcher(temp, total, titulo)
        fig.savefig(f'{rutaIMG}{subRuta}', bbox_inches='tight', dpi=300)

def saveSecuenciaPitcheo(atBats, bateadores, rutaCSV, Npitches=6):
    secuenciaPitcheos = pd.merge(
        atBats[atBats['PitchofPA'] <= Npitches][
            ['Inning', 'PAofInning', 'PitchofPA', 'Pitcher', 'Batter', 'BatterSide', 'RunDif', 
            'TaggedPitchType', 'PitchZone', 'PAResult', 'PitchCall']],
        bateadores[['Bateador', 'seasonAVG']].rename(columns={'Bateador': 'Batter'}),
        on='Batter', how='left'
    )

    secuenciaPitcheos['PitchInfo'] = secuenciaPitcheos['TaggedPitchType'] + ' ' + secuenciaPitcheos['PitchZone'].astype(str)
    secuenciaPitcheos['PitchInfo'] = secuenciaPitcheos['PitchInfo'] + np.where(
        secuenciaPitcheos['PitchCall'].str.startswith('Strike'), ': Strike',
        np.where(secuenciaPitcheos['PitchCall'].str.startswith('Ball'), ': Bola', 
        np.where(secuenciaPitcheos['PitchCall'].str.startswith('Foul'), ': Foul',''
        )))

    secuenciaPitcheos = secuenciaPitcheos.pivot_table(
        index=['Inning', 'PAofInning', 'Pitcher', 'Batter', 'BatterSide', 'seasonAVG', 'RunDif', 'PAResult'],
        columns='PitchofPA',
        values='PitchInfo',
        aggfunc='last'
    ).sort_values(by=['Inning', 'PAofInning']).reset_index().drop(columns=['Inning', 'PAofInning'])
    pitchNo = [str(i) for i in range(1, Npitches + 1)]
    secuenciaPitcheos.columns = ['Pitcher', 'Batter', 'BatterSide', 'seasonAVG', 'RunDif', 'PAResult'] + pitchNo
    secuenciaPitcheos = secuenciaPitcheos[
        ['Pitcher', 'Batter', 'BatterSide', 'seasonAVG', 'RunDif', 'PAResult'] + pitchNo
    ].sort_values(by=['BatterSide', 'seasonAVG']).reset_index(drop=True).rename(
        columns={'Batter': 'Bateador', 'seasonAVG': 'AVG', 
                 'RunDif': 'Diferencia de carreras', 'PAResult': 'Resultado del turno'}
    )

    pitchers = secuenciaPitcheos['Pitcher'].unique().tolist()
    subruta = '/secuenciaPitcheo/{0}/secuencia{1}Vs{2}.csv'
    for pitcher in pitchers:
        nombre = pitcher.replace(' ', '').replace('.', '').strip()
        secuenciaPitcheos[(secuenciaPitcheos['Pitcher'] == pitcher) & 
                          (secuenciaPitcheos['BatterSide'] == 'Left')
                         ].drop(columns=['Pitcher', 'BatterSide']
                                ).to_csv(f'{rutaCSV}{subruta.format('left', nombre, 'Zurdos')}', index=False, encoding='utf-8-sig')
        secuenciaPitcheos[(secuenciaPitcheos['Pitcher'] == pitcher) &
                          (secuenciaPitcheos['BatterSide'] == 'Right')
                         ].drop(columns=['Pitcher', 'BatterSide']
                                ).to_csv(f'{rutaCSV}{subruta.format('right', nombre, 'Derechos')}', index=False, encoding='utf-8-sig')

if __name__ == '__main__':
    rutaTrackman = 'data/20250617-EstadioAlfredo-1.csv'
    rutaBateadores = 'data/bateadores.csv'
    rutaPitchers = 'data/pitchers.csv'
    rutaCSV = 'reporte/csv'
    rutaIMG = 'reporte/img'

    atBats, pitchers, bateadores = leerDatos(rutaTrackman, rutaBateadores, rutaPitchers)

    #saveLineUp(bateadores['home'], rutaCSV, 'home')
    #saveLineUp(bateadores['away'], rutaCSV, 'away')

    #savePitchers(pitchers['home'], atBats['away'], rutaCSV, 'home')
    #savePitchers(pitchers['away'], atBats['home'], rutaCSV, 'away')

    lineaPitcheo = {}
    lineaPitcheo['home'] = getLineaPitcheo(pitchers['home'], atBats['away'])
    lineaPitcheo['away'] = getLineaPitcheo(pitchers['away'], atBats['home'])
    #saveLineaPitcheo(lineaPitcheo['home'], rutaCSV)
    #saveLineaPitcheo(lineaPitcheo['away'], rutaCSV)

    distribucionLanzamientos = {}
    distribucionLanzamientos['home'] = getDistribucionLanzamientos(lineaPitcheo['home'], atBats['away'])
    distribucionLanzamientos['away'] = getDistribucionLanzamientos(lineaPitcheo['away'], atBats['home'])
    #saveDistribucionLanzamientos(distribucionLanzamientos['home'], atBats['away'], rutaCSV, rutaIMG)
    #saveDistribucionLanzamientos(distribucionLanzamientos['away'], atBats['home'], rutaCSV, rutaIMG)

    situacionRiesgo = {}
    situacionRiesgo['home'] = getSituacionPitcher(atBats['away'], 'Riesgo')
    situacionRiesgo['away'] = getSituacionPitcher(atBats['home'], 'Riesgo')
    #saveSituacionPitcher(situacionRiesgo['home'], rutaIMG, 'Riesgo')
    #saveSituacionPitcher(situacionRiesgo['away'], rutaIMG, 'Riesgo')

    situacionVentaja = {}
    situacionVentaja['home'] = getSituacionPitcher(atBats['away'], 'Ventaja')
    situacionVentaja['away'] = getSituacionPitcher(atBats['home'], 'Ventaja')
    #saveSituacionPitcher(situacionVentaja['home'], rutaIMG, 'Ventaja')
    #saveSituacionPitcher(situacionVentaja['away'], rutaIMG, 'Ventaja')

    #saveSecuenciaPitcheo(atBats['home'], bateadores['home'], rutaCSV)
    #saveSecuenciaPitcheo(atBats['away'], bateadores['away'], rutaCSV)
                                                          