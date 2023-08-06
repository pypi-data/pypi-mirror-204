import enum
from typing import Optional

from one_block import base
from one_block.accessory import Accessory


class ButtonStyle(enum.Enum):
    DEFAULT = None
    PRIMARY = 'primary'
    DANGER = 'danger'


class Button(Accessory):
    def __init__(self, label: str, action_id: str, value: str, url: Optional[str] = None,
                 style: ButtonStyle = ButtonStyle.DEFAULT):
        self.label = base.BaseText(label)
        self.action_id = action_id
        self.value = value
        self.url = url
        self.style = style

    def json(self):
        blocks = {
            'type': 'button',
            'text': self.label.json(),
            'value': self.value,
            'action_id': self.action_id
        }
        if self.url:
            blocks['url'] = self.url
        if self.style != ButtonStyle.DEFAULT:
            blocks['style'] = self.style.value
        return blocks
