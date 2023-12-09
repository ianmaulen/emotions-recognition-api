def process_clusters(emotion_results_json):
    clusters = {
        'extrovertido': 0,
        'determinado': 0,
        'estructurado': 0,
        'creativo': 0,
        'racional': 0
    }
    # Aplicar podas (se pueden agregar más reglas, se deben añadir las emociones podadas a pruned_emotions):
    # 1.- Podar aquellas emociones que no tienen más de 'X' puntos porcentuales de variación (5 pts)
    pruned_emotions = [emotion for emotion, values in emotion_results_json.items() if max(values) - min(values) <= 5]
    # 2.- Podar las emociones que no superen el 'X'%
    pruned_emotions += [emotion for emotion, values in emotion_results_json.items() if max(values) <= 10]

    # EXTROVERTIDO, CREATIVO, RACIONAL:
    # 3.- Si Happy no fue podada, entonces "extrovertido" = 1. De lo contrario extrovertido = 0.
    clusters['extrovertido'] = 0 if 'HAPPY' in pruned_emotions else 1
    # 6.- Si surprised no fue podada, entonces "creativo"=1. De lo contrario, creativo=0.
    clusters['creativo'] = 0 if 'SURPRISED' in pruned_emotions else 1
    # 7.- tienen que haber sobrevivido a la poda dos o tres de las siguientes: confused, sad, surprised, entonces "racional" = 1. De lo contrario = 0 
    clusters['racional'] = 1 if len(set(['CONFUSED', 'SAD', 'SURPRISED']).difference(pruned_emotions)) in [2, 3] else 0

    # DETERMINADO:
    # comienzo de condicionales:  
    if ('CONFUSED' in emotion_results_json) and ('ANGRY' in emotion_results_json):
        # determinacion de max1 y min1 de confused
        confused = emotion_results_json['CONFUSED'].copy()
        max_confused1, min_confused1 = max(confused), min(confused)
        confused = [value for value in confused if value not in [max_confused1, min_confused1]]
        # determinacion de max1 y min1 de angry
        angry = emotion_results_json['ANGRY'].copy()
        max_angry1, min_angry1 = max(angry), min(angry)
        angry = [value for value in angry if value not in [max_angry1, min_angry1]]
        # determinacion de max2 y min2 de confused y angry
        max_confused2, min_confused2 = max(confused), min(confused)
        max_angry2, min_angry2 = max(angry), min(angry)
        # Si Confused tiene dos o más oscilaciones de más de 50%, entonces "determinado" = 0.
        if ((max_confused1 - min_confused1 >= 50) and (max_confused2 - min_confused2 >= 50)):
            clusters['determinado'] = 0
        # De lo contrario, si angry tiene dos o más oscilaciones sobre 50% o dos de 25% y confused podado determinado = 1
        elif ( ( ((max_angry1 - min_angry1) >= 50) and ((max_angry2 - min_angry2) >= 50) ) 
                or ( ((max_angry1 - min_angry1) >= 25) and ((max_angry2 - min_angry2) >= 25) 
                    and ('CONFUSED' in pruned_emotions) ) ):
                clusters['determinado'] = 1

    # ESTRUCTURADO
    # comienzo de condicionales:
    if 'CALM' in emotion_results_json and 'FEAR' in emotion_results_json and 'SAD' in emotion_results_json:
        # determinacion de max1 y min1 de calm
        calm = emotion_results_json['CALM'].copy()
        max_calm1, min_calm1 = max(calm), min(calm)
        calm = [value for value in calm if value not in [max_calm1, min_calm1]]
        # determinacion de max1 y min1 de fear
        fear = emotion_results_json['FEAR'].copy()
        max_fear1, min_fear1 = max(fear), min(fear)
        fear = [value for value in fear if value not in [max_fear1, min_fear1]]
        # determinacion de max1 y min1 de sad
        sad = emotion_results_json['CALM'].copy()
        max_sad1, min_sad1 = max(sad), min(sad)
        sad = [value for value in sad if value not in [max_sad1, min_sad1]]
        # determinacion de max2 y min2 de calm, fear y sad
        max_calm2, min_calm2 = max(calm), min(calm)
        max_fear2, min_fear2 = max(fear), min(fear)
        max_sad2, min_sad2 = max(sad), min(sad)
        # Si calm tiene dos o más oscilaciones de 50%
        if ( ((max_calm1 - min_calm1 >= 50) and (max_calm2 - min_calm2 >= 50)) 
            and ( ((max_fear1 - min_fear1 >= 10) and (max_fear2 - min_fear2 >= 10)) 
                or ((max_sad1 - min_sad1 >= 10) and (max_sad2 - min_sad2 >= 10))) ):
            clusters['estructurado'] = 1
    
    return clusters