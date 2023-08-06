from one_block import accessory
from one_block.base import Base, BaseText


class Checkbox(Base):
    def __init__(self, text, action_id, options):
        self.text = BaseText(text, markdown=True)
        self.accessory = accessory.Checkbox(action_id, options)

    def json(self):
        return {
            'type': 'section',
            'text': self.text.json(),
            'accessory': self.accessory.json()
        }
