from .Image import Image
from typing import Iterable


class ImageGallery:
    def __init__(self, images: Iterable[Image]):
        self.images = images
        
    def json(self) -> dict:
        result = {'type': 'ImageGallery'}
        result['items'] = [image.json() for image in self.images]
        
        return result
        