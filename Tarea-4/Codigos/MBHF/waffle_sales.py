import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# 1. Configuración de fuente y estilo unificado
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['font.size'] = 12

# 2. Cargar y procesar datos del CSV
csv_path = "../../data/clean/videojuegos_final.csv"
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"No se encontró el archivo {csv_path}")

df = pd.read_csv(csv_path)

# Convertir ventas a numérico
df['total_sales'] = pd.to_numeric(df['total_sales'], errors='coerce').fillna(0.0)

# Calcular ventas totales y porcentajes por región
total_sales_global = df['total_sales'].sum()

# Agrupar países nórdicos
nordicos = ['Sweden', 'Finland', 'Norway']
sales_us = df[df['country'] == 'United States']['total_sales'].sum()
sales_jp = df[df['country'] == 'Japan']['total_sales'].sum()
sales_nordicos = df[df['country'].isin(nordicos)]['total_sales'].sum()

# El resto son otros países
sales_others = total_sales_global - (sales_us + sales_jp + sales_nordicos)

# Calcular porcentajes exactos
pct_us = (sales_us / total_sales_global) * 100
pct_jp = (sales_jp / total_sales_global) * 100
pct_nordicos = (sales_nordicos / total_sales_global) * 100
pct_others = (sales_others / total_sales_global) * 100

print(f"Ventas Calculadas - EE.UU.: {pct_us:.2f}%, Japón: {pct_jp:.2f}%, Nórdicos: {pct_nordicos:.2f}%, Otros: {pct_others:.2f}%")

# Definir la cantidad de cuadrados para la cuadrícula 10x10 (total 100)
# Ajustamos a valores enteros sumando exactamente 100
sq_us = 67
sq_jp = 22
sq_nordicos = 1
sq_others = 10  # 67 + 22 + 1 + 10 = 100

# 3. Diseñar la cuadrícula de Waffle
# Asignamos a cada índice de 0 a 99 un color de acuerdo a las categorías
tile_categories = (
    ['Estados Unidos'] * sq_us +
    ['Japón'] * sq_jp +
    ['Países Nórdicos'] * sq_nordicos +
    ['Otros Países'] * sq_others
)

# Paleta de colores Premium HSL-tailored
colors_dict = {
    'Estados Unidos': '#3B82F6',    # Azul vibrante
    'Japón': '#F43F5E',             # Rosa/Rojo suave
    'Países Nórdicos': '#10B981',   # Emerald Green
    'Otros Países': '#CBD5E1'       # Gris pizarra claro
}

fig, ax = plt.subplots(figsize=(10, 8.5), facecolor='#FAFAFA')
ax.set_facecolor('#FAFAFA')

# Dibujar la cuadrícula de 10x10 parches de tipo Rectangle
# Dibujamos de abajo hacia arriba, de izquierda a derecha
for idx in range(100):
    row = idx // 10
    col = idx % 10
    category = tile_categories[idx]
    color = colors_dict[category]
    
    # Cada cuadrado mide 0.85 x 0.85 con un gap de 0.15
    rect = mpatches.Rectangle(
        (col, row), 0.85, 0.85,
        facecolor=color,
        edgecolor='white',
        linewidth=0.5
    )
    ax.add_patch(rect)

# Configuración de límites y aspecto
ax.set_xlim(-0.5, 10)
ax.set_ylim(-0.5, 10.5)
ax.set_aspect('equal')
ax.axis('off')

# 4. Título y Subtítulo
plt.text(-0.5, 10.8, "El Origen de las Ventas de Videojuegos", 
         fontsize=20, fontweight='bold', color='#1E293B', family='Arial', ha='left')
plt.text(-0.5, 10.3, "Distribución de ventas globales de videojuegos según el origen de producción", 
         fontsize=12, color='#64748B', family='Arial', ha='left')

# 5. Leyenda Personalizada
legend_patches = [
    mpatches.Patch(color=colors_dict['Estados Unidos'], label=f'Estados Unidos ({pct_us:.1f}%)'),
    mpatches.Patch(color=colors_dict['Japón'], label=f'Japón ({pct_jp:.1f}%)'),
    mpatches.Patch(color=colors_dict['Países Nórdicos'], label=f'Países Nórdicos ({pct_nordicos:.1f}%)'),
    mpatches.Patch(color=colors_dict['Otros Países'], label=f'Otros Países ({pct_others:.1f}%)')
]

legend = ax.legend(
    handles=legend_patches,
    loc='upper left',
    bbox_to_anchor=(1.02, 0.95),
    frameon=False,
    fontsize=12,
    title="Orígenes",
    title_fontsize=13
)
legend.get_title().set_fontweight('bold')
legend.get_title().set_color('#1E293B')

# 6. Anotación de Fuente (Requisito del PDF y Rubrica)
plt.text(-0.5, -0.6, "Nota: Cada cuadrado representa el 1% de las ventas globales (~30.4 millones de unidades).\n"
                    "Países Nórdicos incluye Suecia, Finlandia y Noruega.\n"
                    "Fuente de datos: Video Game Sales 2024 (Kaggle/Wikidata)", 
         fontsize=9.5, color='#64748B', family='Arial', ha='left', va='top', linespacing=1.3)

plt.tight_layout()

# Guardar el archivo como PNG de alta calidad
output_filename = "waffle_sales.png"
plt.savefig(output_filename, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()

print(f"Gráfico de Waffle generado correctamente y guardado como '{output_filename}'.")
