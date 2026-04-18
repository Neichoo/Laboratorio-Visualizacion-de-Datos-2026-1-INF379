import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Leer el csv
df = pd.read_csv('../../data/clean/vgchartz-2024-clean.csv')

# Extraer columnas
cols = ['title', 'total_sales', 'critic_score']
df = df[cols]

# Agrupar por título
df = df.groupby('title', as_index=False).agg({
    'total_sales': lambda x: x.sum(min_count=1),
    'critic_score': 'first'
})

# Crear categorías
bins = [0, 4, 7, 10]
labels = ['Malo', 'Regular', 'Bueno']

df['score_cat'] = pd.cut(df['critic_score'], bins=bins, labels=labels, include_lowest=True)

# Orden de categorías
x_map = {cat: i for i, cat in enumerate(labels)}

# Top 10 juegos
top10 = df.sort_values('total_sales', ascending=False).head(10).copy()

# Colores para el top 10
top10_colors = sns.color_palette('tab10', 10)
color_map = dict(zip(top10['title'], top10_colors))

# Figura con 2 paneles
fig, (ax, ax_panel) = plt.subplots(
    ncols=2,
    figsize=(15, 7),
    gridspec_kw={'width_ratios': [4, 1.8]}
)

df_rest = df.drop(top10.index)

# Gráfico principal
sns.stripplot(
    data=df_rest,
    x='score_cat',
    y='total_sales',
    order=labels,
    hue='score_cat',
    jitter=True,
    size=4,
    alpha=0.25,
    ax=ax
)

# Resaltar top 10
for _, row in top10.iterrows():
    ax.scatter(
        x=x_map[row['score_cat']],
        y=row['total_sales'],
        s=90,
        color=color_map[row['title']],
        edgecolor='black',
        linewidth=0.8,
        zorder=5
    )

# Etiquetas del top por categoría
top_por_categoria = df.loc[df.groupby('score_cat', observed=False)['total_sales'].idxmax()]

for _, row in top_por_categoria.iterrows():
    ax.text(
        x=x_map[row['score_cat']] + 0.03,
        y=row['total_sales'],
        s=row['title'],
        fontsize=9,
        ha='left',
        va='bottom',
        fontweight='bold',
        color='black'
    )

ax.set_title('Ventas de videojuegos por categoría de crítica', fontsize=14)
ax.set_xlabel('Categoría Critic Score')
ax.set_ylabel('Ventas Totales (En millones de unidades)')
ax.set_xticks(range(len(labels)))
ax.set_xticklabels(labels)
ax.grid(axis='y', linestyle='--', alpha=0.3)
ax.set_axisbelow(True)

# Panel derecho
ax_panel.axis('off')
ax_panel.set_xlim(0, 1)
ax_panel.set_ylim(0, 1)

ax_panel.text(
    0.05, 0.96,
    'Top 10 juegos\npor ventas totales',
    fontsize=12,
    fontweight='bold',
    ha='left',
    va='top'
)

y_positions = np.linspace(0.85, 0.10, 10)

for (_, row), y in zip(top10.iterrows(), y_positions):
    ax_panel.scatter(
        x=0.08,
        y=y,
        s=90,
        color=color_map[row['title']],
        edgecolor='black',
        linewidth=0.8,
        zorder=5
    )

    ax_panel.text(
        0.14,
        y,
        row["title"],
        color='black',
        fontsize=10,
        fontweight='bold',
        ha='left',
        va='center'
    )

fig.text(
    0.5, 0.02,
    'Ventas en millones de unidades | Fuente: Video Game Sales 2024 - asaniczka',
    ha='center',
    va='bottom',
    fontsize=10
)

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.show()