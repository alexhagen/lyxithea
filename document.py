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
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import contextlib
import inspect
import nbformat
from nbconvert import HTMLExporter, LatexExporter
from IPython.display import display, HTML
from traitlets.config import Config
from jinja2 import DictLoader
from IPython.core.magics.code import CodeMagics
from . import lyxithea as lyx
import nbformat
import re
from pyg import twod as pyg2d
from . import utils as bi
import __init__ as init
import logging

if lyx.run_from_ipython():
    ip = get_ipython()
else:
    ip = None

def cdoc():
    """``cdoc`` returns the document currently being edited.

    ``cdoc`` will return the document that is currently being edited, or, if
    a document is not currently being edited, returns a new document. Use this
    at the beginning of new chapters so you can edit them in place but still
    have them inherit the whole document.

    :returns lyxithea.document: the document being edited
    """
    if bi.__cdoc__ is not None:
        return bi.__cdoc__
    else:
        return document()

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        try:
            stdout = StringIO.StringIO()
        except AttributeError:
            stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

js = "require(\"notebook/js/cell\").Cell.options_default.cm_config.lineWrapping = true;\n"
#js += "require(\"notebook/js/cell\").CodeCell.options_default.cm_config.lineWrapping = true;\n"
#js += "require(\"notebook/js/cell\").MarkdownCell.options_default.cm_config.lineWrapping = true;\n"
#js = "console.log(Object.getOwnPropertyNames(require(\"notebook/js/cell\").CodeCell));\n"
js += "require(['notebook/js/codecell'], function(codecell) {\n"
js += "    codecell.CodeCell.options_default.highlight_modes['magic_markdown'] = {'reg':[/^%%dis|^%%doc/]}; \n"
js += "    Jupyter.notebook.events.one('kernel_ready.Kernel', function(){\n"
js += "      Jupyter.notebook.get_cells().map(function(cell){\n"
js += "          if (cell.cell_type == 'code'){ cell.auto_highlight(); } }) ;\n"
js += "      });\n"
js += "   });\n"
display_javascript(js, raw=True)

html_str = '<span>$\\newcommand{\\unit}[1]{\\mathrm{\; #1}}$</span>\n'
html_str += '<span>$\\newcommand{\\ce}[1]{\\mathrm{#1}}$</span>\n'
html_str += '<link rel="stylesheet" href="https://cdn.rawgit.com/tiaanduplessis/wenk/master/dist/wenk.css">\n'
html_str += '<style> span.abbr{ color: #999; } </style>\n<style> [data-wenk]:after { z-index: 1000000000; } </style>\n'
display_html(html_str, raw=True)

