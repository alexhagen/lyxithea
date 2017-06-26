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
        super(puslides, self).__init__(bib=bib)
        bi.__cslides__ = self

    def export(self, filename, engine='lualatex'):
        # copy the classfile over
        shutil.copy(osp.join(self.modulepath, 'puslides.cls'), './')
        # copy the css files over
        shutil.copytree(osp.join(self.modulepath, 'css/'), 'css/')
        # copy the fonts over
        shutil.copytree(osp.join(self.modulepath, 'fonts/'), 'fonts/')
        super(puslides, self).export(filename=filename, fmt='latex',
                                     engine=engine, template='puslides')
        shutil.rmtree('fonts/')
        shutil.rmtree('css/')

    def title(self, title):
        self._title = title

    def author(self, author):
        self._author = author

    def part(self, title):
        latex_str = r'\part{%s}' % title
        return display(Latex(latex_str))

    def chapter(title, content):
        latex_str = r'\def\nameofchapter{%s}' % content
        return display(Latex(latex_str))

    def onecolumntitle(self, content):
        self.slide_title = content

    @staticmethod
    def process_content(content, filename=None, **kwargs):
        if isinstance(content, str):
            self.content_one = self.process_markdown(content)
            latex_str = r'''\onecolumnslide{%%
                \begin{content}%%
                    %s
                \end{content}}%%
                {%s}%%''' \
                % (self.content_one, self.slide_title)
            self.slide_title = None
            self.content_one = None
            return Latex(latex_str)
        elif isinstance(content, pyg2d.pyg2d):
            content.export(filename, sizes=['cs'], customsize=(7.5, 5.25))
            return content.show(**kwargs)


    def onecolumn(self, content, **kwargs):
        display(Latex(r'''\onecolumnslide{%%
            \begin{content}%%'''))
        display(self.process_content(content, **kwargs))
        display(Latex(r'''\end{content}}%%
        {%s}%%''' % self.slide_title))
        self.slide_title = None
        self.content_one = None

    def twocolumntitle(self, content):
        self.slide_title = content

    def twocolumnleft(self, content, **kwargs):
        self.content_one = self.process_content(content, **kwargs)

    def twocolumnright(self, content, **kwargs):
        self.content_two = self.process_content(content, **kwargs)
        if self.content_one not None and self.content_two not None:
            display(Latex(r'''\onecolumnslide{%%
                \begin{content}%%'''))
            display(self.process_content(self.content_one, **kwargs))
            display(Latex(r'''\end{content}}%%'''))
            display(Latex(r'''{%%
                \begin{content}%%'''))
            display(self.process_content(self.content_two, **kwargs))
            display(Latex(r'''\end{content}}%%
            {%s}%%''' % self.slide_title))



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
