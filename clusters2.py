from config import getClusterParams

def process_clusters(emotion_results_json):
    db_params = getClusterParams()
    #declaración de variables
    happyLimitExtrovertido = find_limit('HAPPY' , 'extrovertido', db_params)
    happyPeaksExtrovertido = find_peaks('HAPPY' , 'extrovertido', db_params)

    confusedLimitDeterminado = find_limit('CONFUSED' , 'determinado', db_params)
    confusedPeaksDeterminado = find_peaks('CONFUSED' , 'determinado', db_params)
    angryLimitDeterminado = find_limit('ANGRY' , 'determinado', db_params)
    angryPeaksDeterminado = find_peaks('ANGRY' , 'determinado', db_params)

    calmLimitEstructurado = find_limit('CALM' , 'estructurado', db_params)
    calmPeaksEstructurado = find_peaks('CALM' , 'estructurado', db_params)
    sadLimitEstructurado = find_limit('SAD' , 'estructurado', db_params)
    sadPeaksEstructurado = find_peaks('SAD' , 'estructurado', db_params)

    surprisedLimitCreativo = find_limit('SURPRISED' , 'creativo', db_params)
    surprisedPeaksCreativo = find_peaks('SURPRISED' , 'creativo', db_params)

    calmLimitRacional = find_limit('CALM' , 'racional', db_params)
    calmPeaksRacional = find_peaks('CALM' , 'racional', db_params)
    sadLimitRacional = find_limit('SAD' , 'racional', db_params)
    sadPeaksRacional = find_peaks('SAD' , 'racional', db_params)

    clusters = {
        'extrovertido': 0,
        'determinado': 0,
        'estructurado': 0,
        'creativo': 0,
        'racional': 0
    }

    # EXTROVERTIDO: 1 sólo si "happy" tiene 1 o más valores sobre 30%. Si no se cumple esta condición, entonces "extrovertido"=0.
    clusters['extrovertido'] = 1 if (len([value for value in emotion_results_json.get('HAPPY', []) if value > happyLimitExtrovertido]) >= happyPeaksExtrovertido) else 0

    # DETERMINADO: 1 sólo si "confused" no tiene más de dos valores sobre 60%. Además, "angry" debe tener dos o más valores sobre 50%. Si no se cumple esta condición, entonces "determinado"=0.
    clusters['determinado'] = 1 if (len([value for value in emotion_results_json.get('CONFUSED', []) if value > confusedLimitDeterminado]) <= confusedPeaksDeterminado) and (len([value for value in emotion_results_json.get('ANGRY', []) if value > angryLimitDeterminado]) >= angryPeaksDeterminado) else 0
    
    # ESTRUCTURADO: 1 sólo si "calm" tiene 5 o más valores sobre 80% y "sad" tiene 3 o más valores sobre 20%. Si no se cumple esta condición, entonces "estructurado"=0.
    clusters['estructurado'] = 1 if (len([value for value in emotion_results_json.get('CALM', []) if value > calmLimitEstructurado]) >= calmPeaksEstructurado) and (len([value for value in emotion_results_json.get('SAD', []) if value > sadLimitEstructurado]) >= sadPeaksEstructurado) else 0

    # CREATIVO: 1 sólo si "surprised" tiene 1 o más valores sobre 20%. Si no se cumple esta condición, entonces "creativo"=0. 
    clusters['creativo'] = 1 if (len([value for value in emotion_results_json.get('SURPRISED', []) if value > surprisedLimitCreativo]) >= surprisedPeaksCreativo) else 0

    # RACIONAL: 1 sólo si "calm" tiene 10 o más valores sobre 80% y "sad" tiene 3 o más valores sobre 50%. Si no se cumple esta condición, entonces "estructurado"=0.
    clusters['racional'] = 1 if (len([value for value in emotion_results_json.get('CALM', []) if value > calmLimitRacional]) >= calmPeaksRacional) and (len([value for value in emotion_results_json.get('SAD', []) if value > sadLimitRacional]) >= sadPeaksRacional) else 0

    print(f'Se han obtenido los clusters de personalidad')
    return clusters

# funcion para encontrar los limites
def find_limit(emotion_value, cluster_value, data):
    try:
        matching_obj = next((obj for obj in data if obj['emotion_name'] == emotion_value and obj['cluster_name'] == cluster_value), None)
        
        return matching_obj['limit'] if matching_obj else None
    except Exception as e:
        print(e)
# funcion para encontrar los peaks
def find_peaks(emotion_value, cluster_value, data):
    try:
        matching_obj = next((obj for obj in data if obj['emotion_name'] == emotion_value and obj['cluster_name'] == cluster_value), None)

        return matching_obj['peaks'] if matching_obj else None
    except Exception as e:
        print(e)