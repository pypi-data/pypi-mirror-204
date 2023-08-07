from bs4 import BeautifulSoup
from ..block import Block

class Section(Block):
    """

    Args:
        section_title (str):

    Attributes:
        section_title (str):

        content (dict):
    """

    def __init__(self,
                 section_title: str):

        self.section_title = section_title
        self.content = {}

    def set_content(self, content: dict):
        self.check_content(content)
        self.content = content

    def add_content(self, content: dict):
        self.check_content(content)
        self.content.update(content)

    def check_content(self, content: dict):
        assert type(content) == dict
        #for block in content.values():
        #    assert isinstance(block, Block), f"Each item in the content should be a Block, this item has type {type(block)}"

    def _as_html(self):
        html = f"<div><h1 class=\"section_title editable\">{self.section_title}</h1></div>"
        for item in self.content.values():
            html += item._as_html()

        return html
