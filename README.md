# aliceAPI

Библиотека упрощает использование API алисы. Заменя работу со словарями на классы пайтона. Например навык - попугай:

Пример от яндекса
```python
def handler(event):
    text = 'Привет я буду повторять всё что ты скажешь'
    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0:
        text = event['request']['original_utterance']
    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            'end_session': 'false'
        },
    }
```

С использозование библиотеки
```python
from aliceAPI import Request, Response


def handler(event):
    request = Request(event)
    response = Response()

    if request.new:
        response.text = 'Я попугай, повтарю всё что ты скажеш'
    else:
        text = request.command
        response.text = text

    return response.json()

```


## Как разместить навык

Для навыков алисы можно использовать webhook или функции в яндекс облаке. Для Webhook понадобится хостинг и домен, а так
же знания одного из веб фреймворков. Для навыков алисы функции в яндекс облаке бесплатные и их легко использовать
достачно написать функцию обработчик и не нужно замарачиватся с развёртыванием на хостинге. Вот шаблон для яндекс облако
функций, если вставить его в яндекс облако функцию в ответ придёт сообщение "работает". Обратите внимание, handler 
принимает два аргумента второй это контекст функций который нужен для интегриции других сервисов яндекс облако.

[видео урок по размещению навыка в яндекс облаке](https://www.youtube.com/watch?time_continue=1&v=-6Ik2DUWaqI&embeds_referring_euri=https%3A%2F%2Fyandex.ru%2F&source_ve_path=MzY4NDIsMjg2NjY&feature=emb_logo)
### Шаблон
```python
from aliceAPI import Request, Response


def _handler(event):
    """ функция обработчик """
    request = Request(event)
    response = Response()

    # ваш код
    response.text = 'работает'
    
    return response.json()


def handler(event, _):
    """ 
        эта функция предотвращает ситуации когда навык не отвечает. Вместо  HTTP ошибка в ответе webhook: 500 
        показывает error_messge и ошибку если debug=True например: 
        Простите что то пошло не так: TypeError(unsupported operand type(s) for +: 'int' and 'str')   
    """
    error_message = 'Простите что то пошло не так' # текст который будет показыватся при ошбке в коде
    debug = True # показывать ли ошибку. 
    try:
        return _handler(event)
    except Exception as error:
        response = Response(text=error_message) 
        if debug:
            response.text += ': ' + error.__repr__()
        return response.json()

```

## Быстрый старт

`request = Request(event)` - объект нужный для получения парметров запроса

`request.command` - текст сообщения приведённый к нижнему регистру и отчищенный от знаков препинания 

`request.original_utterance` - тест сообщения без изменений

`request.new` - логическое значение, является ли сообщение первым
#
`response = Response()` - объект для формирования ответа
`response.json()` - формирование ответа

`response.text` - текст сообщения

`response.tts`- текст который прочитает алиса может не совпадать с текстом сообщения

`response.end_session` - логическое значение, закончить ли сессию 


### пример который показывает предназначение всего выше перечисленного
```python
from aliceAPI import Request, Response


def handler(event):
    request = Request(event)
    response = Response()

    if request.new: # responce.new используется для приветственного сообщения
        response.text = 'Это привественное сообщение'
    else:
        # если написать привет навык ответит как дела?
        if request.command == 'привет':
            response.text = 'как дела?'
        # если написить 5 навык закончит работу
        elif request.command == '5':
            response.text = "пока"
            response.end_session = True # заканчивает сессию
    
    return response.json() # формирование ответа
```

## Кнопки

Кнопки имеют следёющие параметры

Button()
- `title` - обзательный, тест кнопки, при нажатии отправляется как реплика пользователя
- `hide` - логическое значение, False по умолчанию, hide=True кнопка подсказка, исчезают при новой реплике пользователя, hide=False, кнопка под сообщением не исчезает
- `url`- ссылка которая открывается при нажатии на кнопку
- `payload`- объект который отвравляется в ответ при нажатии кнопки. Работает только для кнопок с hide=True или кнопок
изображний. __**Советую забыть про этот пареметр**__, если вы исползьзовали `payload` вы не можете получить `request.command`.
Тип запроса меняется на "ButtonPressed" только для кнопок с hide=True

Что бы добавить кнопку к ответу `response.add_button()`

Что бы добавить список кнопок к ответу `response.add_buttons()`

## Пример использования кнопок
```python
from aliceAPI import Request, Response, Button


def handler(event):
    request = Request(event)
    response = Response()
    
    # эти кнопки добавляются к каждому ответу
    start_buttons = (
            Button('кнопка', hide=True), # кнопки с hide=True показываются как подсказки 
            Button('кнопки', hide=True)
    )
    response.add_buttons(start_buttons) # добавляет список кнопок

    if request.new:
        response.text = 'Этот навык показывает кнопки'
        
    else:
        if request.command == 'кнопка':
            response.text = 'кнопка'
            response.add_button(Button('эта кнопка скоро исчезнет', hide=True)) 
            # кнопки с hide=True исчезают при следующей реплике пользователя
        elif request.command == 'кнопки':
            # кнопки с hide=False остаются под сообщением
            response.text = 'кнопки'
            response.add_buttons([
                Button('кнопка с сылкой', url='https://yandex.ru'),
                Button('Просто кнопка') 
            ])
    
    return response.json() # формирование ответа

```

## Изображения

Изображения можно загрузить в навык, с помощью консоли или API. И после использовать айди изображения в навыке

### Image

Общий класс изображений имеет следующие атрибуты

Image()
- `image_id` - обязательный, индификатор изображения
- `title` - заголовок изображения
- `description` - описание изображения (не работает с ImageGallery)
- `button` - кнопка изображения

Кнопка изображения отличается от обычной только отсутствием свойства hide. И имеет следующие параметры

ImageButton()
- `text` - текст кнопки при нажатии отвправляется как реплика позьзователя  
- `url` - ссылка котора открывается при нажатии кнопки
- `payload` - объект который отвравляется в ответ при нажатии кнопки. Работает только для кнопок с hide=True или кнопок изображний. Советую забыть про этот пареметр, если вы исползьзовали payload вы не можете получить request.command. Тип запроса меняется на "ButtonPressed"

#### Пример создания изображения
```python
from aliceAPI import Image, ImageButton

# вставить индификатор изображение вместо image_id
image = Image(
    '<image_id>', title='пылесос', 
    description='описание изображения',
    button=ImageButton('ты нажал на изображение')
)
```

Что бы отобразить изображение нужно использовать card. Существует 3 типа card. Можно испозьзовать только один вид card.

- BigImage
- ImageGallery
- ItemsList

Что бы добавить card в ответ `response.card = <BigImage, ImageGallery или ItemList>`

### BigImage

Одно изображение принимет один парамерт `image`

#### Пример создания BigImage
```python
from aliceAPI import Image, ImageButton, BigImage, Request, Response


def handler(event):
    request = Request(event)
    response = Response()
    
    big_image = BigImage(Image(
        # вставить индификатор изображение вместо image_id
        '<image_id>', title='пылесос', 
        description='не забудь нажать',
        button=ImageButton('ты нажал на изображение')
    ))

    response.card = big_image # добавление BigImage в ответ
    
    return response.json() # формирование ответа
```

### ImageGallery

Несколько изображений, не использует description у изображений. Принимает один параметр `images` список изображений.

#### Пример ImageGallery

```python
from aliceAPI import Image, ImageButton, ImageGallery, Request, Response


def handler(event):
    request = Request(event)
    response = Response()
    
    image = Image(
        # вставить индификатор изображение вместо image_id
        '<image_id>', title='пылесос', 
        button=ImageButton('ты нажал на изображение')
    )
    images = [image, image, image] # список изображений
    
    image_gallery = ImageGallery(images)

    response.card = image_gallery # добавление BigImage в ответ
    
    return response.json() # формирование ответа
```

### ItemsList

Список изображений с заголовком принимает слудующие параметры.

ItemsList()

- `images` - обязательный, список изображений
- `title` - заголовок 
- `footer_text` - текст кнопки под ItemsList, использовать вместе с `footer_button` 
- `footer_button` - кнопка под изображением, отображается `footer_text`, но при нажатии отправляется текст кнопки

#### Пример ItemsList
```python
from aliceAPI import Image, ImageButton, ItemsList, Request, Response


def handler(event):
    request = Request(event)
    response = Response()
    
    image = Image(
        # вставить индификатор изображение вместо image_id
        '<image_id>', title='пылесос', 
        description='не забудь нажать',
        button=ImageButton('ты нажал на изображение')
    )
    images = [image, image, image] # список изображений
    
    items_list = ItemsList(images, title='Заголовок',
                           footer_text='текст на нижней кнопке',
                           footer_button=ImageButton(text='ты нажал на кнопку'))

    response.card = items_list # добавление BigImage в ответ
    
    return response.json() # формирование ответа
```



## Запрос Request

запрос содержит следующие атрибуты

- `type` - тип сообщения 
    - "SimpleUtterance" — голосовой ввод.
    - "ButtonPressed" — нажатие кнопки.
    - "AudioPlayer.PlaybackStarted" — событие начала воспроизведения аудиоплеером на умных колонках.
    - "AudioPlayer.PlaybackFinished" — событие завершения воспроизведения.
    - "AudioPlayer.PlaybackNearlyFinished" — событие о скором завершении воспроизведения текущего трека.
    - "AudioPlayer.PlaybackStopped" — остановка воспроизведения.
    - "AudioPlayer.PlaybackFailed" — ошибка воспроизведения.
    - "Purchase.Confirmation" — запрос на подтверждение оплаты в навыке.
    - "Show.Pull" — запрос на чтение данных для шоу.
- `timezone` - название часового пояса например "Europe/Moscow"
- `locale` - язык например "ru-RU"

- `command` - текст сообщения преведённый к нижнему регистру и отчищенный от знаков препинания
- `original_utterance` - текст сообщения
- `message_id` - номер сообщения
- `skill_id` - айди навыка. Можно найти в консоли разработчика

- `new` - является ли сообщение первым. Можно использовать для приветствия
- `application_id` - айди приложения например приложение на телфоне, алиса в баузере, яндекс станция
- `session_id` - айди сесси
- `session_state` - состаяние сессии
- `application_state` - состаяние для отдельного приложения
- `payload` - объект отправленный при нажатии кнопки
- `tokens` - список всех слов в сообщении
- `intents` - интенты
- `entities` - сущности интентов
- `user_id` - айди пользователя
- `access_token` - токен для авторизации
- `user_state` - состаяние пользователя

запрос содержит следующие функции 

- `has_screen()` - возращает True если пользователь может если пользователь может видеть ответ навыка на экране и открывать ссылки в браузере.
- `can_account_linking()`- есть ли пользователя возможность запросить связку аккаунтов.
- `has_audio_player()` - есть ли устройстве пользователя есть аудиоплеер.
- `is_authenticated()` - авторизован ли пользователь 