from aliceAPI import Response, Image, BigImage, ImageButton


def handler(event):
    response = Response()
    
    image_id = '<индификатор изображения>'
    
    button = ImageButton('текст при нажатии',
                        url='https://ya.ru/') # поведение изображения при нажиатии
    image = Image(image_id, title='Заголовок', 
                  description='описание', button=button) # создание изображения
    
    response.card = BigImage(image) # добавление большого изображения
 
    return response.json()