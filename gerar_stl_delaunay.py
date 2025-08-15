import numpy as np
import os
import trimesh
from scipy.spatial import Delaunay

def gerar_stl_delaunay(caminho_pts, output_dir):
    # Carregar os pontos do ficheiro .pts
    pontos = []
    with open(caminho_pts, 'r') as f:
        for linha in f:
            partes = linha.strip().split()
            if len(partes) == 3:
                x, y, z = map(float, partes)
                pontos.append([x, y, z])
    pontos = np.array(pontos)

    # Verificar se há pontos suficientes
    if len(pontos) < 3:
        raise ValueError("São necessários pelo menos 3 pontos para gerar uma malha STL.")

    # Triangulação Delaunay em 2D (x, y)
    pontos_xy = pontos[:, :2]
    delaunay = Delaunay(pontos_xy)

    # Criar faces usando os índices da triangulação
    faces = delaunay.simplices

    # Criar a malha trimesh
    malha = trimesh.Trimesh(vertices=pontos, faces=faces)

    # Guardar como STL
    caminho_stl = os.path.join(output_dir, 'pontos_compensados_delaunay.stl')
    malha.export(caminho_stl)

    print(f"STL gerado com sucesso: {caminho_stl}")
    return malha, caminho_stl

# Exemplo de uso:
# gerar_stl_delaunay('outputs/pts_comp.pts', 'outputs')

