from one_block.base import Base, BaseText


class Header(Base):
    def __init__(self, text):
        self.text = BaseText(text)

    def json(self):
        return {
            'type': 'header',
            'text': self.text.json()
        }
