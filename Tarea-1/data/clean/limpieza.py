import pandas as pd

df = pd.read_csv("../raw/vgchartz-2024.csv")

# Columnas a limpiar de datos NULL
cols = [
    "title", "console", "genre", "critic_score", "total_sales"
]

df_clean = df.dropna(subset=cols)
df_clean.to_csv("vgchartz-2024-clean.csv", index=False)

print("Archivo 'vgchartz-2024-clean.csv' creado correctamente.")