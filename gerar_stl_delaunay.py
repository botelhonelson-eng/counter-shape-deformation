import numpy as np
import os
import trimesh
from scipy.spatial import Delaunay

def gerar_stl_delaunay(pontos, output_dir):   

    # Converter para array numpy
    pontos_np = np.array(pontos)

    # Triangulação Delaunay em 2D (x, y)
    pontos_xy = pontos_np[:, :2]
    delaunay = Delaunay(pontos_xy)
    faces = delaunay.simplices

    # Criar a malha
    malha = trimesh.Trimesh(vertices=pontos_np, faces=faces)

    # Exportar STL
    caminho_stl = os.path.join(output_dir, 'pontos_compensados_delaunay.stl')
    malha.export(caminho_stl)

    return malha, caminho_stl

