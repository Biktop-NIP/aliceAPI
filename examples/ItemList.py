from aliceAPI import Response, Image, ItemsList, ImageButton

def handler(event, context):
    response = Response()
    
    image_id = '<индификатор изображения>'
    
    button = ImageButton('текст при нажатии',
                        url='https://ya.ru/') # поведение изображения при нажиатии
    image = Image(image_id, title='Заголовок',
                  description='опсание', button=button) # создание изображения
    
    images = (image, image, image, image) # списик изображений 
    
    foot_button = ImageButton('нижняя кнопка')
    response.card = ItemsList(title='заголовок', images=images, 
                              footer_text='нижний заголовок',
                              footer_button=foot_button) # добавление списка изображений
 
    return response.json()