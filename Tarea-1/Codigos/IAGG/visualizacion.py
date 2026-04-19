import colorsys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser" #Sin esto crasheaba

# ***** Funciones relacionadas al color ***** #
def convertir_color_a_rgb(color):
    color = color.strip()
    if color.startswith('rgb(') and color.endswith(')'):
        partes = color[4:-1].split(',')
        return tuple(int(float(p.strip())) for p in partes)
    if color.startswith('#'):
        color = color[1:]
    return int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)


def mezclar_con_blanco(color, intensidad):
    """intensidad: 1.0 = color puro, 0.0 = blanco"""
    r, g, b = convertir_color_a_rgb(color)
    intensidad = max(0.0, min(1.0, float(intensidad)))
    r_nuevo = int(255 - (255 - r) * intensidad)
    g_nuevo = int(255 - (255 - g) * intensidad)
    b_nuevo = int(255 - (255 - b) * intensidad)
    return f'rgb({r_nuevo},{g_nuevo},{b_nuevo})'

def generar_color_desde_hue(hue, saturacion=0.55, valor=0.90):
    r, g, b = colorsys.hsv_to_rgb(hue, saturacion, valor)
    return f'rgb({int(r*255)},{int(g*255)},{int(b*255)})'

def suavizar_color(color, mantener=0.86):
    return mezclar_con_blanco(color, mantener)

def construir_paleta_muchos_colores():
    colores_base = (
        px.colors.qualitative.Safe
        + px.colors.qualitative.Set2
        + px.colors.qualitative.Set3
        + px.colors.qualitative.Light24
    )
    colores_unicos = list(dict.fromkeys(colores_base))
    return [suavizar_color(c, mantener=0.86) for c in colores_unicos]

def asignar_colores_consolas(lista_consolas):
    paleta = construir_paleta_muchos_colores()
    mapa_colores = {}
    for i, consola in enumerate(lista_consolas):
        if i < len(paleta):
            mapa_colores[consola] = paleta[i]
        else:
            break
    if len(lista_consolas) > len(paleta):
        razon_aurea = 0.61803398875
        hue = 0.12
        for consola in lista_consolas[len(paleta):]:
            hue = (hue + razon_aurea) % 1.0
            mapa_colores[consola] = generar_color_desde_hue(hue)
    return mapa_colores

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
orden_consolas = list(totales_consola['console'])
mapa_colores = asignar_colores_consolas(orden_consolas)
ids, etiquetas, padres, valores, colores = [], [], [], [], []


# ***** Diagrama Sunburst ***** #
for _, fila in totales_consola.iterrows():
    consola = fila['console']
    ventas_consola = fila['total_sales']
    color_base = mapa_colores[consola]
    id_consola = f'consola::{consola}'
    ids.append(id_consola)
    etiquetas.append(consola)
    padres.append('')
    valores.append(ventas_consola)
    colores.append(mezclar_con_blanco(color_base, 0.98))
    generos = (
        df_sunburst[df_sunburst['console'] == consola]
        .sort_values('total_sales', ascending=False)
        .copy()
    )
    max_ventas_genero = generos['total_sales'].max()
    if pd.isna(max_ventas_genero) or max_ventas_genero <= 0:
        max_ventas_genero = 1.0
    for _, fila_genero in generos.iterrows():
        genero = fila_genero['genre']
        ventas_genero = fila_genero['total_sales']
        proporcion = ventas_genero / max_ventas_genero
        intensidad = 0.45 + 0.50 * proporcion
        id_genero = f'genero::{consola}::{genero}'
        ids.append(id_genero)
        etiquetas.append(genero)
        padres.append(id_consola)
        valores.append(ventas_genero)
        colores.append(mezclar_con_blanco(color_base, intensidad))

fig = go.Figure(
    go.Sunburst(
        ids=ids,
        labels=etiquetas,
        parents=padres,
        values=valores,
        branchvalues='total',
        marker=dict(colors=colores),
        textinfo="label+percent parent"
    )
)

fig.update_layout(
    title='Distribución de ventas de videojuegos por consola y género',
    annotations=[
        dict(
            text='Ventas en millones de unidades | Fuente: Video Game Sales 2024 - asaniczka',
            x=0.5,
            y=-0.1,
            showarrow=False,
            xref='paper',
            yref='paper'
        )
    ]
)

# Tamaño de fuente acordado (igual que en EFRP y MBHF)
fig.update_traces(
    domain=dict(x=[0.125, 0.875]),
    textfont_size=36
)

fig.show()