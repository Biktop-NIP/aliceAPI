from aliceAPI import Response, Button


def handler(event):
    response = Response()
    
    response.text = 'кнопки'
    
    button_1 = Button('кнопка', True) # сздание кнопки
    response.add_button(button_1)     # добавление кнопки
    
    response.add_button(Button('подсказка', False))
    
    return response.json()