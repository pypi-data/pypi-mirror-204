from one_block.base import Base, BaseText


class Markdown(Base):
    def __init__(self, text):
        self.base = BaseText(text, markdown=True)

    def json(self):
        return {
            'type': 'section',
            'text': self.base.json()
        }
