import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial'],
    'font.size': 14
})


def separar_valores(texto):
    if pd.isna(texto):
        return []
    limpio = str(texto).replace('(', '').replace(')', '')
    return [p.strip() for p in limpio.split(',') if p.strip()]


archivo = "../../data/Encuesta_videojuegos.csv"
df = pd.read_csv(
    archivo,
    usecols=['¿Plataformas de Juego Favorita?', '¿Aspecto que valoras más en un videojuego?']
)

df.columns = ['Plataformas', 'Aspecto']
df['Plataformas'] = df['Plataformas'].apply(separar_valores)
df['Aspecto'] = df['Aspecto'].apply(separar_valores)


df_exp = df[['Plataformas', 'Aspecto']].copy()
df_exp = df_exp.explode('Plataformas').explode('Aspecto')

ct = pd.crosstab(df_exp['Plataformas'].to_numpy(), df_exp['Aspecto'].to_numpy())
ct = ct.sort_index()
ct.columns = ct.columns.astype(str)


def get_distinct_palette(n):
    if n <= 10:
        return sns.color_palette('tab10', n_colors=n)
    if n <= 20:
        return sns.color_palette('tab20', n_colors=n)
    return sns.color_palette('husl', n_colors=n)


labels = list(ct.columns)
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(figsize=(18, 18), subplot_kw=dict(polar=True))
palette = get_distinct_palette(len(ct))

for idx, (label, row) in enumerate(ct.iterrows()):
    values = row.tolist()
    values += values[:1]
    color = palette[idx]
    ax.plot(angles, values, label=label, color=color, linewidth=2.5)
    ax.fill(angles, values, alpha=0.2, color=color)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)
ax.set_title('Plataforma vs Aspecto', pad=20)
ax.set_rlabel_position(30)
ax.tick_params(axis='x', pad=12)
ax.tick_params(axis='y', pad=8)
ax.legend(loc='center left', bbox_to_anchor=(1.45, 0.5), fontsize=12, title='Plataforma', title_fontsize=13)
fig.subplots_adjust(left=0.14, right=0.68, top=0.92, bottom=0.05)
fig.tight_layout()
fig.savefig('v2.png', bbox_inches='tight')
plt.close(fig)
