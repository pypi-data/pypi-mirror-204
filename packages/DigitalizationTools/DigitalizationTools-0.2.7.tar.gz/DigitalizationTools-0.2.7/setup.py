
from setuptools import setup, find_packages

VERSION = '0.2.7'
DESCRIPTION = 'A package that manages database through PostgreSQL and creates webapp through Dash plotly.'
LONG_DESCRIPTION = DESCRIPTION

# Setting up
setup(
    name="DigitalizationTools",
    version=VERSION,
    author="Mengke Lu",
    author_email="<mklu0611@gmail.com>",
    description= DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'postgresql', 'dash'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)