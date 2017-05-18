import datetime
from IPython.display import display, HTML, Markdown, Javascript, display_javascript
from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)
import __builtin__ as bi

js = "IPython.CodeCell.config_defaults.highlight_modes['magic_markdown'] = {'reg':[/^%%dis/]};"
display_javascript(js, raw=True)

class document(object):
    """ A document class """
    def __init__(self):
        pass


class dissertation(document):
    """ A dissertation class """
    def __init__(self, bib):
        self._bib = bib
        now = datetime.datetime.now()
        self._month = now.strftime("%B")
        self._year = now.strftime("%Y")
        self._chapter_paths = []
        self._data_paths = []
        bi.__cdis__ = self
        super(dissertation, self).__init__()

    @staticmethod
    def check_chapter_path(path):
        """ checks if the chapter path is a legitimate path

        :param path: the path to the folder to be added
        :returns: boolean if the path is good or not
        """
        return true

    @staticmethod
    def process_markdown(markdown):
        """ looks for python parameter notation in a markdown string """
        return markdown

    def chapter_paths(self, paths):
        """ add paths to the chapter path variable

        :param paths: a list of string paths in the filesystem where chapters
            are found
        """
        for path in paths:
            if self.check_chapter_path(path):
                self._chapter_paths.extend([path])
        return self

    def title(self, title):
        self._title = title
        return self

    def author(self, author):
        self._author = author
        return self

    def author_backwards(self, author):
        self._author_backwards = author
        return self

    def degree(self, degree):
        self._degree = degree
        return self

    def dgr(self, dgr):
        self._dgr = dgr
        return self

    def major_prof(self, major_prof):
        self._major_prof = major_prof
        return self

    def campus(self, campus):
        self._campus = campus
        return self

    def dedication(self, dedication):
        self._dedication = self.process_markdown(dedication)
        display(Markdown(self._dedication))
        return self

    def acknowledgements(self, ack):
        self._acknowledgements = self.process_markdown(ack)
        display(Markdown(self._acknowledgements))
        return self

    def preface(self, preface):
        self._preface = self.process_markdown(preface)
        display(Markdown(self._preface))
        return self

    def toc(self):
        pass
        return self

    def lot(self):
        pass
        return self

    def lof(self):
        pass
        return self

    def nom(self):
        pass
        return self

    def abstract(self, abstract):
        self._abstract = self.process_markdown(abstract)
        display(Markdown(self._abstract))
        return self

    def chapter(self, filename):
        pass
        return self

    def appendix(self, filename):
        pass
        return self

    def bibliography(self):
        self._bib.bibliography()
        return self

    def peek(self):
        html_str = """<h1>{title}</h1>
        <h2>{author}</h2>
        <p>{month}, {year}</p>
        """.format(title=self._title, author=self._author, month=self._month,
                   year=self._year)
        display(HTML(html_str))
        return self

ip = get_ipython()

@magics_class
class dissertation_magics(Magics):

    @line_cell_magic
    def dis(self, line, cell):
        """ call function of dissertation from a line magic """
        cdis = bi.__cdis__
        cmd_str = "cdis.{method}(r\"\"\"{arg}\"\"\")" \
            .format(method=line, arg=cell)
        exec(cmd_str)

ip.register_magics(dissertation_magics)
