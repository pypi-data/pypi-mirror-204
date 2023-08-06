# coding: utf-8
"""
@Version    :
@Function   :
@Author     : Frank
@Contact    : fanglwh@outlook.com
@Date       : 2023/1/31   9:18
@Tool       : PyCharm
@File       : setup.py.py
"""

from setuptools import setup
from __version__ import *


if __name__ == "__main__":

    setup(name=NAME,
          version=VERSION,
          author=AUTHOR,
          long_description_content_type="text/markdown",
          long_description=open("README.md", "r").read(),
          )
