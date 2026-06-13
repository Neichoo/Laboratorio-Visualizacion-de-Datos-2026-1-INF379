import pandas as pd
import plotly.express as px

archivo = "../../data/clean/videojuegos_final.csv"

df = pd.read_csv(archivo)

df["critic_score"] = pd.to_numeric(df["critic_score"], errors="coerce")

df_limpio = df.dropna(subset=["country", "critic_score"])

df_paises = (
    df_limpio
    .groupby("country", as_index=False)
    .agg(
        critic_score_promedio=("critic_score", "mean"),
        cantidad_juegos=("title", "count")
    )
)

df_paises["critic_score_promedio"] = df_paises["critic_score_promedio"].round(2)

fig = px.choropleth(
    df_paises,
    locations="country",
    locationmode="country names",
    color="critic_score_promedio",
    hover_name="country",
    hover_data={
        "critic_score_promedio": True,
        "country": False
    },
    color_continuous_scale="RdYlGn",
    range_color=(0, 10),
    title="Critic Score promedio de videojuegos por país",
    labels={
        "critic_score_promedio": "Critic Score promedio"
    }
)

fig.update_layout(
    font=dict(
        family="Arial",
        size=14
    ),

    title=dict(
        text="Critic Score promedio de videojuegos por país",
        x=0.5,
        font=dict(
            family="Arial",
            size=24
        )
    ),

    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type="natural earth"
    ),

    coloraxis_colorbar=dict(
        title=dict(
            text="Critic Score<br>promedio",
            font=dict(
                family="Arial",
                size=14
            )
        ),
        tickfont=dict(
            family="Arial",
            size=14
        )
    ),

    annotations=[
        dict(
            text="Fuente: Dataset de videojuegos",
            x=0,
            y=-0.08,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(
                family="Arial",
                size=11
            )
        )
    ]
)

fig.show()

fig.write_html("mapa_critic_score_promedio_por_pais.html")