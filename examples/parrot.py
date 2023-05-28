from aliceAPI import Response


def handler(event):
    text = event['request']['command'] # текст введённый или сказанный пользователем
    
    response = Response()
    
    if event['session']['message_id'] == 0: # условие верное когда пользователь заходит в навык
        response.text = 'Я попугай. Я буду повторять все твои фразы'
    else:
        response.text = text               # изменение текста в ответе пользователю
    
    return response.json()