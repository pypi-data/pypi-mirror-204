"""
An extensible python package that enables you to easily create great looking modular html reports

When you have created your data science script and have all the nice results you want to package this up in a nice way.
To allow you share with your peers.
This package helps you create interactive and nice looking reports, yet available in a single static html file.
"""
from .report import Report
from numerous.html_report_generator.components.plotly.gofigure import GoFigure
from .components.div import Div
from .components.tabs import Tabs
from .components.section import Section
from .components.cards import Card
from numerous.html_report_generator.components.pandas.dataframetable import DataFrameTable