class document(object):
    """ ``lyxithea.document`` is analogous to LaTeX's article.cls - a
        generalized journal article-like template.

        :param lyx.bib bib: A ``lyx.bib`` object for the bibliography """
    def __init__(self, bib=None, level=logging.WARNING):
        logging.basicConfig(level=level)
        if bib is None:
            self._bib = lyx.bib('bibs/dissertation.bib')
        else:
            self._bib = bib
        now = datetime.datetime.now()
        self._month = now.strftime("%B")
        self._year = now.strftime("%Y")
        self._chapter_paths = []
        self._data_paths = []
        bi.__cdoc__ = self
        self.cwd = os.path.abspath(os.getcwd())
        self.chapter_paths([self.cwd])

    def title(self, title):
        """ Adds a title to the document that will be printed in the
                ``\maketitle`` environment in LaTeX.

            :param str title: the title of the document
        """
        self._title = title

    def author(self, author):
        """ Adds an author to the document that will be printed in the
                ``\maketitle`` environment in LaTeX.

            :param str author: the author's name

            :todo: implement author lists and author with affiliation
        """
        self._author = author

    def affiliation(self, affiliation):
        """ Adds the affiliation to the author written with the
                ``document.author`` method
            :param str affiliation: the institution the author in the
                ``document.author`` section works at
        """
        self._affiliation = affiliation

    @staticmethod
    def check_chapter_path(path):
        """Check if the chapter path is a legitimate path.

        :param path: the path to the folder to be added
        :returns: boolean if the path is good or not
        """
        path = path.replace('~', os.path.expanduser('~'))
        return os.path.isdir(path)

    def set_hide_dblclick(self, string):
        """A private method to hide the text on double click."""
        javascript_str = """
        function code_toggle()
        {
            var code_shown = $(this).attr('value') == 'true';
            if (code_shown)
            {
                console.log("code shown")
                $(this).children('.input').show('500');
            }
            else
            {
                console.log("code not shown")
                $(this).children('.input').hide('500');
            }

            code_shown = !code_shown;
            $(this).attr('value', code_shown);
        }
        $('.code_cell').each(function() {
            if(!$(this)[0].hasAttribute("value")){
                $(this).attr('value', 'true');
            }
        });
        $('.code_cell').each(function() {
            $(this).unbind("dblclick").dblclick(code_toggle);
        });"""
        return display(Javascript(javascript_str))

    @staticmethod
    def get_locals():
        """Pass local variables to external chapters in other notebooks."""
        lcls = ip.user_module.__dict__
        return lcls

    def process_content(self, content, filename=None, latex=False,
                        **kwargs):
        """Process the arguments into something LaTeX/word can handle.

        ``process_content`` checks the type of the content passed to it and
        will then process it into something that our exporter can handle.
        If ``content`` is a string, it will pull out any python variables and
        replace them with their output, and also process all markdown into
        LaTeX.
        If ``content`` is some graphics class, it will fill in the necessary
        graphics commands.

        :param content: the content that will be processed. Can be ``str``,
            ``pyg2d``, or an ``pygsvg`` object.
        :param str filename: filename for ``svg`` file, if applicable
        :param bool latex: if we need to output the content in LaTeX format,
            default ``False``
        :returns: the content after processing
        """
        if latex:
            return content
        if isinstance(content, str):
            content = self.process_markdown(content)
            latex_str = content
            return latex_str
        elif isinstance(content, pyg2d.pyg2d):
            lyx.latex()
            content.export(filename, force=True, sizes=['1'])
            string = content.show(need_string=True, **kwargs)
            return string
        elif isinstance(content, pyg2d.svg):
            lyx.latex()
            string = content.show(need_string=True, **kwargs)
            return Latex(string)

    def process_markdown(self, markdown):
        """ Looks for python parameter notation in a markdown string

            :todo: Make this into a Jinja2 class for more flexibility.
            :todo: make a context manager for the markdown so I can use ``with``
                syntax

            :param str markdown: Markdown formatted text with possible Python
                inclusions
            :returns str: Markdown formatted replaced text
        """
        matches = re.finditer(bi.__regex__, markdown)
        matches2 = re.finditer(bi.__regex2__, markdown)

        for matchNum, match in enumerate(matches):
            with stdoutIO() as s:
                #lyx.markdown()
                lyx.latex()
                exec(match.group(1), self.get_locals())
                #lyx.latex(False)
                #lyx.markdown(False)
            rep_string = s.getvalue()[:-1]
            if len(rep_string) < 1:
                cmd = "from __future__ import print_function; print ({oldcmd})".format(oldcmd=match.group(1))
                with stdoutIO() as s:
                    #lyx.markdown()
                    lyx.latex()
                    exec(cmd, self.get_locals())
                    #lyx.latex(False)
                    #lyx.markdown(False)
                rep_string = s.getvalue()[:-1]
            markdown = markdown.replace(match.group(), rep_string)
        for matchNum, match in enumerate(matches2):
            with stdoutIO() as s:
                #lyx.markdown()
                lyx.latex()
                exec(match.group(1), self.get_locals())
                #lyx.latex(False)
                #lyx.markdown(False)
            rep_string = s.getvalue()[:-1]
            if len(rep_string) < 1:
                cmd = "from __future__ import print_function; print ({oldcmd})".format(oldcmd=match.group(1))
                with stdoutIO() as s:
                    #lyx.markdown()
                    lyx.latex()
                    exec(cmd, self.get_locals())
                    #lyx.latex(False)
                    #lyx.markdown(False)
                rep_string = s.getvalue()[:-1]
            markdown = markdown.replace(match.group(), rep_string)
        return markdown

    def chapter_paths(self, paths):
        """ Add paths to the chapter path variable

            :param paths: a list of string paths in the filesystem where chapters
                are found
        """
        for path in paths:
            if self.check_chapter_path(path):
                path = path.replace('~', os.path.expanduser('~'))
                self._chapter_paths.extend([path])

    def nom(self):
        """ Prints the nomenclature

            :todo: Implement this into html as well
        """
        latex_str = r'\printnomenclature'
        return display(bi.__formatter__(latex_str))

    def chapter(self, filename):
        pass

    def replace_rel_paths(self, string, filename):
        """ Replaces relative paths with an absolute path

            :todo: make the relative path replacement more robust
        """
        print (filename)
        print (os.path.split(filename))
        # find all paths in the string with a regex
        matches = re.compile(r"(([/]|\.\.|\./)([^.]*[\.][\w][\w][\w][\w]?|$))", flags=0) \
            .findall(string)
        print (matches)
        # for each path
        for match in matches:
            print (match[0])
            rep_str = os.path.relpath(os.path.join(os.path.split(filename)[0], match[0]))
            print (rep_str)
            string.replace(match[0], rep_str)
        return string

    def append_notebook(self, filename, cells, child=True):
        """ Append a notebook (the whole notebook) to a point in a lyxithea
            ``document``.  This works only if the notebook is also a
            ``document``.

            :param str filename: filename of ipynb to append
            :param list cells: the cells that we'll append to
            :param bool child: if the notebook we're appending is the child
        """
        logging.debug(filename)
        #logging.debug(self.find_first(filename))
        _nb = nbformat.read(self.find_first(filename), 4)
        fpath = os.path.abspath(os.path.dirname(self.find_first(filename)))
        cells.extend([nbformat.v4.new_code_cell("import os; os.chdir(\'%s\')" % fpath)])
        for cell in _nb.cells:
            if cell['cell_type'] == 'code':
                logging.debug(cell['source'])
                if re.match('dis\.chapter\([\'\"](.*)[\'\"]\)', cell['source']) is None \
                    and re.match('dis\.appendix\([\'\"](.*)[\'\"]\)', cell['source']) is None \
                    and cell['source'] is not '' \
                    and re.match('dis\.export\([\'\"](.*)[\'\"]\)', cell['source']) is None \
                    and re.match('slides\.export\([\'\"](.*)[\'\"]\)', cell['source']) is None \
                    and re.match('doc\.export\([\'\"](.*)[\'\"]\)', cell['source']) is None:
                        if child:
                            source = cell['source'].replace('lyx.print_todos()', '')\
                                .replace(".export(\'../img", ".export(\'%s/img" % self.cwd)\
                                .replace(".export(\"../img", ".export(\"%s/img" % self.cwd)\
                                .replace(".svg_show(\'../img", ".svg_show(\'%s/img" % self.cwd)\
                                .replace(".svg_show(\"../img", ".svg_show(\"%s/img" % self.cwd)
                            #source = self.replace_rel_paths(source, self.find_first(filename))
                        else:
                            source = cell['source']\
                                .replace(".export(\'../img", ".export(\'%s/img" % self.cwd)\
                                .replace(".export(\"../img", ".export(\"%s/img" % self.cwd)\
                                .replace(".svg_show(\'../img", ".svg_show(\'%s/img" % self.cwd)\
                                .replace(".svg_show(\"../img", ".svg_show(\"%s/img" % self.cwd)
                            #source = self.replace_rel_paths(source, self.find_first(filename))
                        cell_to_add = nbformat.v4.new_code_cell(source)
                        cells.extend([cell_to_add])
                elif re.match('dis\.chapter\([\'\"](.*)[\'\"]\)', cell['source']) is not None:
                    # find the argument of 'dischapter('
                    matches = re.match('dis\.chapter\([\'\"](.*)[\'\"]\)', cell['source'])
                    import_filename = matches.group(1)
                    if '.tex' not in import_filename:
                        self.append_notebook(import_filename, cells)
                    else:
                        src = r'Latex(\'\input{%s}\')' % import_filename
                        cell_to_add = nbformat.v4.new_code_cell(src)
                        cells.extend([cell_to_add])

                elif re.match('dis\.appendix\([\'\"](.*)[\'\"]\)', cell['source']) is not None:
                    # find the argument of 'disappendix('
                    matches = re.match('dis\.appendix\([\'\"](.*)[\'\"]\)', cell['source'])
                    import_filename = matches.group(1)
                    if '.tex' not in import_filename:
                        self.append_notebook(import_filename, cells)
                    else:
                        src = r'Latex(\'\input{%s}\')' % import_filename
                        cell_to_add = nbformat.v4.new_code_cell(src)
                        cells.extend([cell_to_add])
        #cells.extend([nbformat.v4.new_code_cell("os.chdir(\'%s\')" % self.cwd)])
        return cells

    def abstract(self, abstract):
        self._abstract = self.process_markdown(abstract)
        return display(bi.__formatter__('\\begin{abstract}\n' + self._abstract +
                                        '\\end{abstract}'))

    def find_first(self, filename):
        r""" find_first is an internal command for finding the first instance of
            a document on the path
        """
        for path in self._chapter_paths:
            logging.debug(self._chapter_paths)
            if path != '/':
                for root, dirs, files in os.walk(path):
                    logging.debug('%s, %s, %s' % (root, dirs, files))
                    for extension in ["ipynb", "lyx"]:
                        _fname = "{fname}.{ext}".format(fname=filename,
                                                        ext=extension)
                        if _fname in files:
                            logging.debug(os.path.join(root, _fname))
                            return os.path.join(root, _fname)

    def bibliography(self, header_level=3, force_string=True, **kwargs):
        r""" writes the bibliography to the document

            :param int header_level: defines the latex heading level of
                the bibliography section
            :param bool force_string: forces a latex string (not
                IPython.html or IPython.latex) output
        """
        return self._bib.bibliography(header_level=header_level,
                                      force_string=force_string, **kwargs)

    def add_to_cchap(self, string):
        processed_string = self.process_markdown(string)
        #self._current_chapter += processed_string
        return display(bi.__formatter__(processed_string))

    def add(self, string, **kwargs):
        processed_string = self.process_content(string, **kwargs)
        #self._current_chapter += processed_string
        return bi.__formatter__(processed_string)

    def appendix_on(self):
        r""" ``appendix_on`` starts a section of text sent to reserved text for
                appendices. Must be ended with ``appendix_off``.
        """
        display(Latex(r'\saveappendix{'))

    def appendix_off(self):
        r""" ``appendix_off`` ends a section of text reserved for the appendices.
                Must be preceded by ``appendix_on``.
        """
        display(Latex(r'}'))

    def appendices(self):
        r""" ``appendices`` prints all the text saved for appendices.
        """
        display(Latex('\\appendix\n'))
        display(Latex('\\appendicestext\n'))

    def export(self, filename, fmt='latex', engine='pdflatex',
               template="article", metadata={}, **kwargs):
        r""" exports the current document - into latex for now """
        lyx.exporting(True)
        # open the notebook as version four, get its path and all its cells
        self.nb = nbformat.v4.new_notebook()
        self.cwd = os.path.abspath(os.getcwd())
        logging.debug(filename)
        cells = self.append_notebook(filename, [], child=False)
        logging.debug('after cells')
        self.nb['cells'] = cells
        # write it to a temp file
        nbformat.write(self.nb, 'temp_notebook.ipynb', 4)
        # now do the nb_convert to latex by executing
        self.nb = nbformat.read('temp_notebook.ipynb', 4)
        self.nb.metadata += metadata
        self.c = Config()
        self.c.ExecutePreprocessor.interrupt_on_timeout = True
        self.c.ExecutePreprocessor.timeout = 600
        self.template = bi.__templates__[template]
        if fmt == 'latex':
            self.export_latex(filename, engine=engine, **kwargs)
        elif fmt == 'html':
            self.export_html(filename)
        lyx.exporting(False)

    def export_latex(self, filename, engine='pdflatex', interaction='-interaction batchmode'):
        r""" exports to latex """
        lyx.latex()
        lyx.markdown(False)
        bi.__formatter__ = Latex
        bi.__need_latex__ = True
        self.c.LatexExporter.preprocessors = \
            ['nbconvert.preprocessors.ExecutePreprocessor']
        with open('nilf.tplx', 'w') as f:
            f.write(self.template)
        latex_exporter = LatexExporter(config=self.c, template_file='nilf.tplx')
        (body, resources) = latex_exporter.from_notebook_node(self.nb)
        with open('./' + filename + '.tex', 'w') as f:
            f.write(body)
        #interaction = '-interaction batchmode'
        #interaction = ''
        os.system('{engine} {int} ./'.format(engine=engine, int=interaction) + filename + '.tex')
        os.system('bibtex ./' + filename)
        os.system('bibtex ./' + filename + '.aux')
        os.system('{engine} {int} ./'.format(engine=engine, int=interaction) + filename + '.tex')
        os.system('{engine} {int} ./'.format(engine=engine, int=interaction) + filename + '.tex')
        os.system('{engine} {int} ./'.format(engine=engine, int=interaction) + filename + '.tex')
        os.system('makeindex ./{fname}.nlo -s nomencl.ist -o {fname}.nls'.format(fname=filename))
        os.system('{engine} {int} ./'.format(engine=engine, int=interaction) + filename + '.tex')
        display(FileLink('./' + filename + '.pdf'))
        display(FileLink('./' + filename + '.tex'))
        #lyx.latex(False)
        os.remove('temp_notebook.ipynb')
        #os.remove(filename + '.out')
        #os.remove(filename + '.log')
        #os.remove(filename + '.bbl')
        #os.remove(filename + '.aux')
        #os.remove(filename + '.blg')

    def export_html(self, filename, **kwargs):
        r""" exports to html """
        self.c.HTMLExporter.preprocessors = \
            ['nbconvert.preprocessors.ExecutePreprocessor']
        #html_exporter = HTMLExporter(config=c, template_file='noinputhtmlfull.tpl')
        #(body, resources) = html_exporter.from_notebook_node(nb)

if ip is not None:
    @magics_class
    class document_magics(Magics):

        @line_cell_magic
        def doc(self, line, cell):
            """ call function of dissertation from a line magic """
            cdoc = bi.__cdoc__
            # sanitize the inputs
            arg = re.sub(u"(\u2018|\u2019)", "'", cell)
            arg = arg.replace("\'\'\'", "\"\"\"")
            cmd_str = "cdoc.{method}(r\'\'\'{arg}\'\'\')" \
                .format(method=line, arg=arg)
            exec(cmd_str)

    ip.register_magics(document_magics)
