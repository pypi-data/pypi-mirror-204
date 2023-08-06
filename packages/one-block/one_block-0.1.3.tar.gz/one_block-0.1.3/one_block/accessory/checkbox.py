from typing import List

from one_block.accessory.accessory import Accessory
from one_block.accessory.option import Option


class Checkbox(Accessory):
    def __init__(self, action_id: str, options: List[Option]):
        self.action_id = action_id
        self.options = options

    def json(self):
        return {
            'type': 'checkboxes',
            'options': [
                option.json() for option in self.options
            ],
            'action_id': self.action_id
        }
