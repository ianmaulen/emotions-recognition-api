def process_clusters(emotion_results_json, cluster_params):
    clusters = {}

    # Mapear los parámetros por cluster
    cluster_determinado_params = [param for param in cluster_params if param['cluster_name'] == 'determinado']
    cluster_extrovertido_params = [param for param in cluster_params if param['cluster_name'] == 'extrovertido']
    cluster_estructurado_params = [param for param in cluster_params if param['cluster_name'] == 'estructurado']
    cluster_creativo_params = [param for param in cluster_params if param['cluster_name'] == 'creativo']
    cluster_racional_params = [param for param in cluster_params if param['cluster_name'] == 'racional']

    # Evaluar cada cluster
    clusters['extrovertido'] = determine_extrovertido(emotion_results_json, cluster_extrovertido_params)
    clusters['determinado'] = determine_determinado(emotion_results_json, cluster_determinado_params)
    clusters['estructurado'] = determine_estructurado(emotion_results_json, cluster_estructurado_params)
    clusters['creativo'] = determine_creativo(emotion_results_json, cluster_creativo_params)
    clusters['racional'] = determine_racional(emotion_results_json, cluster_racional_params)

    print('clusters determinados con exito..')
    return clusters

def determine_extrovertido(emotion_values, cluster_params):
    happy_alto_peaks = next(param['peak_limits'] for param in cluster_params if param['emotion_name'] == 'HAPPY' and param['level'] == 'alto')
    happy_medio_peaks = next(param['peak_limits'] for param in cluster_params if param['emotion_name'] == 'HAPPY' and param['level'] == 'medio')
    happy_alto_value_limit = next(param['value_limit'] for param in cluster_params if param['emotion_name'] == 'HAPPY' and param['level'] == 'alto')
    happy_medio_value_limit = next(param['value_limit'] for param in cluster_params if param['emotion_name'] == 'HAPPY' and param['level'] == 'medio')

    happy_alto_count = len([value for value in emotion_values['HAPPY'] if value >= happy_alto_value_limit])
    happy_medio_count = len([value for value in emotion_values['HAPPY'] if value >= happy_medio_value_limit])

    if happy_alto_count >= happy_alto_peaks:
        print('extrovertido alto')
        return 'alto'
    elif happy_medio_count >= happy_medio_peaks:
        print('extrovertido medio')
        return 'medio'
    else:
        print('extrovertido bajo')
        return 'bajo'

def determine_determinado(emotion_values, cluster_params):
    confused_alto_peaks = next(param['peak_limits'] for param in cluster_params if param['emotion_name'] == 'CONFUSED' and param['level'] == 'alto')
    confused_medio_peaks = next(param['peak_limits'] for param in cluster_params if param['emotion_name'] == 'CONFUSED' and param['level'] == 'medio')
    angry_alto_peaks = next(param['peak_limits'] for param in cluster_params if param['emotion_name'] == 'ANGRY' and param['level'] == 'alto')
    angry_medio_peaks = next(param['peak_limits'] for param in cluster_params if param['emotion_name'] == 'ANGRY' and param['level'] == 'medio')

    confused_alto_value_limit = next(param['value_limit'] for param in cluster_params if param['emotion_name'] == 'CONFUSED' and param['level'] == 'alto')
    confused_medio_value_limit = next(param['value_limit'] for param in cluster_params if param['emotion_name'] == 'CONFUSED' and param['level'] == 'medio')
    angry_alto_value_limit = next(param['value_limit'] for param in cluster_params if param['emotion_name'] == 'ANGRY' and param['level'] == 'alto')
    angry_medio_value_limit = next(param['value_limit'] for param in cluster_params if param['emotion_name'] == 'ANGRY' and param['level'] == 'medio')

    confused_alto_count = len([value for value in emotion_values['CONFUSED'] if value >= confused_alto_value_limit])
    confused_medio_count = len([value for value in emotion_values['CONFUSED'] if value >= confused_medio_value_limit])
    angry_alto_count = len([value for value in emotion_values['ANGRY'] if value >= angry_alto_value_limit])
    angry_medio_count = len([value for value in emotion_values['ANGRY'] if value >= angry_medio_value_limit])
    
    if confused_alto_count <= confused_alto_peaks and angry_alto_count >= angry_alto_peaks:
        return 'alto'
    elif confused_medio_count <= confused_medio_peaks or angry_medio_count >= angry_medio_peaks:
        return 'medio'
    else:
        return 'bajo'

