import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# 1. Configuración de fuente y estilo unificado
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['font.size'] = 12

# 2. Cargar y procesar datos
csv_path = "../../data/clean/videojuegos_final.csv"
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"No se encontró el archivo {csv_path}")

df = pd.read_csv(csv_path)

# Convertir Critic Score a numérico y eliminar nulos
df['critic_score'] = pd.to_numeric(df['critic_score'], errors='coerce')
df_clean = df.dropna(subset=['console', 'critic_score'])

# Las 5 consolas más vendidas
consolas_top = ['X360', 'PS3', 'PS2', 'PS4', 'Wii']
df_filtered = df_clean[df_clean['console'].isin(consolas_top)]

# Calcular medias individuales
medias_consolas = df_filtered.groupby('console')['critic_score'].mean().to_dict()
global_mean = df_clean['critic_score'].mean()

print("Medias por consola:")
for c, m in medias_consolas.items():
    print(f"  {c}: {m:.2f}")
print(f"Media global: {global_mean:.2f}")

# 3. Preparar la figura con fondo blanco
fig, ax = plt.subplots(figsize=(11, 7), facecolor='#FFFFFF')
ax.set_facecolor('#FFFFFF')

# Colores de identidad de consolas de alto contraste
colors_dict = {
    'X360': '#107C10',  # verde Xbox
    'PS3': '#1A1A1A',   # negro carbón
    'PS2': '#002FA7',   # azul oscuro
    'PS4': '#006FCD',   # azul PlayStation
    'Wii': '#EAF0F6'    # blanco azulado
}

# Configuración del Ridgeline
x_eval = np.linspace(2, 10, 500) # Rango de evaluación del critic score
offset = 0.7  # Distancia vertical entre líneas base
scale = 0.5   # Escala de la altura de la densidad

# Iterar sobre las consolas en orden inverso para que las de arriba se dibujen primero/detrás
for i, console in enumerate(reversed(consolas_top)):
    data = df_filtered[df_filtered['console'] == console]['critic_score'].values
    
    # Estimar densidad de kernel (KDE)
    kde = gaussian_kde(data)
    y_dens = kde(x_eval) * scale
    
    # Línea base vertical
    y_base = i * offset
    
    # Colores para la consola
    color = colors_dict[console]
    # Si es Wii, usamos un color de línea más oscuro (blanco-azulado oscuro) para visibilidad sobre fondo blanco
    line_color = '#94AABF' if console == 'Wii' else color
    fill_color = color
    
    # Graficar la curva de contorno
    ax.plot(x_eval, y_base + y_dens, color=line_color, linewidth=1.8, zorder=i+10)
    
    # Rellenar el área bajo la curva. Usamos alpha=0.6 para Wii para que sea visible, y alpha=0.45 para el resto
    fill_alpha = 0.6 if console == 'Wii' else 0.45
    ax.fill_between(
        x_eval,
        y_base,
        y_base + y_dens,
        facecolor=fill_color,
        edgecolor='none',
        alpha=fill_alpha,
        zorder=i+5
    )
    
    # Línea base de soporte
    ax.axhline(y_base, xmin=0.02, xmax=0.98, color='#CBD5E1', linewidth=1, linestyle='-', zorder=i)
    
    # Dibujar indicador de la media de la consola (usamos line_color para Wii para visibilidad)
    mean_val = medias_consolas[console]
    mean_density = kde(mean_val)[0] * scale
    ax.vlines(
        x=mean_val,
        ymin=y_base,
        ymax=y_base + mean_density,
        color=line_color,
        linewidth=2.5,
        linestyle='--',
        zorder=i+12
    )
    
    # Etiqueta del promedio en formato de texto (Negro #000000)
    ax.text(
        mean_val,
        y_base + mean_density + 0.03,
        f"Med: {mean_val:.2f}",
        fontsize=10.5,
        color='#000000',
        fontweight='bold',
        ha='center',
        va='bottom',
        family='Arial',
        zorder=i+15
    )

# Configuración de los ejes y límites
ax.set_ylim(-0.2, len(consolas_top) * offset + 0.3)
ax.set_xlim(2, 10.2)

# Colocar nombres de consolas en el eje Y (Negro #000000)
ax.set_yticks([i * offset for i in range(len(consolas_top))])
ax.set_yticklabels(reversed(consolas_top), fontsize=13, fontweight='bold', color='#000000')

# Colocar etiquetas en el eje X (Negro #000000)
ax.set_xticks(range(2, 11))
ax.set_xticklabels(range(2, 11), fontsize=12, color='#000000')
ax.set_xlabel("Critic Score (Calificación Crítica)", fontsize=13, fontweight='bold', color='#000000', labelpad=10)

# Línea vertical promedio global de referencia
ax.axvline(
    global_mean,
    color='#64748B',
    linestyle=':',
    linewidth=1.5,
    alpha=0.8,
    zorder=0
)
ax.text(
    global_mean + 0.1,
    len(consolas_top) * offset - 0.2,
    f"Promedio global: {global_mean:.2f}",
    fontsize=11,
    color='#000000',
    family='Arial',
    va='center'
)

# Quitar espinas (bordes de gráfico) para estética minimalista
for spine in ['top', 'right', 'left', 'bottom']:
    ax.spines[spine].set_visible(False)

# Título y Subtítulo (Negro #000000)
plt.text(1.7, len(consolas_top) * offset + 0.45, "Distribución de Calidad por Consola", 
         fontsize=20, fontweight='bold', color='#000000', family='Arial', ha='left')
plt.text(1.7, len(consolas_top) * offset + 0.15, "Comparativa del Critic Score para los videojuegos en las 5 consolas más vendidas", 
         fontsize=12, color='#000000', family='Arial', ha='left')

# Nota de pie de página y fuente (Negro #000000)
plt.text(1.7, -0.7, "Nota: Las líneas segmentadas (--) indican el promedio de calidad para cada consola específica.\n"
                    "El promedio global de calidad en el dataset es de 7.10 (línea punteada ...).\n"
                    "Fuente de datos: Video Game Sales 2024 (Kaggle/Wikidata)", 
         fontsize=9.5, color='#000000', family='Arial', ha='left', va='top', linespacing=1.3)

plt.tight_layout()

# Guardar imagen en alta resolución con fondo blanco
output_filename = "ridgeline_quality.png"
plt.savefig(output_filename, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
plt.close()

print(f"Gráfico Ridgeline generado correctamente y guardado como '{output_filename}'.")
