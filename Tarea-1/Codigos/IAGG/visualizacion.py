import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser" #Sin esto crasheaba

# Cargar datos
df = pd.read_csv("../../data/clean/vgchartz-2024-clean.csv")
TOP_N_CONSOLES = None
if TOP_N_CONSOLES is not None:
    top_consoles = df['console'].value_counts().head(TOP_N_CONSOLES).index
    df = df[df['console'].isin(top_consoles)]
df_grouped = df.groupby(['console', 'genre'], as_index=False)['total_sales'].sum()

# ***** Datos para el diagrama ***** #
df_sunburst = df_grouped.copy()
df_sunburst['total_sales'] = pd.to_numeric(
    df_sunburst['total_sales'], errors='coerce'
).fillna(0.0)
df_sunburst = df_sunburst[df_sunburst['total_sales'] > 0]
totales_consola = (
    df_sunburst.groupby('console', as_index=False)['total_sales']
    .sum()
    .sort_values('total_sales', ascending=False)
    .reset_index(drop=True)
)
ids, etiquetas, padres, valores = [], [], [], []

# ***** Diagrama Sunburst ***** #
for _, fila in totales_consola.iterrows():
    consola = fila['console']
    ventas_consola = fila['total_sales']
    id_consola = f'consola::{consola}'
    ids.append(id_consola)
    etiquetas.append(consola)
    padres.append('')
    valores.append(ventas_consola)
    generos = (
        df_sunburst[df_sunburst['console'] == consola]
        .sort_values('total_sales', ascending=False)
        .copy()
    )
    for _, fila_genero in generos.iterrows():
        genero = fila_genero['genre']
        ventas_genero = fila_genero['total_sales']
        id_genero = f'genero::{consola}::{genero}'
        ids.append(id_genero)
        etiquetas.append(genero)
        padres.append(id_consola)
        valores.append(ventas_genero)
fig = go.Figure(
    go.Sunburst(
        ids=ids,
        labels=etiquetas,
        parents=padres,
        values=valores,
        branchvalues='total',
        textinfo="label+percent parent"
    )
)

# Ajuste de fuente y tamaño
fig.update_layout(
    title=dict(
        text='Distribución de ventas de videojuegos por consola y género',
        font=dict(size=24)
    ),
    font=dict(family='Arial'),
    annotations=[
        dict(
            text='Ventas en millones de unidades | Fuente: Video Game Sales 2024 - asaniczka',
            x=0.5,
            y=-0.1,
            font=dict(size=11),
            showarrow=False,
            xref='paper',
            yref='paper'
        )
    ]
)
fig.update_traces(
    textfont_size=14
)
fig.show()