class Request:
    def __init__(self, request: dict):
        self.request = request
        self.type = request['request']['type']
        self.meta = request['meta']

        self.message_id = request['session']['message_id']
        self.skill_id = request['session']['skill_id']
        self.session_id = request['session']['session_id']
        self.application_id = request['session']['application']['application_id']
        self.new = request['session']['new']

        self.session_state = request['state']['session']
        self.application_state = request['state']['application']

        if self.type == 'SimpleUtterance':
            self.command = request['request']['command']
            self.original_utterance = request['request']['original_utterance']
        elif self.type == 'ButtonPressed':
            self.payload = request['request']['payload']

        if self.type in ['SimpleUtterance', 'ButtonPressed']:
            self.tokens = request['request']['nlu']['tokens']
            self.entities = request['request']['nlu']['entities']
            self.intents = request['request']['nlu']['intents']

        try:
            self.user_id = request['session']['user']['user_id']
            self.access_token = request['session']['user']['access_token']
            self.user_state = request['state']['user']
        except: pass

    def has_screen(self) -> bool:
        """ возращает True если пользователь может если пользователь может видеть ответ навыка на экране и открывать ссылки в браузере. """
        return 'screen' in self.request['meta']['interfaces']

    def can_account_linking(self) -> bool:
        """ У пользователя есть возможность запросить связку аккаунтов. """
        return 'account_linking' in self.request['meta']['interfaces']

    def has_audio_player(self) -> bool:
        """ На устройстве пользователя есть аудиоплеер. """
        return 'audio_player' in self.request['meta']['interfaces']

    def is_authenticated(self) -> bool:
        return 'user' in self.request['session']
