r"""
======================
Quick Start Example
======================

Simple example that creates a report with a figure and a table and adds them to a section.
"""

from pathlib import Path
import os
from numerous.html_report_generator import Report, Section, GoFigure, DataFrameTable
import pandas as pd

# Define output folder and html file
folder = Path('./output')
filename = 'my_first_report'
file = folder.joinpath(filename+'.html')

#Remove previous report file if exists
if os.path.exists(file):
    os.remove(file)

# Create report
report = Report(target_folder=folder, filename=filename)

# Add info for the header and title page
report.add_header_info(header='My Organization',
                       title='My First Report',
                       sub_title='but not the last',
                       sub_sub_title='at all',
                       footer_title='My first footer',
                       footer_content='This is the end!'
                       )

#Add a section
section = Section(section_title="Section 1")

#create a figure
figure = GoFigure({
        "data": [{"type": "bar",
                  "x": [1, 2, 3],
                  "y": [1, 3, 2]}],
        "layout": {"title": {"text": "A Figure Specified By Python Dictionary"}}
    }, caption="Test figure", notes=["Please notice x", "Please notice y"])

#create a table
table = DataFrameTable(pd.DataFrame({
    'a': [1, 2, 3],
    'b': [4, 5, 6]
}), caption="This is a test table")

#Add the figure and table to the section
section.add_content({
    'figure': figure,
    'table': table
})

#Add the section to the report
report.add_blocks({
    'section': section
})

# Save the report - creates the html output file
report.save()