class document(object):
    """ A document class """
    def __init__(self):
        pass


class dissertation(document):
    """ A dissertation class """
    def __init__(self, bib):
        self._bib = bib
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
