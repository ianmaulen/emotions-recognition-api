# -*- coding: utf-8 -*-

import json
from flask import Flask, request, send_file, jsonify
from video_fotograms import extract_frames
from emotion_recognition import process_emotions
from clusters3 import process_clusters
from config import getClusterParams, getOutputText, transformTextAI
import traceback
from openai import OpenAI
# importacion a clusters es el primer modelo creado por José (8 condicionales) y queda inactiva
# from clusters import process_clusters

import os

app = Flask(__name__)

@app.route('/procesar_video', methods=['POST'])
def procesar_video():
    try:
        video_file = request.files['video']
        instruction = request.form['instruction'] 
        video_name = os.path.splitext(video_file.filename)[0]
        video_path = os.path.join('uploads', video_file.filename)
        video_file.save(video_path)

        output_folder = os.path.join('uploads', f'{video_name}_frames')
        extract_frames(video_path, output_folder)

        excel_file_path = os.path.join('uploads', f'{video_name}_resultados_emociones.xlsx')
        emotion_results_json = process_emotions(output_folder, excel_file_path)
        db_params = getClusterParams()
        clusters = process_clusters(emotion_results_json, db_params)
        output = getOutputText(clusters, instruction)
        return jsonify({'status': 'success', 
                        'emotion_results': emotion_results_json,
                        'clusters': clusters,
                        'output': output  
                        }), 200
    except Exception as e:
        print(traceback.format_exc()) 
        return jsonify({'status': 'error', 'message': str(e)}), 500
    

@app.route('/gpt', methods=['POST'])
def procesar_texto():
    try:
        text = request.json['text']
        text_transformed = transformTextAI(text)
        return jsonify({'status': 'success', 
                        'response': text_transformed,
                        }), 200
    except Exception as e:
        print(traceback.format_exc()) 
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)