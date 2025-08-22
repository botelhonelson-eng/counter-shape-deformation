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
    
    
    def encontrar_outliers(valores):
        valores_np = np.array(valores)
        q1 = np.percentile(valores_np, 25)
        q3 = np.percentile(valores_np, 75)
        iqr = q3 - q1

        limite_inferior = q1 - 1.5 * iqr
        limite_superior = q3 + 1.5 * iqr

        outlier_indices = np.where((valores_np < limite_inferior) | (valores_np > limite_superior))[0]
        return outlier_indices.tolist()

    def filtrar_posicoes(lista_original, indices_excluir):
        return [item for i, item in enumerate(lista_original) if i not in indices_excluir]

    
    def gerar_step(pontos, nome_ficheiro):
        with open(nome_ficheiro, "w") as f:
            f.write("ISO-10303-21;\nHEADER;\n")
            f.write("FILE_DESCRIPTION(('Generated STEP file'),'2;1');\n")
            f.write("FILE_NAME('pontos_gerados.stp','20250820',('User'),('Python Script'), '', 'Python', '');\n")
            f.write("FILE_SCHEMA(('GEOMETRIC_MODEL')); \nENDSEC;\nDATA;\n")

            # Definição de contexto geométrico com unidade
            f.write("#1 = APPLICATION_CONTEXT('mechanical design');\n")         

            # Escrever os pontos
            for i, ponto in enumerate(pontos, start=2):
                x, y, z = ponto
                f.write(f"#{i} = CARTESIAN_POINT('', ({x}, {y}, {z}));\n")

            # rodapé    
            f.write(f"#{i+1}=(LENGTH_UNIT()NAMED_UNIT(*)SI_UNIT(.MILLI.,.METRE.));\n")
            f.write(f"#{i+2}=(NAMED_UNIT(*)PLANE_ANGLE_UNIT()SI_UNIT($,.RADIAN.));\n")
            f.write(f"#{i+5}=(NAMED_UNIT(*)SI_UNIT($,.STERADIAN.)SOLID_ANGLE_UNIT());\n")
            f.write(f"#{i+7}=(GEOMETRIC_REPRESENTATION_CONTEXT(3)GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT((#98))GLOBAL_UNIT_ASSIGNED_CONTEXT((#{i+1},#{i+4},#{i+5}))REPRESENTATION_CONTEXT('ID1','3'));\n")

            f.write("ENDSEC;\nEND-ISO-10303-21;\n")


        
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
    med_comp = []
    pontos_stp = []

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
                med_comp.append(compensacao)
                pontos_stp.append(ponto_comp)

                comp_pontos.append(ponto_comp)                
                linha.append(ponto_comp)

        if linha:
            linhas.append(linha)
        linha = []
        inc_x = 0

    
    indices_excluir = encontrar_outliers(med_comp)
    nome_pts_stp = os.path.join(output_dir, 'pts_stp.stp')
    
    pontos_stp = filtrar_posicoes(pontos_stp, indices_excluir)
    gerar_step(pontos_stp, nome_pts_stp)

    #nome_pts = os.path.join(output_dir, 'pts_comp.pts')
    #with open(nome_pts, "w") as ficheiro_pts:
    #    for ind_linha, linha in enumerate(linhas):   
    #        for ponto in linha:
    #            texto_linha = str(ponto[0]) + ' ' + str(ponto[1]) + ' ' + str(ponto[2]) + '\n'
    #            ficheiro_pts.writelines(texto_linha)
    #    ficheiro_pts.close()
    
    return pontos_stp, nome_pts_stp


