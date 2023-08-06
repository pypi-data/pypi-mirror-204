from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Django Viewers Count Middleware get from user request'

# Setting up
setup(
    name="django-viewers-counts-middleware",
    version=VERSION,
    author="Hariharan",
    author_email="hari@ittamil.in",
    description=DESCRIPTION,
    url = "https://github.com/ittamil/django-viewers-counts-middleware",
    packages=find_packages(),
    keywords=['python', 'django', 'viewers count middleware', 'viewers count', 'middleware', 'django plugin'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
