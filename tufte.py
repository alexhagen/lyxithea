import lyxithea as lyx
from IPython.display import display, Latex
from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)
import nbformat
import re
import __builtins__ as bi
import __init__ as init
import document as lyxdoc
import os.path as osp
import shutil
from pyg import twod as pyg2d

ip = get_ipython()

def cdoc():
    if bi.__cdoc__ is not None:
        return bi.__cdoc__
    else:
        return pudoc()


class tufte(lyxdoc.document):
    """ A tufte document class """
    def __init__(self, bib=None):
        pass
