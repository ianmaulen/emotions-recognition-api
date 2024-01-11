# -*- coding: utf-8 -*-

import os
import boto3
import openpyxl
from openpyxl.drawing.image import Image
from openpyxl.utils.dataframe import dataframe_to_rows
from dotenv import load_dotenv
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
import re

load_dotenv()

def extract_image_number(filename):
    match = re.search(r'frame_(\d+)\.jpg', filename)
    if match:
        return int(match.group(1))
    return 0

def process_emotions(image_folder, excel_file_path):
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    region_name = os.environ.get('AWS_REGION')

    rekognition_client = boto3.client('rekognition', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)

    image_files = [os.path.join(image_folder, filename) for filename in os.listdir(image_folder) if filename.endswith('.jpg')]
    image_files = sorted(image_files, key=extract_image_number)

    emotion_results = {
        'CALM': [],
        'CONFUSED': [],
        'SURPRISED': [],
        'FEAR': [],
        'SAD': [],
        'ANGRY': [],
        'HAPPY': [],
        'DISGUSTED': [],
    }

    for image_file in image_files:
        with open(image_file, 'rb') as image_data:
            response = rekognition_client.detect_faces(
                Image={'Bytes': image_data.read()},
                Attributes=['ALL']
            )

        if 'FaceDetails' in response:
            for face_detail in response['FaceDetails']:
                for emotion in face_detail['Emotions']:
                    emotion_type = emotion['Type']
                    confidence = emotion['Confidence']
                    emotion_results[emotion_type].append(confidence)
    print(f'Se han obtenido las emociones de las 30 imagenes con éxito')
    return emotion_results
# EXPORTACIÓN A EXCEL CON GRAFICOS
    # df = pd.DataFrame(emotion_results, index=[f'Imagen {i+1}' for i in range(len(image_files))])

    # wb = openpyxl.Workbook()
    # ws = wb.active
    # contador = 1

    # for emotion in df.columns:
    #     plt.figure(figsize=(8, 4))
    #     plt.plot(range(1, len(image_files) + 1), df[emotion], label=emotion)
    #     plt.xlabel('Imágenes')
    #     plt.ylabel('Confidencia')
    #     plt.legend(loc='best')
    #     plt.title(f'Confidencia de {emotion} por Imagen')
    #     img_buffer = BytesIO()
    #     plt.savefig(img_buffer, format='png')
    #     img = Image(img_buffer)
    #     ws.add_image(img, 'A' + str(contador))
    #     contador += 22

    # nombres_columna = ['Imagen ' + str(i + 1) for i in range(len(image_files))]

    # ws_tabla = wb.create_sheet("Tabla de Emociones")

    # datos_tabla = []
    # emociones = df.columns

    # datos_tabla.append([''] + nombres_columna)

    # for emocion in emociones:
    #     fila = [emocion]
    #     fila.extend(df[emocion])
    #     datos_tabla.append(fila)

    # for fila in datos_tabla:
    #     ws_tabla.append(fila)

    # wb.save(excel_file_path)
    # print(f"Resultados guardados en {excel_file_path}")