import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# 1. Configuración de la fuente y tamaño solicitados
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['font.size'] = 14

# 2. Cargar los datos
df = pd.read_csv("../../data/Encuesta_videojuegos.csv")

# 3. Extraer solo el Top 5 más frecuente de cada columna
top_plat = df['¿Plataformas de Juego Favorita?'].value_counts().head(5).index.tolist()
top_gen = df['¿Género favorito de videojuego?'].value_counts().head(5).index.tolist()
top_mod = df['Qué modalidad de juego prefieres?'].value_counts().head(5).index.tolist()
top_asp = df['¿Aspecto que valoras más en un videojuego?'].value_counts().head(5).index.tolist()

# 4. Inicializar el Grafo
G = nx.Graph()

# 5. Añadir solo los nodos del Top 5 asignándoles su capa
for val in top_plat: G.add_node(val, layer=0)
for val in top_gen:  G.add_node(val, layer=1)
for val in top_mod:  G.add_node(val, layer=2)
for val in top_asp:  G.add_node(val, layer=3)

# 6. Añadir las conexiones (aristas) con un "label" que indique su significado
for _, row in df.iterrows():
    # ¡Corregido! Ahora lee correctamente la columna de Plataformas
    plat = row['¿Plataformas de Juego Favorita?']
    gen = row['¿Género favorito de videojuego?']
    mod = row['Qué modalidad de juego prefieres?']
    asp = row['¿Aspecto que valoras más en un videojuego?']
    
    if pd.notna(plat) and pd.notna(gen) and plat in top_plat and gen in top_gen:
        # Añadimos el atributo label para indicar qué significa la conexión
        G.add_edge(plat, gen, label="Juega")
        
    if pd.notna(gen) and pd.notna(mod) and gen in top_gen and mod in top_mod:
        G.add_edge(gen, mod, label="Prefiere")
        
    if pd.notna(mod) and pd.notna(asp) and mod in top_mod and asp in top_asp:
        G.add_edge(mod, asp, label="Valora")

# (Opcional) Eliminar nodos que quedaron sin conexiones después del filtrado
G.remove_nodes_from(list(nx.isolates(G)))

# 7. Configurar colores distintivos por capa para los nodos resultantes
color_map = {0: '#FF9999', 1: '#66B2FF', 2: '#99FF99', 3: '#FFCC99'}
node_colors = [color_map[G.nodes[node]['layer']] for node in G.nodes()]

# 8. Crear la figura y el layout multipartito (un poco más ancha para leer mejor los textos)
plt.figure(figsize=(18, 10))
pos = nx.multipartite_layout(G, subset_key="layer")

# 9. Dibujar el grafo (Nodos y líneas)
nx.draw(
    G, pos,
    with_labels=True,
    node_color=node_colors,
    node_size=5500,      # Nodos ligeramente más grandes para que quepa la letra 14
    edge_color='#B0B0B0', 
    width=1.5,           
    font_family='Arial', 
    font_size=14,        # Tamaño 14 solicitado
    font_weight='bold'
)

# 10. Dibujar las etiquetas de las conexiones (qué significa cada arista)
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(
    G, pos,
    edge_labels=edge_labels,
    font_family='Arial',
    font_size=10,        # Un poco más pequeño para que no se amontone todo el texto
    font_color='#4A4A4A',# Gris oscuro para leerlo bien
    bbox=dict(alpha=0.8, edgecolor='none', facecolor='white') # Fondo blanco sutil para mejorar la lectura
)

# Añadir títulos a las columnas (capas)
plt.text(-1, 1.1, 'Plataforma (Top 5)', fontsize=16, fontweight='bold', ha='center', family='Arial')
plt.text(-0.33, 1.1, 'Género (Top 5)', fontsize=16, fontweight='bold', ha='center', family='Arial')
plt.text(0.33, 1.1, 'Modalidad (Top 5)', fontsize=16, fontweight='bold', ha='center', family='Arial')
plt.text(1, 1.1, 'Aspecto Valorado (Top 5)', fontsize=16, fontweight='bold', ha='center', family='Arial')

# 11. Guardar la imagen con el nombre exacto solicitado
plt.savefig('visualizacion-Gemini.png', format='png', dpi=300, bbox_inches='tight')

# Cerrar la figura para liberar memoria
plt.close()

print("El diagrama se ha generado correctamente con las plataformas y los significados de cada conexión.")