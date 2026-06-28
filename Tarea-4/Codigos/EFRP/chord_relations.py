import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.path as mpath

# 1. Configuración de fuente y estilo unificado
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['font.size'] = 12

# 2. Cargar y procesar datos de la encuesta
survey_path = "../../data/clean/Encuesta_videojuegos.csv"
if not os.path.exists(survey_path):
    # Intentar localmente
    survey_path = "Encuesta_videojuegos.csv"

if not os.path.exists(survey_path):
    raise FileNotFoundError("No se encontró el archivo de encuesta 'Encuesta_videojuegos.csv'")

df = pd.read_csv(survey_path)

# Definir géneros y modalidades de interés
genres_list = ['Shooter', 'Acción', 'RPG/JRPG', 'Aventura', 'Sandbox']
modes_list = ['Multijugador', 'SinglePlayer', 'PVP', 'Cooperativo', 'PVE']

# Contar co-ocurrencias
co_occurrences = {}
for g in genres_list:
    for m in modes_list:
        co_occurrences[(g, m)] = 0

for _, row in df.iterrows():
    genres_raw = row['¿Género favorito de videojuego?']
    modes_raw = row['Qué modalidad de juego prefieres?']
    
    if pd.isna(genres_raw) or pd.isna(modes_raw):
        continue
        
    genres = [g.strip() for g in str(genres_raw).split(',') if g.strip()]
    modes = [m.strip() for m in str(modes_raw).split(',') if m.strip()]
    
    for g in genres:
        if g in genres_list:
            for m in modes:
                if m in modes_list:
                    co_occurrences[(g, m)] += 1

# Calcular pesos de nodos
genre_weights = {g: sum(co_occurrences[(g, m)] for m in modes_list) for g in genres_list}
mode_weights = {m: sum(co_occurrences[(g, m)] for g in genres_list) for m in modes_list}

# Convertir ángulos a radianes
def deg2rad(deg):
    return deg * np.pi / 180.0

# 3. Calcular la distribución de arcos
# Lado izquierdo (Géneros): 95° a 265° (rango de 170°)
# Lado derecho (Modalidades): -85° a 85° (rango de 170°)
R = 1.0          # Radio del círculo interior
R_outer = 1.04   # Radio del anillo exterior
gap_angle = 2.0  # Espacio entre nodos en grados

# Géneros (Lado Izquierdo)
total_g_weight = sum(genre_weights.values())
g_angles_budget = 170.0 - (len(genres_list) - 1) * gap_angle
g_start = 95.0

# Modalidades (Lado Derecho)
total_m_weight = sum(mode_weights.values())
m_angles_budget = 170.0 - (len(modes_list) - 1) * gap_angle
m_start = -85.0

# Asignar ángulos iniciales y finales para cada nodo
node_arcs = {}

# Asignar arcos de Géneros (de arriba a abajo: de 95° a 265° en sentido antihorario)
current_angle = g_start
for g in genres_list:
    weight = genre_weights[g]
    arc_len = (weight / total_g_weight) * g_angles_budget
    node_arcs[g] = (current_angle, current_angle + arc_len)
    current_angle += arc_len + gap_angle

# Asignar arcos de Modalidades (de abajo a arriba: de -85° a 85° en sentido antihorario)
current_angle = m_start
for m in modes_list:
    weight = mode_weights[m]
    arc_len = (weight / total_m_weight) * m_angles_budget
    node_arcs[m] = (current_angle, current_angle + arc_len)
    current_angle += arc_len + gap_angle

# 4. Calcular los sub-arcos de las conexiones
connection_arcs = {}

# Para cada Género, sus conexiones con las Modalidades
for g in genres_list:
    theta_start, theta_end = node_arcs[g]
    total_w = genre_weights[g]
    curr_theta = theta_start
    # El orden de las cuerdas dentro del arco del género va de arriba a abajo
    for m in modes_list:
        w = co_occurrences[(g, m)]
        arc_w = (w / total_w) * (theta_end - theta_start)
        connection_arcs[(g, m, 'g')] = (curr_theta, curr_theta + arc_w)
        curr_theta += arc_w

