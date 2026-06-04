import pandas as pd

games = pd.read_csv("vgchartz-2024-clean.csv")
publishers = pd.read_csv("publisher_country.csv")
countries = pd.read_csv("countries_latlon.csv")

# Publisher -> Country
games = games.merge(
    publishers,
    on="publisher",
    how="left"
)

# Country -> Lat/Lon
games = games.merge(
    countries,
    on="country",
    how="left"
)

games.to_csv(
    "videojuegos_final.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Generado: videojuegos_final.csv")