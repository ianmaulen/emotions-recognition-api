# -*- coding: utf-8 -*-

from flask import Flask, request, send_file, jsonify
from video_fotograms import extract_frames
from emotion_recognition import process_emotions
import os

app = Flask(__name__)

@app.route('/procesar_video', methods=['POST'])
def procesar_video():
    try:
        video_file = request.files['video']
        video_name = os.path.splitext(video_file.filename)[0]
        video_path = os.path.join('uploads', video_file.filename)
        video_file.save(video_path)

        output_folder = os.path.join('uploads', f'{video_name}_frames')
        extract_frames(video_path, output_folder)

        excel_file_path = os.path.join('uploads', f'{video_name}_resultados_emociones.xlsx')
        process_emotions(output_folder, excel_file_path)

        return send_file(excel_file_path, as_attachment=True), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)