# Para cada Modalidad, sus conexiones con los Géneros
for m in modes_list:
    theta_start, theta_end = node_arcs[m]
    total_w = mode_weights[m]
    curr_theta = theta_start
    # El orden de las cuerdas dentro del arco de la modalidad va de abajo a arriba
    for g in genres_list:
        w = co_occurrences[(g, m)]
        arc_w = (w / total_w) * (theta_end - theta_start)
        connection_arcs[(g, m, 'm')] = (curr_theta, curr_theta + arc_w)
        curr_theta += arc_w

# Colores para los géneros (que colorearán sus cuerdas asociadas)
colors_genres = {
    'Shooter': '#F43F5E',     # Rosa
    'Acción': '#F97316',      # Naranja
    'RPG/JRPG': '#8B5CF6',    # Violeta
    'Aventura': '#3B82F6',    # Azul
    'Sandbox': '#10B981'      # Esmeralda
}
color_mode_arcs = '#475569'   # Gris pizarra para modalidades de juego

# 5. Función para generar puntos del arco
def get_arc_points(start_deg, end_deg, radius, num_points=15):
    angles = np.linspace(deg2rad(start_deg), deg2rad(end_deg), num_points)
    return [(radius * np.cos(a), radius * np.sin(a)) for a in angles]

# 6. Inicializar la figura de Matplotlib
fig, ax = plt.subplots(figsize=(11, 11), facecolor='#FAFAFA')
ax.set_facecolor('#FAFAFA')

# Dibujar los anillos exteriores
# Géneros (Lado Izquierdo)
for g in genres_list:
    t_start, t_end = node_arcs[g]
    color = colors_genres[g]
    
    # Dibujar sector circular grueso
    outer_pts = get_arc_points(t_start, t_end, R_outer)
    inner_pts = list(reversed(get_arc_points(t_start, t_end, R)))
    
    # Crear PathPatch
    vertices = outer_pts + inner_pts
    codes = [mpath.Path.MOVETO] + [mpath.Path.LINETO] * (len(outer_pts) - 1)
    codes += [mpath.Path.LINETO] + [mpath.Path.LINETO] * (len(inner_pts) - 1)
    codes += [mpath.Path.CLOSEPOLY]
    vertices.append(outer_pts[0])
    
    path = mpath.Path(vertices, codes)
    patch = mpatches.PathPatch(path, facecolor=color, edgecolor='white', linewidth=0.5, zorder=10)
    ax.add_patch(patch)
    
    # Agregar etiqueta de texto horizontal fuera del arco
    mid_deg = (t_start + t_end) / 2.0
    mid_rad = deg2rad(mid_deg)
    label_r = R_outer + 0.05
    ax.text(
        label_r * np.cos(mid_rad),
        label_r * np.sin(mid_rad),
        g,
        fontsize=12,
        fontweight='bold',
        color='#1E293B',
        ha='right' if (mid_rad > np.pi/2 or mid_rad < -np.pi/2) else 'left',
        va='center',
        family='Arial',
        zorder=12
    )

# Modalidades (Lado Derecho)
for m in modes_list:
    t_start, t_end = node_arcs[m]
    color = color_mode_arcs
    
    outer_pts = get_arc_points(t_start, t_end, R_outer)
    inner_pts = list(reversed(get_arc_points(t_start, t_end, R)))
    
    vertices = outer_pts + inner_pts
    codes = [mpath.Path.MOVETO] + [mpath.Path.LINETO] * (len(outer_pts) - 1)
    codes += [mpath.Path.LINETO] + [mpath.Path.LINETO] * (len(inner_pts) - 1)
    codes += [mpath.Path.CLOSEPOLY]
    vertices.append(outer_pts[0])
    
    path = mpath.Path(vertices, codes)
    patch = mpatches.PathPatch(path, facecolor=color, edgecolor='white', linewidth=0.5, zorder=10)
    ax.add_patch(patch)
    
    mid_deg = (t_start + t_end) / 2.0
    mid_rad = deg2rad(mid_deg)
    label_r = R_outer + 0.05
    ax.text(
        label_r * np.cos(mid_rad),
        label_r * np.sin(mid_rad),
        m,
        fontsize=12,
        fontweight='bold',
        color='#1E293B',
        ha='right' if (mid_rad > np.pi/2 or mid_rad < -np.pi/2) else 'left',
        va='center',
        family='Arial',
        zorder=12
    )

