import abc
from typing import List


class Base(abc.ABC):
    def json(self):
        raise NotImplementedError


class BaseText(Base):
    def __init__(self, text: str, markdown: bool = False, emoji: bool = True):
        self.text = text
        self.markdown = markdown
        self.emoji = emoji

    def json(self):
        block_type = 'mrkdwn' if self.markdown else 'plain_text'
        base = {
            'type': block_type,
            'text': self.text,
        }
        if not self.markdown:
            base['emoji'] = self.emoji
        return base


def get_blocks(blocks: List[Base]):
    return [b.json() for b in blocks]
