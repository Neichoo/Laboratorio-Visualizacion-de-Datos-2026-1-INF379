import pandas as pd

# Cambia esto por la ruta de tu archivo
archivo = "vgchartz-2024-clean.csv"

# Leer CSV
df = pd.read_csv(archivo)

# Obtener valores únicos
publishers = (
    df["publisher"]
    .dropna()
    .astype(str)
    .str.strip()
    .sort_values()
    .unique()
)

developers = (
    df["developer"]
    .dropna()
    .astype(str)
    .str.strip()
    .sort_values()
    .unique()
)

# Mostrar resultados
print(f"\n=== PUBLISHERS ÚNICOS ({len(publishers)}) ===")
for p in publishers:
    print(p)

print(f"\n=== DEVELOPERS ÚNICOS ({len(developers)}) ===")
for d in developers:
    print(d)

# Guardar a CSV
pd.DataFrame({"publisher": publishers}).to_csv(
    "publishers_unicos.csv",
    index=False,
    encoding="utf-8-sig"
)

pd.DataFrame({"developer": developers}).to_csv(
    "developers_unicos.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nArchivos generados:")
print("- publishers_unicos.csv")
print("- developers_unicos.csv")

print("\nTOP 20 DEVELOPERS")
print(df["developer"].value_counts().head(20))

print("\nTOP 20 PUBLISHERS")
print(df["publisher"].value_counts().head(215))