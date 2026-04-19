import pandas as pd
import plotly.express as px
import plotly.io as pio

df = pd.read_csv("../../data/clean/vgchartz-2024-clean.csv")

df = df.dropna(subset=["publisher", "developer", "total_sales"])

total = df["total_sales"].sum()

fig = px.icicle(
    df,
    path=["publisher", "developer"],
    values="total_sales",
    title=f"Developers más rentables de cada Publisher.   Total: {total:.1f}",
)

fig.update_layout(
    margin=dict(t=30, l=0, r=10, b=25),

    font=dict(
        family="Arial",
    ),

    title_font=dict(
        family="Arial",
        size=24
    ),

    annotations=[
        dict(
            text='Ventas en millones de unidades | Fuente: Video Game Sales 2024 - asaniczka',
            x=0.5,
            y=-0.03,
            showarrow=False,
            xref='paper',
            yref='paper',
            font=dict(
                family="Arial",
                size=11
            )
        )
    ]
)

fig.update_traces(
    domain=dict(x=[0.0, 0.75]),
    texttemplate="%{label} %{value:.1f}",
    textfont=dict(
        family="Arial",
        size=14
    )
)

pio.write_image(fig, "icicle.png", width=1200, height=800)