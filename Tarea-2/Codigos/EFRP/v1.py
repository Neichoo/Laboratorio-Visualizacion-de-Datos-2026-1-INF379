import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter, defaultdict
from matplotlib.patches import Rectangle
from matplotlib import transforms

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = 14
# =========================
# CARGAR CSV
# =========================

archivo = "../../data/Encuesta_videojuegos.csv"

df = pd.read_csv(archivo)
df = df.drop(columns=["Marca temporal"], errors="ignore")

# =========================
# FUNCIONES AUXILIARES
# =========================

def separar_valores(columna):
    valores = []

    for item in columna.dropna():
        separados = [x.strip() for x in str(item).split(",")]
        valores.append(separados)

    return valores


def escalar(valor, minimo, maximo, salida_min, salida_max):
    if maximo == minimo:
        return (salida_min + salida_max) / 2

    return salida_min + (valor - minimo) * (salida_max - salida_min) / (maximo - minimo)


# =====================================================
# DATOS
# =====================================================

col_genero = "¿Género favorito de videojuego?"
col_modalidad = "Qué modalidad de juego prefieres?"

lista_generos = separar_valores(df[col_genero])
lista_modalidades = separar_valores(df[col_modalidad])

relaciones = defaultdict(set)

conteo_generos = Counter()
conteo_modalidades_por_genero = Counter()
conteo_relaciones = Counter()

for generos, modalidades in zip(lista_generos, lista_modalidades):

    for genero in generos:
        conteo_generos[genero] += 1

        for modalidad in modalidades:
            relaciones[genero].add(modalidad)

            nodo_modalidad = f"{modalidad}_{genero}"

            conteo_modalidades_por_genero[nodo_modalidad] += 1
            conteo_relaciones[(genero, nodo_modalidad)] += 1

# =====================================================
# GRAFO
# =====================================================

G = nx.Graph()

for genero, modalidades in relaciones.items():

    G.add_node(genero, tipo="genero")

    for modalidad in modalidades:

        nodo_modalidad = f"{modalidad}_{genero}"

        G.add_node(
            nodo_modalidad,
            tipo="modalidad",
            label=modalidad
        )

        G.add_edge(
            genero,
            nodo_modalidad,
            peso=conteo_relaciones[(genero, nodo_modalidad)]
        )

# =====================================================
# SORT CÍRCULOS INTERNOS
# Géneros ordenados de mayor a menor frecuencia
# =====================================================

generos = sorted(
    relaciones.keys(),
    key=lambda g: conteo_generos[g],
    reverse=True
)

num_generos = len(generos)

# =====================================================
# POSICIONES RADIALES
# =====================================================

pos = {}

radio_generos = 4
radio_barras = 8

angulos_generos = np.linspace(
    0,
    2 * np.pi,
    num_generos,
    endpoint=False
)

for angulo, genero in zip(angulos_generos, generos):

    gx = radio_generos * np.cos(angulo)
    gy = radio_generos * np.sin(angulo)

    pos[genero] = (gx, gy)

sector_total = (2 * np.pi) / num_generos
margen_sector = sector_total * 0.15

angulos_modalidades = {}

# =====================================================
# SORT CÍRCULOS/BARRAS EXTERNAS
# Modalidades ordenadas de mayor a menor frecuencia
# dentro de cada género
# =====================================================

for angulo_genero, genero in zip(angulos_generos, generos):

    modalidades = sorted(
        relaciones[genero],
        key=lambda m: conteo_modalidades_por_genero[f"{m}_{genero}"],
        reverse=True
    )

    cantidad = len(modalidades)

    inicio_sector = (
        angulo_genero
        - (sector_total / 2)
        + margen_sector
    )

    fin_sector = (
        angulo_genero
        + (sector_total / 2)
        - margen_sector
    )

    if cantidad == 1:
        angulos_m = [angulo_genero]
    else:
        angulos_m = np.linspace(
            inicio_sector,
            fin_sector,
            cantidad
        )

    for angulo_m, modalidad in zip(angulos_m, modalidades):

        nodo_modalidad = f"{modalidad}_{genero}"

        bx = radio_barras * np.cos(angulo_m)
        by = radio_barras * np.sin(angulo_m)

        pos[nodo_modalidad] = (bx, by)
        angulos_modalidades[nodo_modalidad] = angulo_m

