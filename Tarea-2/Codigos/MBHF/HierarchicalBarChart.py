import pandas as pd
import plotly.express as px

df = pd.read_csv("../../data/Encuesta_videojuegos.csv")

df['Plataformas'] = df['¿Plataformas de Juego Favorita?'].str.split(', ')
df['Generos'] = df['¿Género favorito de videojuego?'].str.split(', ')

df_exploded = df.explode('Plataformas').explode('Generos')

count_df = df_exploded.groupby(['Plataformas', 'Generos']).size().reset_index(name='count')

platform_order = count_df.groupby('Plataformas')['count'].sum().sort_values(ascending=False).index.tolist()

fig = px.bar(count_df,
             x='count',
             y='Plataformas',
             color='Generos',
             orientation='h',
             category_orders={'Plataformas': platform_order},
             title='Plataformas y Géneros Favoritos',
             labels={'Plataformas': 'Plataformas', 'count': '', 'Generos': 'Géneros'},
             barmode='stack',
             text='Generos')

fig.update_traces(textposition='inside', insidetextanchor='middle', textfont=dict(color='white', size=10))
fig.update_layout(yaxis={'categoryorder':'array', 'categoryarray': platform_order},
                  legend_title_text='Géneros',
                  bargap=0.15,
                  margin=dict(l=150, r=50, t=70, b=50))
fig.update_yaxes(autorange='reversed')

fig.show()