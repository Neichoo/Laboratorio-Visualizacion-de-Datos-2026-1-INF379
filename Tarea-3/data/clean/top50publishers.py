import pandas as pd

df = pd.read_csv("vgchartz-2024-clean.csv")

pubs = (
    df.groupby("publisher")
      .size()
      .reset_index(name="juegos")
      .sort_values("juegos", ascending=False)
)

pubs["porcentaje"] = pubs["juegos"] / pubs["juegos"].sum() * 100
pubs["acumulado"] = pubs["porcentaje"].cumsum()

print(pubs.head(50))