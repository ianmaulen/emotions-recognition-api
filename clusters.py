def process_clusters(emotion_results_json):
    clusters = {
        'extrovertido': 0,
        'determinado': 0,
        'estructurado': 0,
        'creativo': 0,
        'racional': 0
    }

    # Podar aquellas emociones que no tienen más de 5 puntos porcentuales de variación
    pruned_emotions = [emotion for emotion, values in emotion_results_json.items() if max(values) - min(values) <= 15]

    # Podar las emociones que no superen el 8%
    pruned_emotions += [emotion for emotion, values in emotion_results_json.items() if max(values) <= 10]

    # Reglas para asignar valores a los clusters extrovertido, creativo, racional
    clusters['extrovertido'] = 0 if 'HAPPY' in pruned_emotions else 1
    clusters['creativo'] = 0 if 'SURPRISED' in pruned_emotions else 1
    clusters['racional'] = 1 if len(set(['CONFUSED', 'SAD', 'SURPRISED']).difference(pruned_emotions)) in [2, 3] else 0

    # Reglas complejas para 'determinado'
    if 'CONFUSED' in emotion_results_json and len([1 for i in range(len(emotion_results_json['CONFUSED']) - 1) if abs(emotion_results_json['CONFUSED'][i] - emotion_results_json['CONFUSED'][i + 1]) > 50]) >= 2:
        clusters['determinado'] = 0
    elif 'ANGRY' in emotion_results_json and len([1 for i in range(len(emotion_results_json['ANGRY']) - 1) if abs(emotion_results_json['ANGRY'][i] - emotion_results_json['ANGRY'][i + 1]) > 50]) >= 2:
        clusters['determinado'] = 1

    # Reglas complejas para 'estructurado'
    if 'CALM' in emotion_results_json and len([1 for i in range(len(emotion_results_json['CALM']) - 1) if abs(emotion_results_json['CALM'][i] - emotion_results_json['CALM'][i + 1]) > 50]) >= 2:
        if 'FEAR' in emotion_results_json and len([1 for i in range(len(emotion_results_json['FEAR']) - 1) if abs(emotion_results_json['FEAR'][i] - emotion_results_json['FEAR'][i + 1]) > 10]) >= 1:
            clusters['estructurado'] = 1
        elif 'SAD' in emotion_results_json and len([1 for i in range(len(emotion_results_json['SAD']) - 1) if abs(emotion_results_json['SAD'][i] - emotion_results_json['SAD'][i + 1]) > 10]) >= 1:
            clusters['estructurado'] = 1

    return clusters