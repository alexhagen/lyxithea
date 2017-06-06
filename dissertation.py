import datetime
from IPython.display import display, HTML, Markdown, Javascript, display_javascript
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

ip = get_ipython()

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


js = "require(\"notebook/js/cell\").Cell.options_default.cm_config.lineWrapping = true;\n"
#js += "require(\"notebook/js/cell\").CodeCell.options_default.cm_config.lineWrapping = true;\n"
#js += "require(\"notebook/js/cell\").MarkdownCell.options_default.cm_config.lineWrapping = true;\n"
#js = "console.log(Object.getOwnPropertyNames(require(\"notebook/js/cell\").CodeCell));\n"
js += "require(['notebook/js/codecell'], function(codecell) {\n"
js += "    codecell.CodeCell.options_default.highlight_modes['magic_markdown'] = {'reg':[/^%%dis/]}; \n"
js += "    Jupyter.notebook.events.one('kernel_ready.Kernel', function(){\n"
js += "      Jupyter.notebook.get_cells().map(function(cell){\n"
js += "          if (cell.cell_type == 'code'){ cell.auto_highlight(); } }) ;\n"
js += "      });\n"
js += "   });\n"
display_javascript(js, raw=True)

def cdis():
    if bi.__cdis__ is not None:
        return bi.__cdis__
    else:
        return dissertation()

class document(object):
    """ A document class """
    def __init__(self):
        pass


