from typing import Optional, List, AnyStr
from .section import Section

class Card(Section):
    """
    Create a card that can be formatted with html classes, and which may have content

    Args:
        id: the id applied to the card
        classes: the html classes to apply to the card
    """
    def __init__(self, id: Optional[AnyStr] = None, classes: Optional[List | AnyStr] = None):
        """

        """
        super().__init__(section_title="")
        self.id = id
        self.classes = classes

    def _as_html(self):
        html = f"<div class={self.classes} id={self.id}>"
        for item in self.content.values():
            html += item._as_html()
        html += '</div>'
        return html