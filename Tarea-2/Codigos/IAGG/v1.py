import pandas as pd
import matplotlib.pyplot as plt
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
    usecols=['Qué modalidad de juego prefieres?', '¿Aspecto que valoras más en un videojuego?']
)

df.columns = ['Modalidad', 'Aspecto']
df['Modalidad'] = df['Modalidad'].apply(separar_valores)
df['Aspecto'] = df['Aspecto'].apply(separar_valores)


df_exp = df[['Modalidad', 'Aspecto']].copy()
df_exp = df_exp.explode('Modalidad').explode('Aspecto')

ct = pd.crosstab(df_exp['Modalidad'].to_numpy(), df_exp['Aspecto'].to_numpy())
ct = ct.sort_index()
ct.columns = ct.columns.astype(str)


fig, ax = plt.subplots(figsize=(18, 10))
x = np.arange(len(ct.columns))
y = np.arange(len(ct.index))
xs, ys, sizes, freqs = [], [], [], []
max_val = ct.values.max()
norm = plt.Normalize(vmin=0, vmax=max_val)

for i, row in enumerate(ct.index):
    for j, col in enumerate(ct.columns):
        value = ct.loc[row, col]
        if value > 0:
            xs.append(j)
            ys.append(i)
            sizes.append((value / max_val) * 2500 + 80)
            freqs.append(value)

scatter = ax.scatter(
    xs,
    ys,
    s=sizes,
    c=freqs,
    cmap='Blues',
    norm=norm,
    alpha=0.85,
    edgecolors='k'
)

for x_val, y_val, value in zip(xs, ys, freqs):
    ax.text(x_val, y_val, str(value), ha='center', va='center', fontsize=12, color='black')

ax.set_xticks(x)
ax.set_xticklabels(ct.columns, rotation=45, ha='right')
ax.set_yticks(y)
ax.set_yticklabels(ct.index)
ax.set_title('Aspectos Valorados por Modalidad de Juego')
ax.set_xlim(-0.5, len(ct.columns) - 0.5)
ax.set_ylim(-0.5, len(ct.index) - 0.5)
fig.colorbar(scatter, ax=ax, label='Frecuencia', pad=0.02)
fig.tight_layout()
fig.savefig('v1.png', bbox_inches='tight')
plt.close(fig)
