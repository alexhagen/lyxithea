import datetime
from IPython.display import display, HTML, Markdown, Javascript, display_javascript
from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)
from IPython.display import FileLink, JSON, DisplayObject
import os.path
import os
import re
import sys
import StringIO
import contextlib
import inspect
import nbformat
from nbconvert import HTMLExporter
from IPython.display import display, HTML
from traitlets.config import Config
from jinja2 import DictLoader
from IPython.core.magics.code import CodeMagics
import lyxithea as lyx
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

    def find_first(self, filename):
        for path in self._chapter_paths:
            for root, dirs, files in os.walk(path):
                for extension in ["ipynb", "lyx"]:
                    _fname = "{fname}.{ext}".format(fname=filename,
                                                    ext=extension)
                    if _fname in files:
                        return os.path.join(root, _fname)

    def chapter(self, filename):
        nb = nbformat.read(filename, as_version=4)
        nb2 = nbformat.read('test_export.ipynb', as_version=4)
        print nb.cells
        for cell in nb.cells:
            nb2.new_code_cell(cell.source)
        #if False: #not os.path.isfile('/tmp/convertingjupyter'):
        #ip.magic("load " + filename)
        #else:
        #return display(JSON(nbformat.read(filename, as_version=4)))

    def export(self, filename):
        if not os.path.isfile('/tmp/convertingjupyter'):
            os.system('touch /tmp/convertingjupyter')
            with open('./' + filename + '.ipynb', 'r') as f:
                string = f.read()
            nb = nbformat.reads(string, as_version=4)
            c = Config()
            c.HTMLExporter.preprocessors = \
                ['nbconvert.preprocessors.ExecutePreprocessor']
            tmplt = r"""
                {%- extends 'full.tpl' -%}

                {% block input_group %}
                {% endblock input_group %}"""
            with open('noinputhtmlfull.tpl', 'w') as f:
                f.write(tmplt)
            html_exporter = HTMLExporter(config=c, template_file='noinputhtmlfull.tpl')
            (body, resources) = html_exporter.from_notebook_node(nb)
            with open('./' + filename + '.html', 'w') as f:
                f.write(body)
            display(FileLink('./' + filename + '.html'))
        else:
            os.system('rm /tmp/convertingjupyter')


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

    def add_to_cchap(self, string):
        processed_string = self.process_markdown(string)
        self._current_chapter += processed_string
        display(Markdown(processed_string))
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
            var ev = $._data($(this), 'events');
            if (!(ev && ev.dblclick)) {
                $(this).dblclick(code_toggle);
            }
        });"""
        display(Javascript(javascript_str))
        return self

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
