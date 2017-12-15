import lyxithea as lyx
from IPython.display import display, Latex, HTML
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
import pypandoc
import numpy as np
from mwe import mwe

ip = get_ipython()


def cdoc():
    if bi.__cdoc__ is not None:
        return bi.__cdoc__
    else:
        return article()


class article(lyxdoc.document):
    """ A two column article class """
    def __init__(self, bib=None):
        self.modulepath = osp.dirname(__file__)
        super(article2, self).__init__(bib=bib)
        bi.__cdoc__ = self

    def export(self, filename, engine='pdflatex'):
        metadata = {"author": self._author, "title": self._title,
                    "affiliation": self._affiliation}
        super(article2, self).export(filename=filename, fmt='latex',
                                     engine=engine, template='article2',
                                     metadata=metadata)


@magics_class
class article2_magics(Magics):

    @line_cell_magic
    def art2(self, line, cell):
        """ call function of article2 from a line magic """
        cdoc = bi.__cdoc__
        # sanitize the inputs
        arg = re.sub(u"(\u2018|\u2019)", "'", cell)
        arg = arg.replace("\'\'\'", "\"\"\"")
        cmd_str = "cdoc.{method}(r\'\'\'{arg}\'\'\')" \
            .format(method=line, arg=arg)
        exec(cmd_str)

ip.register_magics(article2_magics)