def determine_estructurado(emotion_values, cluster_params):
    calm_alto_peaks = next(param['peak_limits'] for param in cluster_params if param['emotion_name'] == 'CALM' and param['level'] == 'alto')
    sad_alto_peaks = next(param['peak_limits'] for param in cluster_params if param['emotion_name'] == 'SAD' and param['level'] == 'alto')
    calm_medio_peaks = next(param['peak_limits'] for param in cluster_params if param['emotion_name'] == 'CALM' and param['level'] == 'medio')
    sad_medio_peaks = next(param['peak_limits'] for param in cluster_params if param['emotion_name'] == 'SAD' and param['level'] == 'medio')

    calm_alto_value_limit = next(param['value_limit'] for param in cluster_params if param['emotion_name'] == 'CALM' and param['level'] == 'alto')
    sad_alto_value_limit = next(param['value_limit'] for param in cluster_params if param['emotion_name'] == 'SAD' and param['level'] == 'alto')
    calm_medio_value_limit = next(param['value_limit'] for param in cluster_params if param['emotion_name'] == 'CALM' and param['level'] == 'medio')
    sad_medio_value_limit = next(param['value_limit'] for param in cluster_params if param['emotion_name'] == 'SAD' and param['level'] == 'medio')

    calm_alto_count = len([value for value in emotion_values['CALM'] if value >= calm_alto_value_limit])
    calm_medio_count = len([value for value in emotion_values['CALM'] if value >= calm_medio_value_limit])
    sad_alto_count = len([value for value in emotion_values['SAD'] if value >= sad_alto_value_limit])
    sad_medio_count = len([value for value in emotion_values['SAD'] if value >= sad_medio_value_limit])
    
    if calm_alto_count >= calm_alto_peaks and sad_alto_count >= sad_alto_peaks:
        return 'alto'
    elif calm_medio_count >= calm_medio_peaks or sad_medio_count >= sad_medio_peaks:
        return 'medio'
    else:
        return 'bajo'

def determine_creativo(emotion_values, cluster_params):
    surprised_alto_peaks = next(param['peak_limits'] for param in cluster_params if param['emotion_name'] == 'SURPRISED' and param['level'] == 'alto')
    surprised_medio_peaks = next(param['peak_limits'] for param in cluster_params if param['emotion_name'] == 'SURPRISED' and param['level'] == 'medio')

    surprised_alto_value_limit = next(param['value_limit'] for param in cluster_params if param['emotion_name'] == 'SURPRISED' and param['level'] == 'alto')
    surprised_medio_value_limit = next(param['value_limit'] for param in cluster_params if param['emotion_name'] == 'SURPRISED' and param['level'] == 'medio')

    surprised_alto_count = len([value for value in emotion_values['SURPRISED'] if value >= surprised_alto_value_limit])
    surprised_medio_count = len([value for value in emotion_values['SURPRISED'] if value >= surprised_medio_value_limit])
    
    if surprised_alto_count >= surprised_alto_peaks:
        return 'alto'
    elif surprised_medio_count >= surprised_medio_peaks:
        return 'medio'
    else:
        return 'bajo'

def determine_racional(emotion_values, cluster_params):
    calm_alto_peaks = next(param['peak_limits'] for param in cluster_params if param['emotion_name'] == 'CALM' and param['level'] == 'alto')
    sad_alto_peaks = next(param['peak_limits'] for param in cluster_params if param['emotion_name'] == 'SAD' and param['level'] == 'alto')
    calm_medio_peaks = next(param['peak_limits'] for param in cluster_params if param['emotion_name'] == 'CALM' and param['level'] == 'medio')
    sad_medio_peaks = next(param['peak_limits'] for param in cluster_params if param['emotion_name'] == 'SAD' and param['level'] == 'medio')

    calm_alto_value_limit = next(param['value_limit'] for param in cluster_params if param['emotion_name'] == 'CALM' and param['level'] == 'alto')
    calm_medio_value_limit = next(param['value_limit'] for param in cluster_params if param['emotion_name'] == 'CALM' and param['level'] == 'medio')
    sad_alto_value_limit = next(param['value_limit'] for param in cluster_params if param['emotion_name'] == 'SAD' and param['level'] == 'alto')
    sad_medio_value_limit = next(param['value_limit'] for param in cluster_params if param['emotion_name'] == 'SAD' and param['level'] == 'medio')

    calm_alto_count = len([value for value in emotion_values['CALM'] if value >= calm_alto_value_limit])
    calm_medio_count = len([value for value in emotion_values['CALM'] if value >= calm_medio_value_limit])
    sad_alto_count = len([value for value in emotion_values['SAD'] if value >= sad_alto_value_limit])
    sad_medio_count = len([value for value in emotion_values['SAD'] if value >= sad_medio_value_limit])
    
    if calm_alto_count >= calm_alto_peaks and sad_alto_count >= sad_alto_peaks:
        return 'alto'
    elif calm_medio_count >= calm_medio_peaks or sad_medio_count >= sad_medio_peaks:
        return 'medio'
    else:
        return 'bajo'