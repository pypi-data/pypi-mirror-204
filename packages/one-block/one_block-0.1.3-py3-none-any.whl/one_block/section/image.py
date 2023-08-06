from one_block import base
from one_block import image


class Image(base.Base):
    def __init__(self, text, image_url, alt_text):
        self.text = base.BaseText(text, markdown=True)
        self.image = image.Image(image_url=image_url, alt_text=alt_text)

    def json(self):
        return {
            'type': 'section',
            'text': self.text.json(),
            'accessory': self.image.json()
        }
