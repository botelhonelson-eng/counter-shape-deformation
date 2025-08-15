import re
import os
import trimesh

def convert_to_stl_any(path_3D):  
    def converter_iv(path_3D):
        erro = False
        lista_coord = []   
        lista_normais = []
        lista_indices_faces_cor = []        
        ficheiro_iv = path_3D
        
        if erro == False:
            try:
                with open(ficheiro_iv, "r") as iv:
                    linhas= iv.readlines()
                    num_linha = 1
                    while num_linha < len(linhas)-1:                 
                        if 'diffuseColor' in linhas[num_linha]:
                            lista_coord = []   
                            lista_normais = [] 
                            linha_cor =re.split(' ', linhas[num_linha][24:].rstrip())
                            cor = int(round(float(linha_cor[0])*255,0)), int(round(float(linha_cor[1])*255,0)), int(round(float(linha_cor[2])*255,0))
                            num_linha_int = num_linha + 4
                            while '}' not in linhas[num_linha_int]: 
                                normal_aux =re.split(' ', linhas[num_linha_int].replace("vector", "").replace("[", "").replace("]", "").replace(",", "").rstrip().lstrip())
                                normal= float(normal_aux[0]), float(normal_aux[1]), float(normal_aux[2])
                                lista_normais.append(normal)
                                num_linha_int += 1
                            num_linha_int += 5
                            while '}' not in linhas[num_linha_int]: 
                                ponto_aux =re.split(' ', linhas[num_linha_int].replace("point", "").replace("[", "").replace("]", "").replace(",", "").rstrip().lstrip())
                                ponto= float(ponto_aux[0]), float(ponto_aux[1]), float(ponto_aux[2])
                                lista_coord.append(ponto)
                                num_linha_int += 1
                            for ind in range(0, len(lista_normais), 3):                                     
                               lista_indices_faces_cor.append([lista_normais[ind], lista_coord[ind], lista_coord[ind+1], lista_coord[ind+2], cor])         
                        num_linha += 1

                    if len(lista_indices_faces_cor) == 0:
                        erro = True
                    else:
                        erro = False
            except:
                erro = True
           
        return lista_indices_faces_cor, erro
    mesh = trimesh.creation.icosphere(subdivisions=3, radius=1.0, color=None)
    lista_indices_faces_cor, erro_stl = converter_iv(path_3D)    
    if erro_stl == False:          
        nome_ficheiro = path_3D[:-3] + '.stl'
        ficheiro_stl = open(nome_ficheiro, "w") 
        ficheiro_stl.write('solid iv_stl\n')
        cor_faces_mesh = []
        for ind, faces in enumerate(lista_indices_faces_cor):   
            vetor_1 = faces[0]   
            ponto_1 = faces[1]
            ponto_2 = faces[2]
            ponto_3 = faces[3]                
            cor_faces_mesh.append(faces[4])           
            ficheiro_stl.write(f'  facet normal {str(vetor_1[0])} {str(vetor_1[1])} {str(vetor_1[2])}\n')
            ficheiro_stl.write('    outer loop\n')
            ficheiro_stl.write(f'      vertex {str(ponto_1[0])} {str(ponto_1[1])} {str(ponto_1[2])}\n')
            ficheiro_stl.write(f'      vertex {str(ponto_2[0])} {str(ponto_2[1])} {str(ponto_2[2])}\n')
            ficheiro_stl.write(f'      vertex {str(ponto_3[0])} {str(ponto_3[1])} {str(ponto_3[2])}\n')
            ficheiro_stl.write('    endloop\n')
            ficheiro_stl.write('  endfacet\n')                   
        ficheiro_stl.write('endsolid vrml_stl')
        ficheiro_stl.close()
        
        mesh = trimesh.load_mesh(nome_ficheiro)
        if mesh.is_empty == False:
            for ind, face in enumerate(mesh.faces):
                mesh.visual.face_colors[ind] = [cor_faces_mesh[ind][0], cor_faces_mesh[ind][1], cor_faces_mesh[ind][2], 255]  
        else:
            erro_stl = True
    else:
        print(f'STL conversion error on file {os.path.basename(path_3D)}')       
    return mesh





