class dissertation(document):
    """ A dissertation class """
    def __init__(self, bib=None):
        if bib is None:
            self._bib = lyx.bib('bibs/dissertation.bib')
        else:
            self._bib = bib
        now = datetime.datetime.now()
        self._month = now.strftime("%B")
        self._year = now.strftime("%Y")
        self._chapter_paths = []
        self._data_paths = []
        bi.__cdis__ = self
        self._current_chapter = ''
        self._chapters = []
        super(dissertation, self).__init__()

    @staticmethod
    def check_chapter_path(path):
        """ checks if the chapter path is a legitimate path

        :param path: the path to the folder to be added
        :returns: boolean if the path is good or not
        """
        path = path.replace('~', os.path.expanduser('~'))
        return os.path.isdir(path)

    @staticmethod
    def get_locals():
        lcls = ip.user_module.__dict__
        return lcls

    def process_markdown(self, markdown):
        """ looks for python parameter notation in a markdown string

        :todo: Make this into a Jinja2 class for more flexibility.
        :todo: make a context manager for the markdown so I can use ``with``
            syntax
        """
        matches = re.finditer(bi.__regex__, markdown)

        for matchNum, match in enumerate(matches):
            with stdoutIO() as s:
                #lyx.markdown()
                lyx.latex()
                exec(match.group(1), self.get_locals())
                #lyx.latex(False)
                #lyx.markdown(False)
            rep_string = s.getvalue()
            if len(rep_string) < 1:
                cmd = "print {oldcmd}".format(oldcmd=match.group(1))
                with stdoutIO() as s:
                    #lyx.markdown()
                    lyx.latex()
                    exec(cmd, self.get_locals())
                    #lyx.latex(False)
                    #lyx.markdown(False)
                rep_string = s.getvalue()
            markdown = markdown.replace(match.group(), rep_string)
        return markdown

    def chapter_paths(self, paths):
        """ add paths to the chapter path variable

        :param paths: a list of string paths in the filesystem where chapters
            are found
        """
        for path in paths:
            if self.check_chapter_path(path):
                path = path.replace('~', os.path.expanduser('~'))
                self._chapter_paths.extend([path])

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
        return display(bi.__formatter__('\\begin{dedication}\n' + self._dedication +
                                '\\end{dedication}\n'))

    def acknowledgements(self, ack):
        self._acknowledgements = self.process_markdown(ack)
        return bi.__formatter__('\\begin{acknowledgements}\n' +
                                self._acknowledgements +
                                '\\end{acknowledgements}\n')

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

    def nom(self):
        return display(bi.__formatter__(r'\printnomenclature{}'))

    def abstract(self, abstract):
        self._abstract = self.process_markdown(abstract)
        return display(bi.__formatter__('\\begin{abstract}\n' + self._abstract +
                                        '\\end{abstract}'))

    def find_first(self, filename):
        for path in self._chapter_paths:
            for root, dirs, files in os.walk(path):
                for extension in ["ipynb", "lyx"]:
                    _fname = "{fname}.{ext}".format(fname=filename,
                                                    ext=extension)
                    if _fname in files:
                        return os.path.join(root, _fname)

    def chapter(self, filename):
        pass

    def replace_rel_paths(self, string, filename):
        print filename
        print os.path.split(filename)
        # find all paths in the string with a regex
        matches = re.compile(r"(([/]|\.\.|\./)([^.]*[\.][\w][\w][\w][\w]?|$))", flags=0) \
            .findall(string)
        print matches
        # for each path
        for match in matches:
            print match[0]
            rep_str = os.path.relpath(os.path.join(os.path.split(filename)[0], match[0]))
            print rep_str
            string.replace(match[0], rep_str)
        return string

    def append_notebook(self, filename, cells, child=True):
        _nb = nbformat.read(self.find_first(filename), 4)
        fpath = os.path.abspath(os.path.dirname(self.find_first(filename)))
        cells.extend([nbformat.v4.new_code_cell("import os; os.chdir(\'%s\')" % fpath)])
        for cell in _nb.cells:
            if cell['cell_type'] == 'code':
                if re.match('dis\.chapter\([\'\"](.*)[\'\"]\)', cell['source']) is None \
                    and re.match('dis\.appendix\([\'\"](.*)[\'\"]\)', cell['source']) is None \
                    and cell['source'] is not '' \
                    and re.match('dis\.export\([\'\"](.*)[\'\"]\)', cell['source']) is None:
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
                    self.append_notebook(import_filename, cells)
                elif re.match('dis\.appendix\([\'\"](.*)[\'\"]\)', cell['source']) is not None:
                    # find the argument of 'disappendix('
                    matches = re.match('dis\.appendix\([\'\"](.*)[\'\"]\)', cell['source'])
                    import_filename = matches.group(1)
                    self.append_notebook(import_filename, cells)
        #cells.extend([nbformat.v4.new_code_cell("os.chdir(\'%s\')" % self.cwd)])
        return cells

    def export(self, filename):
        #for path in self._chapter_paths[-1:0:-1]:
        #    os.system('cp -f {path}../img/*.svg img/'.format(path=path))
        #    os.system('cp -f {path}../img/*.svg img/'.format(path=path))
        nb = nbformat.v4.new_notebook()
        self.cwd = os.path.abspath(os.getcwd())
        cells = self.append_notebook(filename, [], child=False)
        nb['cells'] = cells

        nbformat.write(nb, 'temp_notebook.ipynb', 4)

        # now do the nb_convert to latex by executing
        nb = nbformat.read('temp_notebook.ipynb', 4)
        c = Config()
        c.HTMLExporter.preprocessors = \
            ['nbconvert.preprocessors.ExecutePreprocessor']
        c.LatexExporter.preprocessors = \
            ['nbconvert.preprocessors.ExecutePreprocessor']
        tmplt = r"""
            {%- extends 'full.tpl' -%}

            {% block input_group %}
            {% endblock input_group %}"""
        lyx.latex()
        lyx.markdown(False)
        #html_exporter = HTMLExporter(config=c, template_file='noinputhtmlfull.tpl')
        #(body, resources) = html_exporter.from_notebook_node(nb)
        bi.__formatter__ = Latex
        bi.__need_latex__ = True
        with open('nilf.tplx', 'w') as f:
            f.write(bi.__dissertation_template__)
        latex_exporter = LatexExporter(config=c, template_file='nilf.tplx')
        (body, resources) = latex_exporter.from_notebook_node(nb)
        with open('./' + filename + '.tex', 'w') as f:
            f.write(body)
        os.system('pdflatex ./' + filename + '.tex')
        os.system('bibtex ./' + filename)
        os.system('pdflatex ./' + filename + '.tex')
        os.system('pdflatex ./' + filename + '.tex')
        display(FileLink('./' + filename + '.pdf'))
        display(FileLink('./' + filename + '.tex'))
        #lyx.latex(False)
        os.remove('temp_notebook.ipynb')
        #os.remove(filename + '.out')
        #os.remove(filename + '.log')
        os.remove(filename + '.bbl')
        os.remove(filename + '.aux')
        os.remove(filename + '.blg')

    def appendix(self, filename):
        pass

    def bibliography(self):
        return self._bib.bibliography()

    def appendices(self):
        return Latex('\n \\appendices')

    def peek(self):
        html_str = """<h1>{title}</h1>
        <h2>{author}</h2>
        <p>{month}, {year}</p>
        """.format(title=self._title, author=self._author, month=self._month,
                   year=self._year)
        return bi.__formatter__(html_str)

    def set_hide_dblclick(self, string):
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

    def add_to_cchap(self, string):
        processed_string = self.process_markdown(string)
        self._current_chapter += processed_string
        return display(bi.__formatter__(processed_string))

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
