from flask import Flask, request, render_template
from openai import OpenAI
import pymysql
import os
import random
from dotenv import load_dotenv

load_dotenv()
# conexión a la base de datos
db = pymysql.connect(host=os.environ.get('DATABASE_HOST'), user=os.environ.get('DATABASE_USERNAME'), passwd=os.environ.get('DATABASE_PASSWORD'), db=os.environ.get('DATABASE_NAME'))

# obtiene todos los parametros
def getClusterParams():
    cursor = db.cursor()
    sql = """
    SELECT e.emotion_name, c.cluster_name, cp.value_limit, cp.peak_limits, cp.level
    FROM cluster_params cp
    JOIN emotions e ON cp.emotion_id = e.id
    JOIN clusters c ON cp.cluster_id = c.id;
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
    cursor.close()
    return results

## obtiene un texto de manera aleatoria para formar un output
def getOutputText(cluster_levels, instruction):
    texts = {}
    cursor = db.cursor()
    output_raw = ""

    for cluster_name, level in cluster_levels.items():
        cursor.execute("""
            SELECT text FROM cluster_texts 
            WHERE cluster_name = %s AND level = %s AND status = 1
            """, (cluster_name, level))
        
        results = cursor.fetchall()
        if results:
            random_text = random.choice(results)
            texts[cluster_name] = random_text[0]
            output_raw += texts[cluster_name] + "\n"

    cursor.close()
    transofmedText = transformTextAI(texts['extrovertido'], instruction)
    #return output_raw
    return transofmedText

def transformTextAI(text, instruction):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"{instruction}: {text}"}
        ]
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content