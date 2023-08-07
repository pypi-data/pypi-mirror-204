from typing import Optional

_figure_number = {}

def get_next_figure_number(type:str):
    if type not in _figure_number:
        _figure_number[type]=0
    _figure_number[type] += 1
    return _figure_number[type]

class Caption:

    def __init__(self, caption, notes: Optional[list[str]] = None, type: str = "Figure"):
        self.caption = caption
        if notes:
            self.notes = notes
        else:
            self.notes = []
        self.type = type
        self.number = get_next_figure_number(type)

    def caption_as_html(self):
        notes_str = ''.join([f'<div class="note"> <i>Note: {n} </i></div>' for n in self.notes])
        return f'<div class="caption-section"><div class="caption"><b>{self.type} {self.number}:</b> {self.caption}</div>{notes_str}</div>'