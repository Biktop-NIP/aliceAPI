from typing import Iterable
from .ui import Button, BigImage


class Response:
    def __init__(self, text: str='', tts: str='', end_session: bool=False,
                 buttons: Iterable=[], card: BigImage | None=None,
                 session_state: dict | None=None, user_state: dict | None=None,
                 app_state: dict | None=None):
        
        self.text = text 
        self.tts = tts
        self.end_session = end_session
        self._version = '1.0'
        self.buttons = list(buttons)
        self.card = card
        self.session_state = session_state
        self.user_state = user_state
        self.app_state = app_state
        
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
        if self.session_state is not None:
            result['session_state'] = self.session_state
        if self.user_state is not None:
            result['user_state_update'] = self.user_state
        if self.app_state is not None:
            result['application_state'] = self.app_state
            
        return result