import pandas as pd
import plotly.graph_objects as go

# Leer dataset
df = pd.read_csv('../../data/clean/vgchartz-2024-clean.csv')

# --------------------------------------------------
# 1. Top 20 títulos por ventas
# --------------------------------------------------
top_titles = (
    df.groupby("title", as_index=False)["total_sales"]
    .sum()
    .sort_values(by="total_sales", ascending=False)
    .head(20)
)

df_top = df[df["title"].isin(top_titles["title"])]

# --------------------------------------------------
# 2. Agrupar flujos
# --------------------------------------------------
cd = df_top.groupby(["console", "developer"], as_index=False)["total_sales"].sum()
dt = df_top.groupby(["developer", "title"], as_index=False)["total_sales"].sum()

# --------------------------------------------------
# 3. ORDENAR nodos correctamente
# --------------------------------------------------

# Consolas y developers (orden natural)
consoles = list(cd["console"].unique())
developers = list(cd["developer"].unique())

# 🔥 Titles ordenados por ventas (de mayor a menor)
titles_sorted = top_titles.sort_values(
    by="total_sales", ascending=False
)["title"].tolist()

# Lista final de nodos
labels = consoles + developers + titles_sorted

# Mapear nodo a índice
label_to_index = {label: i for i, label in enumerate(labels)}

# --------------------------------------------------
# 4. Crear links
# --------------------------------------------------
sources = []
targets = []
values = []

# console -> developer
for _, row in cd.iterrows():
    sources.append(label_to_index[row["console"]])
    targets.append(label_to_index[row["developer"]])
    values.append(row["total_sales"])

# developer -> title
for _, row in dt.iterrows():
    sources.append(label_to_index[row["developer"]])
    targets.append(label_to_index[row["title"]])
    values.append(row["total_sales"])

# --------------------------------------------------
# 5. Sankey
# --------------------------------------------------
fig = go.Figure(data=[go.Sankey(
    arrangement="snap",  # ayuda a respetar el orden
    node=dict(
        pad=20,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values
    )
)])

# Layout
fig.update_layout(
    title_text="Flujo de Ventas de Videojuegos (Top 20 Títulos)",
    font=dict(family="Arial", size=14),
    title_font=dict(family="Arial", size=24),
    annotations=[
        dict(
            text="Console → Developer → Title (ordenado por ventas)",
            showarrow=False,
            x=0.5,
            y=-0.1,
            xref="paper",
            yref="paper",
            font=dict(family="Arial", size=11)
        )
    ]
)

# Guardar
fig.write_image("sankey_videojuegos.png", width=1200, height=800)

fig.show()