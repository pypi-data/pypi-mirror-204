from setuptools import setup, find_packages

VERSION = '1.5.1'
DESCRIPTION = "Package for coloring strings in the terminal"
LONG_DESCRIPTION = "Package for coloring strings in the terminal"

# Setting up
setup(
    name="pipcolouringslibV1",
    version=VERSION,
    author="NHJonas",
    author_email="nick.faltermeier@gmx.de",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Operating System :: Microsoft :: Windows",
    ]
)