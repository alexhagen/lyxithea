import datetime
from IPython.display import display, HTML

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
        super(dissertation, self).__init__()

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
        self._dedication = dedication

    def acknowledgements(self, ack):
        self._acknowledgements = ack

    def preface(self, preface):
        self._preface = preface

    def toc(self):
        pass

    def lot(self):
        pass

    def lof(self):
        pass

    def nom(self):
        pass

    def abstract(self, abstract):
        self._abstract = abstract

    def chapter(self, filename):
        pass

    def appendix(self, filename):
        pass

    def bibliography(self):
        self._bib.bibliography()

    def peek(self):
        html_str = """<h1>{title}</h1>
        <h2>{author}</h2>
        <p>{month}, {year}</p>
        """.format(title=self._title, author=self._author, month=self._month,
                   year=self._year)
        display(HTML(html_str))
