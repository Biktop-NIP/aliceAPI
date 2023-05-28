class ImageButton:
    def __init__(self, text: str, payload: dict | None=None, url: str | None=None):
        
        self.text = text
        self.payload = payload
        self.url = url
        
    def json(self):
        result = {
            'text': self.text,
        }
        if self.payload is not None:
            result['payload'] = self.payload
        if self.url is not None:
            result['url'] = self.url
        return result
            