import trimesh
import numpy as np
import os

def def_3D(stl_or, stl_def, stl_med, passo, nivel_compensacao, output_dir):
    def calcular_inter(superf, x, y):
        z_distante = superf.bounds[1, 2] + 100
        ponto_ray = np.array([x, y, z_distante])
        locations, _, _ = superf.ray.intersects_location(
            ray_origins=[ponto_ray],
            ray_directions=[[0, 0, -1]],
            multiple_hits=False
        )
        return locations[0] if len(locations) > 0 else []

    limite_x_min = stl_or.bounds[0, 0]
    limite_x_max = stl_or.bounds[1, 0]
    limite_y_min = stl_or.bounds[0, 1]
    limite_y_max = stl_or.bounds[1, 1]

    inc_y = 0
    inc_x = 0
    comp_pontos = []
    linhas = []
    linha = []
    fator_comp = nivel_compensacao/100

    while limite_y_min + inc_y < limite_y_max:
        inc_y += passo
        while limite_x_min + inc_x < limite_x_max:
            inc_x += passo
            x = limite_x_min + inc_x
            y = limite_y_min + inc_y

            inter_or = calcular_inter(stl_or, x, y)
            inter_def = calcular_inter(stl_def, x, y)
            inter_med = calcular_inter(stl_med, x, y)

            if len(inter_or) > 0 and len(inter_def) > 0 and len(inter_med) > 0:
                compensacao = (inter_med[2] - inter_or[2]) * fator_comp
                ponto_comp = [x, y, inter_def[2] - compensacao]
                comp_pontos.append(ponto_comp)
                linha.append(ponto_comp)

        if linha:
            linhas.append(linha)
        linha = []
        inc_x = 0

    nome_pts = os.path.join(output_dir, 'pts_comp.pts')
    
    with open(nome_pts, "w") as ficheiro_pts:

        for ind_linha, linha in enumerate(linhas):   
            for ponto in linha:
                texto_linha = str(ponto[0]) + ' ' + str(ponto[1]) + ' ' + str(ponto[2]) + '\n'
                ficheiro_pts.writelines(texto_linha)

    
    ficheiro_pts.close()
    return nome_pts