# =====================================================
# ESCALAS VISUALES
# =====================================================

conteos_generos = list(conteo_generos.values())
conteos_modalidades = list(conteo_modalidades_por_genero.values())

min_genero = min(conteos_generos)
max_genero = max(conteos_generos)

min_modalidad = min(conteos_modalidades)
max_modalidad = max(conteos_modalidades)

tamanos_generos = [
    escalar(
        conteo_generos[g],
        min_genero,
        max_genero,
        300,
        1800
    )
    for g in generos
]

# =====================================================
# DIBUJAR
# =====================================================

fig, ax = plt.subplots(figsize=(22, 22))

# -------------------------
# ARISTAS
# -------------------------

anchos_aristas = [
    escalar(
        G[u][v]["peso"],
        1,
        max(conteo_relaciones.values()),
        0.5,
        2.5
    )
    for u, v in G.edges()
]

nx.draw_networkx_edges(
    G,
    pos,
    ax=ax,
    width=anchos_aristas,
    alpha=0.25,
    edge_color="gray"
)

# -------------------------
# NODOS INTERNOS: GÉNEROS
# -------------------------

nx.draw_networkx_nodes(
    G,
    pos,
    ax=ax,
    nodelist=generos,
    node_size=tamanos_generos,
)

# =====================================================
# BARRAS EXTERNAS
# =====================================================

modalidades_nodos = [
    n for n in G.nodes
    if G.nodes[n]["tipo"] == "modalidad"
]

ancho_barra = 0.22
largo_min = 0.8
largo_max = 3.5

for nodo in modalidades_nodos:

    x, y = pos[nodo]

    angulo = angulos_modalidades[nodo]

    valor = conteo_modalidades_por_genero[nodo]

    largo_barra = escalar(
        valor,
        min_modalidad,
        max_modalidad,
        largo_min,
        largo_max
    )

    rect = Rectangle(
        (0, -ancho_barra / 2),
        largo_barra,
        ancho_barra,
        alpha=0.85
    )

    transformacion = (
        transforms.Affine2D()
        .rotate(angulo)
        .translate(x, y)
        + ax.transData
    )

    rect.set_transform(transformacion)
    ax.add_patch(rect)

# =====================================================
# ETIQUETAS INTERNAS
# =====================================================

for genero in generos:

    x, y = pos[genero]

    ax.text(
        x,
        y,
        f"{genero}\n({conteo_generos[genero]})",
        fontsize=8,
        ha="center",
        va="center",
        fontweight="bold"
    )

# =====================================================
# ETIQUETAS EXTERNAS
# =====================================================

for nodo in modalidades_nodos:

    label = G.nodes[nodo]["label"]
    valor = conteo_modalidades_por_genero[nodo]

    angulo = angulos_modalidades[nodo]
    angulo_grados = np.degrees(angulo)

    largo_barra = escalar(
        valor,
        min_modalidad,
        max_modalidad,
        largo_min,
        largo_max
    )

    distancia_texto = radio_barras + largo_barra + 0.35

    tx = distancia_texto * np.cos(angulo)
    ty = distancia_texto * np.sin(angulo)

    rotacion = angulo_grados

    if 90 < angulo_grados < 270:
        rotacion += 180
        alineacion = "right"
    else:
        alineacion = "left"

    ax.text(
        tx,
        ty,
        f"{label} ({valor})",
        fontsize=10,
        rotation=rotacion,
        rotation_mode="anchor",
        ha=alineacion,
        va="center"
    )

# =====================================================
# FINAL
# =====================================================

limite = radio_barras + largo_max + 3

ax.set_xlim(-limite, limite)
ax.set_ylim(-limite, limite)

ax.set_aspect("equal")
ax.axis("off")

plt.title(
    "Modalidad de juego preferida por género",
    fontsize=18,
    pad=30
)

plt.tight_layout()

plt.savefig(
    "v1.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()