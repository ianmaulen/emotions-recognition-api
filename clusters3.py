def compare(value, restriction, limit):
    if restriction == '>=':
        return value >= limit
    elif restriction == '>':
        return value > limit
    elif restriction == '<=':
        return value <= limit
    elif restriction == '<':
        return value < limit
    else:
        raise ValueError(f"Restricción no soportada: {restriction}")

def process_clusters(emotion_results_json, cluster_params):
    clusters = {param['cluster_name']: 'bajo' for param in cluster_params}  # Valor por defecto es 'bajo'
    
    for param in cluster_params:
        emotion_values = [value for value in emotion_results_json.get(param['emotion_name'], []) if compare(value, param['restriction'], param['limits'])]
        print(f"Evaluando {param['cluster_name']} con {param['emotion_name']}: {emotion_values}")
        
        if param['cluster_name'] == 'determinado':
            confused_values = len([value for value in emotion_results_json.get('CONFUSED', []) if value > 60])
            angry_values = len([value for value in emotion_results_json.get('ANGRY', []) if value > 50])
            if confused_values <= 2 and angry_values >= 2:
                clusters['determinado'] = 'alto'
            elif confused_values <= 2 or angry_values >= 2:
                if clusters['determinado'] != 'alto':
                    clusters['determinado'] = 'medio'
            else:
                clusters['determinado'] = 'bajo'
        else:
            if param['levels'] == 'alto' and len(emotion_values) >= param['peaks']:
                clusters[param['cluster_name']] = 'alto'
            elif param['levels'] == 'medio' and len(emotion_values) >= param['peaks']:
                if clusters[param['cluster_name']] != 'alto':
                    clusters[param['cluster_name']] = 'medio'
            elif param['levels'] == 'bajo' and len(emotion_values) < param['peaks']:
                if clusters[param['cluster_name']] == 'bajo':
                    clusters[param['cluster_name']] = 'bajo'
    
    print(f'Se han procesado los clusters de personalidad')
    return clusters