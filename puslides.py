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
import pypandoc

ip = get_ipython()

def cslides():
    if bi.__cslides__ is not None:
        return bi.__cslides__
    else:
        return puslides()


class puslides(lyxdoc.document):
    """ A purdue slides class """
    def __init__(self, bib=None):
        self.modulepath = osp.dirname(__file__)
        self.content_one = None
        self.content_two = None
        self.content = [None, None, None, None, None, None, None]
        super(puslides, self).__init__(bib=bib)
        bi.__cslides__ = self

    def export(self, filename, engine='lualatex'):
        # copy the classfile over
        shutil.copy(osp.join(self.modulepath, 'puslides.cls'), './')
        # copy the css files over
        shutil.copytree(osp.join(self.modulepath, 'css/'), 'css/')
        # copy the fonts over
        shutil.copytree(osp.join(self.modulepath, 'fonts/'), 'fonts/')
        metadata = {"author": self._author, "title": self._title,
                    "affiliation": self._affiliation,
                    "subtitle": self._subtitle,
                    "venue": self._venue,
                    "city": self._city}
        super(puslides, self).export(filename=filename, fmt='latex',
                                     engine=engine, template='puslides',
                                     metadata=metadata)
        shutil.rmtree('fonts/')
        shutil.rmtree('css/')

    def title(self, title):
        self._title = title

    def author(self, author):
        self._author = author

    def affiliation(self, affiliation):
        self._affiliation = affiliation

    def subtitle(self, subtitle):
        self._subtitle = subtitle

    def venue(self, venue):
        self._venue = venue

    def city(self, city):
        self._city = city

    def part(self, title):
        latex_str = r'\part{%s}' % title
        return display(Latex(latex_str))

    def chapter(title, content):
        latex_str = r'\def\nameofchapter{%s}' % content
        return display(Latex(latex_str))

    def clear_slide(self):
        self.slide_title = None
        self.content = [None for x in self.content]

    def bibliography(self):
        return super(puslides, self).bibliography(header_level=3, force_string=True)

    def process_content(self, content, index, filename=None, **kwargs):
        if isinstance(content, str):
            self.content[index] = \
                pypandoc.convert_text(self.process_markdown(content), 'latex',
                                      format='md')
            latex_str = self.content[index]
            return latex_str
        elif isinstance(content, pyg2d.pyg2d):
            content.export(filename, sizes=['cs'], customsize=(7.5, 5.25))
            return content.show(**kwargs)

    def onecolumntitle(self, content):
        self.slide_title = content

    def onecolumn(self, content, **kwargs):
        self.process_content(content, 0, **kwargs)
        display(Latex(r'\onecolumnslide{\begin{content}%s \end{content}}{%s}' % (self.content[0], self.slide_title)))
        self.clear_slide()

    def twocolumntitle(self, content):
        self.slide_title = content

    def twocolumnleft(self, content, **kwargs):
        self.process_content(content, 0, **kwargs)

    def twocolumnright(self, content, **kwargs):
        self.process_content(content, 1, **kwargs)
        if self.content[0] is not None and self.content[1] is not None:
            latex_str = (r'\twocolumnslide{\begin{content}%s \end{content}}' + \
                r'{\begin{content}%s \end{content}}' + \
                r'{%s}') % \
                (self.content[0], self.content[1], self.slide_title)
            display(Latex(latex_str))
            self.clear_slide()

    def twocolumnshiftlefttitle(self, content):
        self.slide_title = content

    def twocolumnshiftleftleft(self, content, **kwargs):
        self.process_content(content, 0, **kwargs)

    def twocolumnshiftleftright(self, content, **kwargs):
        self.process_content(content, 1, **kwargs)
        if self.content[0] is not None and self.content[1] is not None:
            latex_str = (r'\twocolumnshiftleft{\begin{content}%s \end{content}}' + \
                r'{\begin{content}%s \end{content}}' + \
                r'{%s}') % \
                (self.content[0], self.content[1], self.slide_title)
            display(Latex(latex_str))
            self.clear_slide()

    def twocolumnshiftrighttitle(self, content):
        self.slide_title = content

    def twocolumnshiftrightleft(self, content, **kwargs):
        self.process_content(content, 0, **kwargs)

    def twocolumnshiftrightright(self, content, **kwargs):
        self.process_content(content, 1, **kwargs)
        if self.content[0] is not None and self.content[1] is not None:
            latex_str = (r'\twocolumnshiftright{\begin{content}%s \end{content}}' + \
                r'{\begin{content}%s \end{content}}' + \
                r'{%s}') % \
                (self.content[0], self.content[1], self.slide_title)
            display(Latex(latex_str))
            self.clear_slide()

    def tworowtitle(self, content):
        self.slide_title = content

    def tworowtop(self, content, **kwargs):
        self.process_content(content, 0, **kwargs)

    def tworowbottom(self, content, **kwargs):
        self.process_content(content, 1, **kwargs)
        if self.content[0] is not None and self.content[1] is not None:
            latex_str = (r'\tworow{\begin{content}%s \end{content}}' + \
                r'{\begin{content}%s \end{content}}' + \
                r'{%s}') % \
                (self.content[0], self.content[1], self.slide_title)
            display(Latex(latex_str))
            self.clear_slide()

    def tworowpushdowntitle(self, content):
        self.slide_title = content

    def tworowpushdowntop(self, content, **kwargs):
        self.process_content(content, 0, **kwargs)

    def tworowpushdownbottom(self, content, **kwargs):
        self.process_content(content, 1, **kwargs)
        if self.content[0] is not None and self.content[1] is not None:
            latex_str = (r'\tworowpushdown{\begin{content}%s \end{content}}' + \
                r'{\begin{content}%s \end{content}}' + \
                r'{%s}') % \
                (self.content[0], self.content[1], self.slide_title)
            display(Latex(latex_str))
            self.clear_slide()

    def tworowpushuptitle(self, content):
        self.slide_title = content

    def tworowpushuptop(self, content, **kwargs):
        self.process_content(content, 0, **kwargs)

    def tworowpushupbottom(self, content, **kwargs):
        self.process_content(content, 1, **kwargs)
        if self.content[0] is not None and self.content[1] is not None:
            latex_str = (r'\tworowpushup{\begin{content}%s \end{content}}' + \
                r'{\begin{content}%s \end{content}}' + \
                r'{%s}') % \
                (self.content[0], self.content[1], self.slide_title)
            display(Latex(latex_str))
            self.clear_slide()

    def tworowtoptwocolumntitle(self, content):
        self.slide_title = content

    def tworowtoptwocolumntop(self, content, **kwargs):
        self.process_content(content, 0, **kwargs)

    def tworowpushipbottom(self, content, **kwargs):
        self.process_content(content, 1, **kwargs)
        if self.content[0] is not None and self.content[1] is not None:
            latex_str = (r'\tworowpushup{\begin{content}%s \end{content}}' + \
                r'{\begin{content}%s \end{content}}' + \
                r'{%s}') % \
                (self.content[0], self.content[1], self.slide_title)
            display(Latex(latex_str))
            self.clear_slide()


@magics_class
class puslides_magics(Magics):

    @line_cell_magic
    def slides(self, line, cell):
        """ call function of puslides from a line magic """
        cslides = bi.__cslides__
        # sanitize the inputs
        arg = re.sub(u"(\u2018|\u2019)", "'", cell)
        arg = arg.replace("\'\'\'", "\"\"\"")
        cmd_str = "cslides.{method}(r\'\'\'{arg}\'\'\')" \
            .format(method=line, arg=arg)
        exec(cmd_str)

ip.register_magics(puslides_magics)
