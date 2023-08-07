from ..table import Table
from typing import List, Optional, AnyStr


class DataFrameTable(Table):
    """
    Create a dataframe (pandas) table, which may be formatted using html classes

    Args:
        table_df: the pandas dataframe table
        caption: a caption applied to the top of the html table
        notes: notes to added
        show_index: True if the index column should be shown, false if not (default)
        classes: the html classes to format the table with

    """

    def __init__(self, table_df, caption: str, notes: Optional[List[str]] = None, show_index: bool = False,
                 classes: Optional[List | AnyStr] = None):

        if not notes:
            notes = []
        super(DataFrameTable, self).__init__(caption, notes)

        self.table_df = table_df
        self.show_index = show_index
        self.classes = classes

    def as_html_figure_content(self):
        return self.table_df.to_html(classes=self.classes, index=self.show_index, render_links=True, escape=False)

    def _as_html(self):
        return self.as_html_figure_content()