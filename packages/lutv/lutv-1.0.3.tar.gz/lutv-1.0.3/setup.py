from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0.3'
DESCRIPTION = 'This is my personal project'

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# Setting up
setup(
    name="lutv",
    version=VERSION,
    author="Trần Xuân Lợi",
    author_email="tranxuanloi2007@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['LuTV', 'lutv', 'random', 'random_uer', 'lutvrandom','LuTV Random User', "Tranxuanloi","TranXuanLoi","tranxuanloi","tranxuanloi2007"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Android",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)