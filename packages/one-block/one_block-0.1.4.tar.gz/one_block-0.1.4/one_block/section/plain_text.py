from one_block.base import Base, BaseText


class PlainText(Base):
    def __init__(self, text, emoji=True):
        self.base = BaseText(text, emoji)

    def json(self):
        return {
            'type': 'section',
            'text': self.base.json()
        }
