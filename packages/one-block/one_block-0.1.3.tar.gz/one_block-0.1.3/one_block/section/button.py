from one_block import accessory
from one_block.accessory import ButtonStyle
from one_block.base import Base, BaseText


class Button(Base):
    def __init__(self, text, button_label, action_id, value, url=None, style=ButtonStyle.DEFAULT):
        self.text = BaseText(text, markdown=True)
        self.accessory = accessory.Button(button_label, action_id, value, url=url, style=style)

    def json(self):
        return {
            'type': 'section',
            'text': self.text.json(),
            'accessory': self.accessory.json()
        }
