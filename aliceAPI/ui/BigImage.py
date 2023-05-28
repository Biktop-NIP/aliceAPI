from .Image import Image


class BigImage:
    def __init__(self, image: Image):
        self.image = image 
    
    def json(self):
        result = { 'type': 'BigImage' }
        result.update(self.image.json())
        
        return result
    