# Dibujar las cuerdas/cintas con curvas de Bezier
for g in genres_list:
    for m in modes_list:
        w = co_occurrences[(g, m)]
        if w == 0:
            continue
            
        color = colors_genres[g]
        
        # Obtener los ángulos de los sub-arcos de conexión
        g_theta_s, g_theta_e = connection_arcs[(g, m, 'g')]
        m_theta_s, m_theta_e = connection_arcs[(g, m, 'm')]
        
        # Puntos del arco del género
        g_pts = get_arc_points(g_theta_s, g_theta_e, R)
        # Puntos del arco de la modalidad (invertidos para el sentido de la cinta)
        m_pts = list(reversed(get_arc_points(m_theta_s, m_theta_e, R)))
        
        # Dibujar cuerda: arco género -> curva bezier a modalidad -> arco modalidad -> curva bezier a género
        # Vértices del path
        vertices = []
        codes = []
        
        # 1. Mover al inicio del arco del género
        vertices.append(g_pts[0])
        codes.append(mpath.Path.MOVETO)
        
        # 2. Dibujar línea/arco del género
        for pt in g_pts[1:]:
            vertices.append(pt)
            codes.append(mpath.Path.LINETO)
            
        # 3. Curva bezier hacia el inicio de la modalidad (control en 0,0)
        vertices.append((0.0, 0.0))  # Control
        vertices.append(m_pts[0])    # End point
        codes.append(mpath.Path.CURVE3)
        codes.append(mpath.Path.CURVE3)
        
        # 4. Dibujar línea/arco de la modalidad
        for pt in m_pts[1:]:
            vertices.append(pt)
            codes.append(mpath.Path.LINETO)
            
        # 5. Curva bezier de regreso al inicio del género (control en 0,0)
        vertices.append((0.0, 0.0))  # Control
        vertices.append(g_pts[0])    # End point
        codes.append(mpath.Path.CURVE3)
        codes.append(mpath.Path.CURVE3)
        
        vertices.append(g_pts[0])
        codes.append(mpath.Path.CLOSEPOLY)
        
        path = mpath.Path(vertices, codes)
        # alpha=0.35 para que las intersecciones de cuerdas se vean transparentes y elegantes
        patch = mpatches.PathPatch(path, facecolor=color, edgecolor='none', alpha=0.35, zorder=5)
        ax.add_patch(patch)

# Configurar el gráfico
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')
ax.axis('off')

# Título y Subtítulo
plt.text(-1.45, 1.40, "Preferencia de Géneros y Modalidades de Juego", 
         fontsize=20, fontweight='bold', color='#1E293B', family='Arial', ha='left')
plt.text(-1.45, 1.32, "Relación de preferencia entre géneros de videojuegos y sus modalidades según respuestas de la encuesta", 
         fontsize=12, color='#64748B', family='Arial', ha='left')

# Nota de pie de página y fuente de datos
plt.text(-1.45, -1.35, "Nota: El ancho de las cintas en los extremos es proporcional a la cantidad de respuestas de preferencia.\n"
                       "Las cintas se colorean de acuerdo al género de origen con opacidad para visualizar la superposición.\n"
                       "Fuente de datos: Encuesta de comportamiento de jugadores (Tarea 2)", 
         fontsize=9.5, color='#64748B', family='Arial', ha='left', va='top', linespacing=1.3)

plt.tight_layout()

# Guardar la imagen en alta definición
output_filename = "chord_relations.png"
plt.savefig(output_filename, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()

print(f"Diagrama de cuerdas generado correctamente y guardado como '{output_filename}'.")
