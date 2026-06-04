import pandas as pd

# Cargar archivo publisher-country
df = pd.read_csv("publisher_country.csv")

# Coordenadas de referencia por país
country_coords = {
    "United States": (37.0902, -95.7129),
    "Japan": (36.2048, 138.2529),
    "United Kingdom": (55.3781, -3.4360),
    "France": (46.2276, 2.2137),
    "Germany": (51.1657, 10.4515),
    "Italy": (41.8719, 12.5674),
    "Russia": (61.5240, 105.3188),
    "Poland": (51.9194, 19.1451),
    "Canada": (56.1304, -106.3468),
    "Finland": (61.9241, 25.7482),
    "Norway": (60.4720, 8.4689),
    "Switzerland": (46.8182, 8.2275),
    "Austria": (47.5162, 14.5501),
    "Sweden": (60.1282, 18.6435),
    "South Korea": (35.9078, 127.7669),
    "Netherlands": (52.1326, 5.2913),
    "Hong Kong": (22.3193, 114.1694),
    "Cyprus": (35.1264, 33.4299),
    "Unknown": (0.0, 0.0),

    
    "Denmark": (56.2639, 9.5018),

    
    "China": (35.8617, 104.1954),
    "Spain": (40.4637, -3.7492),
    "Belgium": (50.5039, 4.4699),
    "Australia": (-25.2744, 133.7751)
}

# Países únicos
countries = (
    df["country"]
    .dropna()
    .astype(str)
    .str.strip()
    .unique()
)

# Crear dataframe
rows = []

for country in sorted(countries):
    lat, lon = country_coords.get(country, (None, None))

    rows.append({
        "country": country,
        "latitude": lat,
        "longitude": lon
    })

countries_df = pd.DataFrame(rows)

# Mostrar países sin coordenadas
missing = countries_df[
    countries_df["latitude"].isna()
]

if len(missing) > 0:
    print("Países sin coordenadas:")
    print(missing["country"].tolist())

countries_df.to_csv(
    "countries_latlon.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Archivo generado: countries_latlon.csv")