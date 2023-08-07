# numerous Report Generator

A python package focused on enabling you to create beautiful and powerful html reports with great ease. You can use the reports to document your work and showcase your data, even generating these automitically with your analysis code already implemented in python.

This package exposes a simple library to create a report, adding your sections, figures and tables or even just directly html divs with your own custom html code.

When you have added your content to the report you can save it to a stand-alone html file you can share with anyone.

We have provided you with a first template that you can modify to your needs. Soon we will publish a guide on how to change basic things in it - for instance the logo file.

## Installation

The package numerous report generator can be installed with:
```console
pip install numerous-html-report-generator
```

## Quick start

Here is a simple example to get you started once you have installed the package:

```python
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
```

## Contributing:

Please see CONTRIBUTING.md for details on how to contribute.