import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter, defaultdict
from matplotlib.patches import Circle
import math

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = 14
# =========================
# CARGAR CSV
# =========================

archivo = "../../data/Encuesta_videojuegos.csv"

df = pd.read_csv(archivo)
df = df.drop(columns=["Marca temporal"], errors="ignore")

# =========================
# FUNCION AUXILIAR
# =========================

def separar_valores(columna):

    valores = []

    for item in columna.dropna():

        separados = [
            x.strip()
            for x in str(item).split(",")
        ]

        valores.append(separados)

    return valores

# =====================================================
# DATOS
# =====================================================

col_genero = "¿Género favorito de videojuego?"
col_aspecto = "¿Aspecto que valoras más en un videojuego?"

lista_generos = separar_valores(df[col_genero])
lista_aspectos = separar_valores(df[col_aspecto])

# =====================================================
# CONTAR ASPECTOS POR GÉNERO
# =====================================================

conteo_genero_aspecto = defaultdict(Counter)

for generos, aspectos in zip(
    lista_generos,
    lista_aspectos
):

    for genero in generos:

        for aspecto in aspectos:

            conteo_genero_aspecto[genero][aspecto] += 1

# =====================================================
# FIGURA
# =====================================================

fig, ax = plt.subplots(figsize=(24, 18))

# =====================================================
# CALCULAR RADIOS SEGÚN FRECUENCIA
# =====================================================

generos = list(conteo_genero_aspecto.keys())

radios_generos = {}

for genero in generos:

    aspectos = conteo_genero_aspecto[genero]

    total = sum(aspectos.values())

    # ---------------------------------
    # RADIO PROPORCIONAL A FRECUENCIA
    # usando sqrt para mejor percepción visual
    # ---------------------------------

    radio_principal = max(
        3.5,
        min(
            9.0,
            math.sqrt(total) * 0.9
        )
    )

    radios_generos[genero] = radio_principal

# =====================================================
# ORDENAR POR TAMAÑO
# =====================================================

generos.sort(
    key=lambda g: radios_generos[g],
    reverse=True
)

# =====================================================
# DISTRIBUCIÓN EN GRILLA
# =====================================================

n = len(generos)

columnas = int(np.ceil(np.sqrt(n)))
filas = int(np.ceil(n / columnas))

espaciado_x = 22
espaciado_y = 22

posiciones = {}

for idx, genero in enumerate(generos):

    fila = idx // columnas
    columna = idx % columnas

    x = columna * espaciado_x
    y = -fila * espaciado_y

    posiciones[genero] = (x, y)

# =====================================================
# CENTRAR GRILLA
# =====================================================

ancho_total = (columnas - 1) * espaciado_x
alto_total = (filas - 1) * espaciado_y

for genero in posiciones:

    x, y = posiciones[genero]

    posiciones[genero] = (
        x - ancho_total / 2,
        y + alto_total / 2
    )

# =====================================================
# DIBUJAR CADA GÉNERO
# =====================================================

for genero in generos:

    x, y = posiciones[genero]

    aspectos = conteo_genero_aspecto[genero]

    top_aspectos = aspectos.most_common(10)

    total = sum(aspectos.values())

    radio_principal = radios_generos[genero]

    # =================================================
    # CÍRCULO PRINCIPAL
    # =================================================

    circulo_principal = Circle(
        (x, y),
        radio_principal,
        alpha=0.75
    )

    ax.add_patch(circulo_principal)

    # =================================================
    # TÍTULO DEL GÉNERO
    # =================================================

    ax.text(
        x,
        y + radio_principal + 1.5,
        genero.upper(),
        ha="center",
        va="center",
        fontsize=15,
        weight="bold"
    )

    # =================================================
    # ASPECTO CENTRAL
    # =================================================

    if len(top_aspectos) == 0:
        continue

    aspecto_central, valor_central = top_aspectos[0]

    radio_central = max(
        0.9,
        min(
            2.8,
            math.sqrt(valor_central) * 0.45
        )
    )

    circulo_central = Circle(
        (x, y),
        radio_central,
        alpha=0.50
    )

    ax.add_patch(circulo_central)

    texto_central = aspecto_central

    if len(texto_central) > 14:

        texto_central = (
            texto_central[:12] + "..."
        )

    ax.text(
        x,
        y,
        f"{texto_central}\n{valor_central}",
        ha="center",
        va="center",
        fontsize=10,
        weight="bold"
    )

    # =================================================
    # ASPECTOS SECUNDARIOS
    # =================================================

    restantes = top_aspectos[1:]

    cantidad_restantes = len(restantes)

    if cantidad_restantes > 0:

        angulos_internos = np.linspace(
            0,
            2 * np.pi,
            cantidad_restantes,
            endpoint=False
        )

        radio_interno = (
            radio_principal * 0.65
        )

        for ang_i, (aspecto, valor) in zip(
            angulos_internos,
            restantes
        ):

            ix = (
                x
                + radio_interno * np.cos(ang_i)
            )

            iy = (
                y
                + radio_interno * np.sin(ang_i)
            )

            # ---------------------------------
            # RADIO SEGÚN FRECUENCIA
            # ---------------------------------

            radio_aspecto = max(
                0.6,
                min(
                    2.2,
                    math.sqrt(valor) * 0.38
                )
            )

            circulo_aspecto = Circle(
                (ix, iy),
                radio_aspecto,
                alpha=0.35
            )

            ax.add_patch(circulo_aspecto)

            texto = aspecto

            if len(texto) > 10:

                texto = texto[:8] + "..."

            ax.text(
                ix,
                iy,
                f"{texto}\n{valor}",
                ha="center",
                va="center",
                fontsize=11
            )

# =====================================================
# AJUSTES FINALES
# =====================================================

margen = 14

x_min = (
    min(x for x, y in posiciones.values())
    - margen
)

x_max = (
    max(x for x, y in posiciones.values())
    + margen
)

y_min = (
    min(y for x, y in posiciones.values())
    - margen
)

y_max = (
    max(y for x, y in posiciones.values())
    + margen
)

ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

ax.set_aspect("equal")

plt.title(
    "Aspectos más valorados por género",
    fontsize=22,
    pad=30
)

plt.axis("off")

plt.tight_layout()

plt.savefig(
    "v2.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()