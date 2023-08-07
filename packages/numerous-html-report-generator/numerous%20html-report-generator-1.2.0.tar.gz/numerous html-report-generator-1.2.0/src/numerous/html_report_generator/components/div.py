from numerous.html_report_generator.block import Block


class Div(Block):
    """

        Args:
            html (str):

        Attributes:
            html (str):
    """
    def __init__(self, html, **kwargs):

        self.html = html
        self.kwargs = kwargs

    def _as_html(self):
        modifiers=[]

        for k, v in self.kwargs.items():
            modifiers.append(f'{k}="{v}"')

        return f"<div {' '.join(modifiers)}>{self.html}</div>"
