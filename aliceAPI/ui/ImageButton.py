from typing import Optional


class ImageButton:
    def __init__(self, text: str, payload: Optional[dict] = None, url: Optional[str] = None):
        
        self.text = text
        self.payload = payload
        self.url = url
        
    def json(self) -> dict:
        result = {
            'text': self.text,
        }
        if self.payload is not None:
            result['payload'] = self.payload
        if self.url is not None:
            result['url'] = self.url
        return result
            