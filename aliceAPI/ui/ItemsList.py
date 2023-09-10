from .Image import Image
from typing import Iterable
from .Button import Button
from typing import Optional


class ItemsList:
    def __init__(self, images: Iterable[Image], title: Optional[str] = None,
                 footer_text: Optional[str] = None, footer_button: Optional[Button] = None):
        
        self.images = images
        self.title = title
        self.footer_text = footer_text
        self.footer_button = footer_button
        
    def json(self) -> dict:
        result = {'type': 'ItemsList'}
        if self.title is not None:
            result['header'] = {}
            result['header']['text'] = self.title
        if self.footer_text is not None:
            result['footer'] = {}
            result['footer']['text'] = self.footer_text
            if self.footer_button is not None:
                result['footer']['button'] = self.footer_button.json()
            
        result['items'] = [image.json() for image in self.images]
        
        return result
        