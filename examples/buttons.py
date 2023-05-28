from aliceAPI import Response, Button


def handler(event):
    response = Response()
    
    response.text = 'кнопки' # без текста кнопки с hide=False не отображаются
    
    buttons_1 = [
        Button('gogle', False, url='https://ya.ru/'), # кнопка - ссылка
        Button('конопка', False), 
        Button('text', False),
    ]
    response.add_buttons(buttons_1) # добовлене первой групы кнопок
    
    buttons_2 = [   
        Button('payload', True, payload={'что-то': ' '}), # кнопка с payload
        Button('подсказка 2', True),
        Button('подсказка 3', True),
    ]
    response.add_buttons(buttons_2) # добавление второй группы кнопок
    
    return response.json()