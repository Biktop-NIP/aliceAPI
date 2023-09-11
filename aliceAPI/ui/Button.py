from typing import Optional


class Button:
    def __init__(self, title: str, hide: bool = False,
                 payload: Optional[dict] = None, url: Optional[str] = None):
        
        self.title = title
        self.hide = hide
        self.payload = payload
        self.url = url
        
    def json(self) -> dict:
        result = {
            'title': self.title,
            'hide': self.hide 
        }
        if self.payload is not None:
            result['payload'] = self.payload
        if self.url is not None:
            result['url'] = self.url
        return result
            