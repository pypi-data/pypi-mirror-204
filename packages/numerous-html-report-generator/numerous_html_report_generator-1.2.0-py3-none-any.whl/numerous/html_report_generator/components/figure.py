from ..block import Block
from typing import Optional
from ..caption import Caption


class Figure(Block):

    def __init__(self, caption:str, notes: Optional[list[str]] = None):
        self.caption = Caption(caption=caption, notes=notes, type="Figure")

    def _as_html_figure_content(self):
        return ""

    def _as_html(self):
        return f"{self._as_html_figure_content() + self.caption.caption_as_html()}"

