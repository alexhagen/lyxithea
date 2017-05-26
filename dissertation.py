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
import __builtin__
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

js = "IPython.CodeCell.config_defaults.highlight_modes['magic_markdown'] = {'reg':[/^%%dis/]}; \n"
js += "IPython.Cell.options_default.cm_config.lineWrapping = true;"
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
                lyx.markdown()
                exec(match.group(1), self.get_locals())
                lyx.markdown(False)
            rep_string = s.getvalue()
            if len(rep_string) < 1:
                cmd = "print {oldcmd}".format(oldcmd=match.group(1))
                with stdoutIO() as s:
                    lyx.markdown()
                    exec(cmd, self.get_locals())
                    lyx.markdown(False)
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
        return bi.__formatter__(self._dedication)

    def acknowledgements(self, ack):
        self._acknowledgements = self.process_markdown(ack)
        return bi.__formatter__(self._acknowledgements)

    def preface(self, preface):
        self._preface = self.process_markdown(preface)
        return display(bi.__formatter__(self._preface))

    def toc(self):
        pass

    def lot(self):
        pass

    def lof(self):
        pass

    def nom(self):
        pass

    def abstract(self, abstract):
        self._abstract = self.process_markdown(abstract)
        return display(bi.__formatter__(self._abstract))

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

    def export(self, filename):
        nb = nbformat.v4.new_notebook()

        def append_notebook(filename, cells):
            _nb = nbformat.read(self.find_first(filename), 4)
            for cell in _nb.cells:
                if cell['cell_type'] == 'code':
                    if re.match('dis\.chapter\([\'\"](.*)[\'\"]\)', cell['source']) is None \
                        and re.match('dis\.appendix\([\'\"](.*)[\'\"]\)', cell['source']) is None \
                        and cell['source'] is not '' \
                        and re.match('lyx\.print_todos\(\)', cell['source']) is None \
                        and re.match('dis\.export\([\'\"](.*)[\'\"]\)', cell['source']) is None:
                        cell_to_add = nbformat.v4.new_code_cell(cell['source'])
                        cells.extend([cell_to_add])
                    elif re.match('dis\.chapter\([\'\"](.*)[\'\"]\)', cell['source']) is not None:
                        # find the argument of 'dischapter('
                        matches = re.match('dis\.chapter\([\'\"](.*)[\'\"]\)', cell['source'])
                        import_filename = matches.group(1)
                        append_notebook(import_filename, cells)
                    elif re.match('dis\.appendix\([\'\"](.*)[\'\"]\)', cell['source']) is not None:
                        # find the argument of 'disappendix('
                        matches = re.match('dis\.appendix\([\'\"](.*)[\'\"]\)', cell['source'])
                        import_filename = matches.group(1)
                        append_notebook(import_filename, cells)
            return cells
        cells = append_notebook(filename, [])
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
        tmplt = r"""
            ((*- extends 'article.tplx' -*))

            ((* block input_group *))
                ((*- if cell.metadata.get('nbconvert', {}).get('show_code', False) -*))
                    ((( super() )))
                ((*- endif -*))
            ((* endblock input_group *))

            ((* block data_latex -*))
                ((( output.data['text/latex'] | strip_files_prefix )))
            ((* endblock data_latex *))

            ((* block packages *))
            ((( super() )))
            \usepackage{tikz}
            \newcommand{\unit}[1]{\mathrm{#1}}
            \newcommand{\ce}[1]{\mathrm{#1}}
            ((* endblock packages *))

            % Author and Title from metadata
            ((* block maketitle *))

            ((*- if nb.metadata["latex_metadata"]: -*))
            ((*- if nb.metadata["latex_metadata"]["author"]: -*))
                \author{((( nb.metadata["latex_metadata"]["author"] )))}
            ((*- endif *))
            ((*- else -*))
                \author{Alex Hagen}
            ((*- endif *))

            ((*- if nb.metadata["latex_metadata"]: -*))
            ((*- if nb.metadata["latex_metadata"]["affiliation"]: -*))
                \affiliation{((( nb.metadata["latex_metadata"]["affiliation"] )))}
            ((*- endif *))
            ((*- endif *))

            ((*- if nb.metadata["latex_metadata"]: -*))
            ((*- if nb.metadata["latex_metadata"]["title"]: -*))
                \title{((( nb.metadata["latex_metadata"]["title"] )))}
            ((*- endif *))
            ((*- else -*))
                \title{((( resources.metadata.name )))}
            ((*- endif *))

            \date{\today}
            \maketitle
            ((* endblock maketitle *))"""
        with open('noinputlatexfull.tplx', 'w') as f:
            f.write(tmplt)
        #html_exporter = HTMLExporter(config=c, template_file='noinputhtmlfull.tpl')
        #(body, resources) = html_exporter.from_notebook_node(nb)
        bi.__formatter__ = Latex
        __need_latex__ = True
        latex_exporter = LatexExporter(config=c, template_file='noinputlatexfull.tplx')
        (body, resources) = latex_exporter.from_notebook_node(nb)
        with open('./' + filename + '.tex', 'w') as f:
            f.write(body)
        os.system('pdflatex ./' + filename + '.tex')
        os.system('bibtex ./' + filename)
        os.system('pdflatex ./' + filename + '.tex')
        os.system('pdflatex ./' + filename + '.tex')
        display(FileLink('./' + filename + '.pdf'))
        display(FileLink('./' + filename + '.tex'))
        #os.remove('temp_notebook.ipynb')

    def appendix(self, filename):
        pass

    def bibliography(self):
        return self._bib.bibliography()

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
        cmd_str = "cdis.{method}(r\'\'\'{arg}\'\'\')" \
            .format(method=line, arg=arg)
        exec(cmd_str)

ip.register_magics(dissertation_magics)
