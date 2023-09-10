from .ImageButton import ImageButton
from typing import  Optional


class Image:
    def __init__(self, image_id: str, title: Optional[str] = None,
                 description: Optional[str] = None, button: Optional[ImageButton] = None):
        
        self.image_id = image_id
        self.title = title
        self.description = description
        self.button = button
        
    def json(self) -> dict:
        result = {'image_id': self.image_id}
        if self.title is not None: 
            result['title'] = self.title 
        if self.description is not None: 
            result['description'] = self.description 
        if self.button is not None:
            result['button'] = self.button.json()
                
        return result
        