from flask import Flask, request, send_from_directory, jsonify, render_template
import os
import trimesh
from def_3D import def_3D
from gerar_stl_delaunay import gerar_stl_delaunay
from convert_to_stl_any import convert_to_stl_any

app = Flask(__name__, static_folder='static')
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-stl', methods=['POST'])

def process_stl():
    
    try:
        stl_or_path = os.path.join(UPLOAD_FOLDER, request.files['stl_or'].filename)
        extensao = os.path.splitext(request.files['stl_or'].filename)[1].lower()
        if extensao == '.iv':
            stl_or = convert_to_stl_any(stl_or_path)
        else:
            request.files['stl_or'].save(stl_or_path)
            stl_or = trimesh.load(stl_or_path)       

    
        stl_def_path = os.path.join(UPLOAD_FOLDER, request.files['stl_def'].filename)
        extensao = os.path.splitext(request.files['stl_def'].filename)[1].lower()
        if extensao == '.iv':
            stl_def = convert_to_stl_any(stl_def_path)
        else:
            request.files['stl_def'].save(stl_def_path)
            stl_def = trimesh.load(stl_def_path)         

        
        stl_med_path = os.path.join(UPLOAD_FOLDER, request.files['stl_med'].filename)
        extensao = os.path.splitext(request.files['stl_med'].filename)[1].lower()
        
        if extensao == '.iv':
            stl_med = convert_to_stl_any(stl_med_path)
        else:
            request.files['stl_med'].save(stl_med_path)
            stl_med = trimesh.load(stl_med_path)   

        
        passo = float(request.form.get('passo', 1.0))
        nivel_compensacao = float(request.form.get('nivel_compensacao', 100))

        pts_path = def_3D(stl_or, stl_def, stl_med, passo, nivel_compensacao, OUTPUT_FOLDER)
        
        filename = os.path.basename(pts_path)
        
        stl_compensacao, stl_filename = gerar_stl_delaunay(pts_path, OUTPUT_FOLDER)

        
        stl_or.visual.face_colors = [0, 255, 0, 255]  # Verde
        stl_med.visual.face_colors = [0, 0, 255, 255]  # Azul
        stl_def.visual.face_colors = [255, 255, 0, 255]  # Amarelo
        stl_compensacao.visual.face_colors = [255, 0, 0, 255]  # Amarelo


        scene = trimesh.Scene([stl_or, stl_med, stl_def, stl_compensacao]) 
        #scene.show()
       
        scene.export(os.path.join(app.root_path, 'static', 'output.glb'))
        scene.show()

        return jsonify({
            "download_url": f"/download/{filename}",
            "stl_url": f"/outputs/{stl_filename}",
            "message": "Cálculo concluído com sucesso."
        })

    except Exception as e:        
        return jsonify({
            "error": str(e)
        }), 500

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)

@app.route('/outputs/<filename>', methods=['GET'])
def serve_output_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
