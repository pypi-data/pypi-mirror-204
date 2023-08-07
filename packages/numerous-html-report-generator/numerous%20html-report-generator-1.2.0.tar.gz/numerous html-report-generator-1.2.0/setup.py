import setuptools
import os
from distutils.util import convert_path
from pathlib import Path

ver_path = convert_path('version.txt')
ver = None
if os.path.exists(ver_path):
    with open(ver_path) as ver_file:
        ver = ver_file.read()

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="numerous html-report-generator",
    version=ver,
    author="numerous - Tobias Skov Reipuert, Tobias Dokkedal Elmøe, Lasse Nyberg Thomsen, Ósk Björnsdottir",
    author_email="report-generator@numerous.com",
    description="Report generator for html reports",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_namespace_packages(where='src'),
    package_dir={'': 'src'},
    package_data={"": ["*.html"]},
    include_package_data=True,
    install_requires=requirements,
    python_requires='>=3.9',
    license="O-BSD-3",
)

