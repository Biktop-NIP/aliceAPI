import os


IDENTIFIER = os.getenv('SKILL_IDENTIFIER')
TOCEN = os.getenv('DIALOGS_AUTH_TOCEN')

URL_IMAGE = 'https://dialogs.yandex.net/api/v1/skills/'+IDENTIFIER+'/images/'
URL_SOUNDS = 'https://dialogs.yandex.net/api/v1/skills/'+IDENTIFIER+'/sounds/'
URL_STATUS = 'https://dialogs.yandex.net/api/v1/status'
