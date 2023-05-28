from typing import Iterable
from .ui import Button, BigImage


class Response:
    def __init__(self, text: str='', tts: str='', end_session: bool=False,
                 buttons: Iterable=[], card: BigImage | None=None):
        
        self.text = text 
        self.tts = tts
        self.end_session = end_session
        self._version = '1.0'
        self.buttons = list(buttons)
        self.card = card
        
    def add_button(self, button: Button):
        ''' Добавляет одну кнопку '''
        self.buttons.append(button)
            
    def add_buttons(self, buttons: Iterable[Button]):
        ''' Добавляет списк кнопок '''
        self.buttons.extend(buttons)
        
    def json(self):
        result = \
        {
            'response': {
                'text': self.text,
                'tts': self.tts,
                'end_session': self.end_session
            },
            'version': self._version
        }
        if self.buttons:
            result['response']['buttons'] = [button.json() for button in self.buttons]
        if self.card is not None:
            result['response']['card'] = self.card.json()
            
        return result