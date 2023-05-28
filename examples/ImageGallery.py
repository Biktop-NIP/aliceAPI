from aliceAPI import Response, Image, ImageGallery, ImageButton


def handler(event, context):
    response = Response()
    
    image_id = '<индификатор изображения>'
    
    button = ImageButton('текст при нажатии',
                        url='https://ya.ru/') # поведение изображения при нажиатии
    image = Image(image_id, title='Заголовок', button=button) # создание изображения
    
    images = (image, image, image, image) # списик изображений 
    
    response.card = ImageGallery(images) # добавление галерии изображений
 
    return response.json()