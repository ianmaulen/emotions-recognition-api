from flask import Flask, request, render_template
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()
# conexión a la base de datos
db = pymysql.connect(host=os.environ.get('DATABASE_HOST'), user=os.environ.get('DATABASE_USERNAME'), passwd=os.environ.get('DATABASE_PASSWORD'), db=os.environ.get('DATABASE_NAME'))

def getClusterParams():
    cursor = db.cursor()
    sql = """
    SELECT e.emotion_name, c.cluster_name, cp.limit, cp.peaks
    FROM cluster_params cp
    JOIN emotions e ON cp.emotion = e.id
    JOIN clusters c ON cp.cluster = c.id;
    """
    cursor.execute(sql)
    # nombres de columnas
    column_names = [column[0] for column in cursor.description]
    # filas
    rows = cursor.fetchall()
    # Construir objetos con nombres de columnas como claves
    results = []
    for row in rows:
        row_dict = dict(zip(column_names, row))
        results.append(row_dict)
    print(f'Se han obtenido los parámetros desde la BD')
    return results