import re

#función que evalúa las expresiones
def safe_eval(expression, variables):
    # Función para reemplazar divisiones por cero
    def replace_zero_div(match):
        divisor = match.group(1)
        return f'/ max({divisor}, 1)'

    # Expresión regular para encontrar divisores
    division_pattern = r'/\s*\(([^)]+)\)'

    # Reemplazar divisiones por cero en la expresión
    modified_expression = re.sub(division_pattern, replace_zero_div, expression)

    # Evaluar la expresión modificada
    return eval(modified_expression, {}, variables)

def process_clusters(emotion_points, cluster_params):
    emotion_sums = {}

    # Verificar que emotion_points sea un diccionario
    if isinstance(emotion_points, dict):
        # Sumar los puntajes de las emociones
        for emotion, scores in emotion_points.items():
            if isinstance(scores, list):  # Asegurarse de que scores sea una lista
                emotion_sums[emotion] = sum(scores)  # Sumar todos los puntajes de la emoción
            else:
                print(f"Error: Los puntajes para {emotion} no son una lista.")
    else:
        print("Error: emotion_points debe ser un diccionario.")

    cluster_data = {}

    #evalúo cada item y su operacion
    for cluster, data in cluster_params.items():
        try:
            # Evaluar la operación usando la función segura
            points = safe_eval(data['operacion'], emotion_sums)

            if points >= data['alto']:
                level = 'alto'
            elif points > data['bajo']:
                level = 'medio'
            else:
                level = 'bajo'

            # Almacenar en un solo objeto
            cluster_data[cluster] = {'level': level, 'points': points}
        except NameError as e:
            print(f"Error en la operación para {cluster}: {e}")

    return cluster_data
