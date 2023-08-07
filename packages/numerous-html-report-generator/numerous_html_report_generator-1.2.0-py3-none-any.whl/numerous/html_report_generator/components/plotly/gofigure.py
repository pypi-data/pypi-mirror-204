from ..figure import Figure
from plotly import graph_objects as go
from plotly.basedatatypes import BaseTraceType
from typing import Union, Optional
def wrap_div(html, class_=None):
    if class_:
        return f"<div class='{class_}'>\n{html}\n</div>\n"
    else:
        return f'<div>\n{html}\n</div>\n'

class GoFigure(Figure):
    """

            Args:
                figure_data (dict):
                post_script (str):
            Attributes:
                html (str):
    """
    def __init__(self, figure_data: Union[list[BaseTraceType], dict], caption:str, notes:Optional[list[str]] = None, post_script: str = ""):
        super(GoFigure, self).__init__(caption, notes)
        self.figure_data = figure_data
        self.post_script = post_script
        self.figure_obj = go.Figure(self.figure_data)

    def _as_html_figure_content(self):

        html = wrap_div(self.figure_obj.to_html(config={"displayModeBar": True},
                                                            # show_link=False,
                                                            include_plotlyjs=False,
                                                            # output_type='div',
                                                            full_html=False,
                                                            post_script=self.post_script),
                        class_='figure_div')

        return html
