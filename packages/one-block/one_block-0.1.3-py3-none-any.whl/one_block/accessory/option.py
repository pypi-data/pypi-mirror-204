from one_block.accessory import Accessory
from one_block.base import BaseText


class Option(Accessory):
    def __init__(self, item: str, value=None, description=None, markdown=False):
        self.item = BaseText(item, markdown=markdown)
        value = value or item
        self.description = BaseText(description, markdown=True) if description else None
        self.value = value

    def json(self):
        base = {
            'text': self.item.json(),
            'value': self.value
        }
        if self.description:
            base['description'] = self.description.json()
        return base
