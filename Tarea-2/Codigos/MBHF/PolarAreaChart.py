import pandas as pd
import plotly.express as px

cols = [
    '¿Plataformas de Juego Favorita?',
    'Qué modalidad de juego prefieres?'
]

df = pd.read_csv("../../data/Encuesta_videojuegos.csv", usecols=cols)

df = df.dropna()

df['¿Plataformas de Juego Favorita?'] = (
    df['¿Plataformas de Juego Favorita?'].astype(str)
)

df['Qué modalidad de juego prefieres?'] = (
    df['Qué modalidad de juego prefieres?'].astype(str)
)

df['Plataformas'] = (
    df['¿Plataformas de Juego Favorita?']
    .str.split(', ')
)

df['Modalidad'] = (
    df['Qué modalidad de juego prefieres?']
    .str.split(', ')
)

rows = []

for plataformas, modalidades in zip(df['Plataformas'], df['Modalidad']):

    if not isinstance(plataformas, list):
        continue

    if not isinstance(modalidades, list):
        continue

    for p in plataformas:
        for m in modalidades:
            rows.append((p.strip(), m.strip()))

count_df = (
    pd.DataFrame(rows, columns=['Plataformas', 'Modalidad'])
    .value_counts()
    .reset_index(name='count')
)

top_plataformas = (
    count_df.groupby('Plataformas')['count']
    .sum()
    .sort_values(ascending=False)
    .head(8)
    .index
)

count_df = count_df[
    count_df['Plataformas'].isin(top_plataformas)
]

fig = px.bar_polar(
    count_df,
    r='count',
    theta='Plataformas',
    color='Modalidad',
    template='plotly_dark',
    category_orders={
        'Plataformas': list(top_plataformas)
    },
    color_discrete_sequence=px.colors.qualitative.Bold
)

fig.update_layout(
    title='Modalidades de Juego por Plataforma',
    width=1000,
    height=800,
    font_size=14,
    legend_title='Modalidad',
    polar=dict(
        radialaxis=dict(
            showticklabels=True,
            ticks='outside'
        )
    )
)

fig.show()