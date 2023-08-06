from one_block import accessory
from one_block.base import Base, BaseText


class DatePicker(Base):
    def __init__(self, text, action_id, initial_date=None, placeholder=None):
        self.text = BaseText(text, markdown=True)
        self.accessory = accessory.DatePicker(action_id, initial_date, placeholder)

    def json(self):
        return {
            'type': 'section',
            'text': self.text.json(),
            'accessory': self.accessory.json()
        }


class TimePicker(Base):
    def __init__(self, text, action_id, initial_time=None, placeholder=None):
        self.text = BaseText(text, markdown=True)
        self.accessory = accessory.DatePicker(action_id, initial_time, placeholder)

    def json(self):
        return {
            'type': 'section',
            'text': self.text.json(),
            'accessory': self.accessory.json()
        }
