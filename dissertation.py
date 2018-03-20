from __future__ import division
from __future__ import print_function
import datetime
from IPython.display import display, HTML, Markdown, Javascript, display_javascript, display_html
from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)
from IPython.display import FileLink, JSON, DisplayObject, Latex
import os.path
import os
import re
import sys
import StringIO
import contextlib
import inspect
import nbformat
from nbconvert import HTMLExporter, LatexExporter
from IPython.display import display, HTML
from traitlets.config import Config
from jinja2 import DictLoader
from IPython.core.magics.code import CodeMagics
import lyxithea as lyx
import nbformat
import re
import __builtins__ as bi
import __init__ as init
import document as lyxdoc

ip = get_ipython()

def cdis():
    if bi.__cdis__ is not None:
        return bi.__cdis__
    else:
        return dissertation()


class dissertation(lyxdoc.document):
    """ A dissertation class """
    def __init__(self, bib=None):
        super(dissertation, self).__init__(bib=bib)
        bi.__cdis__ = self
        self._current_chapter = ''
        self._chapters = []

    def title(self, title):
        self._title = title

    def author(self, author):
        self._author = author

    def author_backwards(self, author):
        self._author_backwards = author

    def degree(self, degree):
        self._degree = degree

    def dgr(self, dgr):
        self._dgr = dgr

    def major_prof(self, major_prof):
        self._major_prof = major_prof

    def campus(self, campus):
        self._campus = campus

    def dedication(self, dedication):
        self._dedication = self.process_markdown(dedication)
        return display(bi.__formatter__('\\begin{dedication}\n' +
                                        self._dedication +
                                        '\\end{dedication}\n'))

    def acknowledgements(self, ack):
        self._acknowledgements = self.process_markdown(ack)
        return display(bi.__formatter__('\\begin{acknowledgements}\n' +
                                        self._acknowledgements +
                                        '\\end{acknowledgements}\n'))

    def preface(self, preface):
        self._preface = self.process_markdown(preface)
        return display(bi.__formatter__('\\begin{preface}\n' + self._preface +
                                '\\end{preface}\n'))

    def toc(self):
        return display(bi.__formatter__(r'\pdfbookmark{TABLE OF CONTENTS}{TABLE OF CONTENTS}\tableofcontents{}'))

    def lot(self):
        return display(bi.__formatter__(r'\listoftables'))

    def lof(self):
        return display(bi.__formatter__(r'\listoffigures'))

    def appendix(self, filename):
        pass

    def appendices(self):
        return Latex('\n \\appendices')

    def peek(self):
        html_str = """<h1>{title}</h1>
        <h2>{author}</h2>
        <p>{month}, {year}</p>
        """.format(title=self._title, author=self._author, month=self._month,
                   year=self._year)
        return bi.__formatter__(html_str)

    def export(self, filename):
        super(dissertation, self).export(filename=filename, fmt='latex',
                                         template='dissertation')


@magics_class
class dissertation_magics(Magics):

    @line_cell_magic
    def dis(self, line, cell):
        """ call function of dissertation from a line magic """
        cdis = bi.__cdis__
        # sanitize the inputs
        arg = re.sub(u"(\u2018|\u2019)", "'", cell)
        arg = arg.replace("\'\'\'", "\"\"\"")
        cmd_str = "cdis.{method}(r\'\'\'{arg}\'\'\')" \
            .format(method=line, arg=arg)
        exec(cmd_str)

ip.register_magics(dissertation_magics)
