from __future__ import division
from __future__ import print_function
from tabulate import tabulate
from IPython.display import SVG
from IPython.display import display
from IPython.display import Latex
from IPython.display import HTML
from IPython.display import Javascript
from IPython.display import FileLink
from IPython.display import Markdown
import sys
import os
import os.path
import subprocess
import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
#import __builtins__ as bi
from . import utils as bi
import tempfile
import psgv.psgv as psgv
import re
import numpy as np
#from pytexit import pytexit
import inspect

todos = psgv.psgv('__todos__')
todos.val = []
__needs_latex__ = psgv.psgv('__needs_latex__')
__needs_latex__.val = False
__needs_markdown__ = psgv.psgv('__needs_markdown__')
__needs_markdown__.val = True
__labels__ = psgv.psgv('__lyxlabels__')
__labels__.val = {}
__tabcount__ = psgv.psgv('__lyxtabcount__')
__tabcount__.val = 1
__tables__ = psgv.psgv('__lyxtables__')
__tables__.val = {}
__figures__ = psgv.psgv('__lyxfigures__')
__figures__.val = {}
__figcount__ = 1
__chapters__ = psgv.psgv('__lyxchapters__')
__chapters__.val = {}
__sections__ = psgv.psgv('__lyxsections__')
__sections__.val = {}
__subsections__ = psgv.psgv('__lyxsubsections__')
__subsections__.val = {}
__eqs__ = psgv.psgv('__lyxeqs__')
__eqs__.val = {}
__lsts__ = psgv.psgv('__lyxlsts__')
__lsts__.val = {}
__itms__ = psgv.psgv('__lyxitms__')
__itms__.val = {}
__algs__ = psgv.psgv('__lyxalgs__')
__algs__.val = {}
__apps__ = psgv.psgv('__lyxapps__')
__apps__.val = {}
__exporting__ = psgv.psgv('__lyxexporting__')
__exporting__.val = False
__context__ = psgv.psgv('__context__')


def get_pname(id):
    """Check the process name.

    An internal command to determine the process name of the current exporting
    process.
    """
    p = subprocess.Popen(["ps -o cmd= {}".format(id)], stdout=subprocess.PIPE,
                         shell=True)
    return str(p.communicate()[0])


def run_from_ipython():
    """ An internal command to determine if the script is running from IPython
            or just from a regular Python console.

        :returns bool: True if in an IPython notebook, false otherwise.
    """
    try:
        __IPYTHON__
        return True
    except NameError:
        return False

def need_latex():
    """ An internal command to determine if we need to compile in LaTeX

        :returns bool: True if we need to compile in LaTeX, false otherwise.

        :todo: Make ``need_latex`` process dependent
    """
    return __needs_latex__.val

def need_markdown():
    """ An internal command to determine if we need to compile in Markdown

        :returns bool: True if we need to compile in Markdown, false otherwise.

        :todo: Make ``need_markdown`` process dependent
    """
    return __needs_markdown__.val

def latex(i=True):
    __needs_latex__.val = i

def exporting(i=True):
    __exporting__.val = i

def is_exporting():
    return __exporting__.val

def markdown(i=True):
    __needs_markdown__.val = i

def tex_escape(text):
    """
        :param text: a plain text message
        :return: the message escaped to appear correctly in LaTeX
    """
    conv = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless',
        '>': r'\textgreater',
    }
    regex = re.compile('|'.join(re.escape(unicode(key)) for key in sorted(conv.keys(), key = lambda item: - len(item))))
    return regex.sub(lambda match: conv[match.group()], text)

def table_no_caption(array, headers=None, floatfmt=".2f"):
    if run_from_ipython() and not need_latex():
        table = tabulate.tabulate(array, headers=headers, tablefmt='html',
                         numalign='center', stralign='center',
                         floatfmt=floatfmt)
        return str(table)
    elif run_from_ipython() and need_latex():
        table = tabulate.tabulate(array, headers=headers, tablefmt='latex_raw',
                         numalign='center', stralign='center',
                         floatfmt=floatfmt)
        return str(table)

def threeparttable(array, headers=None, label=None, caption='', floatfmt=".2f",
                   after='', sideways=False):
    if run_from_ipython() and need_latex():
        table = tabulate.tabulate(array, headers=headers, tablefmt='latex_raw',
                         numalign='center', stralign='center',
                         floatfmt=floatfmt)
        if sideways:
            env = 'sidewaystable'
        else:
            env = 'table'
        strlatex = r"""
        \begin{%s}
            \centering
            \begin{threeparttable}
                \caption{%s\label{tab:%s}}
                %%\begin{adjustbox}{max width=\textwidth}
                    %s
                %%\end{adjustbox}
                \begin{tablenotes}
                %s
                \end{tablenotes}
            \end{threeparttable}
        \end{%s}""" % (env, caption, label, table, after, env)
        __tables__.val[label] = __tabcount__.val
        __tabcount__.val += 1
        return display(Latex(strlatex))

def includepdf(filename, pages=None):
    if pages is None:
        strlatex = r"""\includepdf[pages=-]{%s.pdf}
        """ % filename
    return strlatex

def table(array, caption='', label=None, headers=None, floatfmt=".2f",
          sideways=False, span_columns=False, need_string=False,
          rotate=False, extrarowheight=0):
    if rotate:
        array = np.fliplr(np.rot90(np.rot90(np.rot90(array))))
    if label is None:
        label = __tabcount__.val
        #print __tabcount__
    if sideways:
        env = 'sidewaystable'
    elif span_columns:
        env = 'table*'
    else:
        env = 'table'
    if headers:
        if not all(isinstance(el, list) for el in headers):
            headers = [headers]
    #print headers
    if run_from_ipython() and not need_latex():
        table = tabulate.tabulate(array, headers=headers, tablefmt='html',
                         numalign='center', stralign='center',
                         floatfmt=floatfmt)
        __tables__.val[label] = __tabcount__.val
        fig_html = r"""
            <div class='table' style='align: center; margin-left: auto; margin-right: auto;'>
                <div style='margin: auto; text-align: center;' class='tablecaption' name='%s'><b>Table %d:</b> %s</div>
                %s
            </div>
        """ % (label, __tabcount__.val, caption, table)
        __tabcount__.val += 1
        if need_markdown():
            return display(HTML(fig_html))
        else:
            return display(HTML(fig_html))
    elif run_from_ipython() and need_latex():
        table = tabulate.tabulate(array, headers=headers, tablefmt='latex_raw',
                         numalign='center', stralign='center',
                         floatfmt=floatfmt)
        strlatex = r"""
        \begin{%s}
            \centering
            \caption{%s\label{tab:%s}}
            %%\begin{adjustbox}{max width=\textwidth}
                \setlength\extrarowheight{%dpt}
                %s
            %%\end{adjustbox}
        \end{%s}""" % (env, caption, label, extrarowheight, table, env)
        __tables__.val[label] = __tabcount__.val
        __tabcount__.val += 1
        if need_string:
            return strlatex
        return display(Latex(strlatex))

def to_pdf():
    if 'jupyter-nbconvert' not in get_pname(os.getpid()) + get_pname(os.getppid()):
        with open('/tmp/need_latex', 'w') as f:
            f.write('True')
        f.close()
        os.chdir(os.getcwd())
        subprocess.cwd = os.getcwd()
        if False:
            # first lets remove all of the cell metadata
            display(Javascript("""
                var ncells = IPython.notebook.ncells();
                var cells = IPython.notebook.get_cells();
                for (var i = 0; i < ncells; i++) {
                    var cell = cells[i];
                    if (cell.metadata.hasOwnProperty('variables')) {
                        delete cell.metadata.variables;
                    }
                }
                """))
            # and, lets run all of the cells, but this should include latex stuff
            display(Javascript("""
                require(['base/js/namespace',
                        'jquery',
                        'notebook/js/cell',
                        'base/js/security',
                        'components/marked/lib/marked',
                        'base/js/events'],
                function(jupyter, $, events) {
                    "use strict";
                    var runall = function() {
                        console.log("Auto-running all cells above...");
                        events.on("rendered.MarkdownCell", function (event, data) {
                            var element = data.cell.element.find('div.text_cell_render');
                            console.log('editing a cell');
                            var text = execute_python(data.cell, element[0].innerHTML);
                            if (text !== undefined) {
                                element[0].innerHTML = text;
                                MathJax.Hub.Queue(["Typeset",MathJax.Hub,element[0]]);
                            }
                        });
                        jupyter.actions.call('jupyter-notebook:run-all-cells-above');
                        jupyter.actions.call('jupyter-notebook:save-notebook');
                    };
                    return {
                        runall : runall
                    };
                });
            """))
        # now lets actually convert it
        cmd = 'jupyter nbconvert --to latex stored_energy_fingerprints.ipynb'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        if os.path.exists("/tmp/need_latex"):
            os.remove("/tmp/need_latex")
        if False:
            display(Javascript("""
                require(['base/js/namespace', 'jquery'],
                function(jupyter, $) {
                    console.log("Auto-running all cells-below...");
                    jupyter.actions.call('jupyter-notebook:run-all-cells-above');
                    jupyter.actions.call('jupyter-notebook:save-notebook');
                });
            """))


def nom(abbr, extended, kind='abbr'):
    """Add the entry to the document's nomenclature.

    :param str abbr: The label for the nomenclature entry
    :param str extended: The extended description for the nomenclature entry
    :param str kind: The kind of nomenclature entry, choice of ``'abbr'`` for
        an abbreviation, ``'symb'`` for a symbol, ``'subsup'`` for a super- or
        sub- script, ``'unit'`` for a type of unit, ``'def'`` or ``'defs'`` for
        a definition.
    """
    if abbr not in bi.__nom__.keys():
        bi.__nom__[kind] = {}
        bi.__nom__[kind][abbr] = extended
    if run_from_ipython() and not need_latex():
        html_str = "<span class='abbr' data-wenk='{extd}'>{abbr}</span>"\
            .format(abbr=abbr, extd=extended)
        if need_markdown():
            return html_str
        else:
            return display(HTML(html_str))
    elif run_from_ipython() and need_latex():
        kinds = {'abbr': 'A', 'symb': 'Y', 'subsup': 'S',
                 'unit': 'U', 'units': 'U',
                 'def': 'D', 'defs': 'D'}
        latex_str = r"%s\nomenclature[%s]{%s}{%s}" % \
            (abbr, kinds[kind], abbr,
             extended)
        return latex_str


def lipsum():
    """Write random text as filler.

    Lorem Ipsum is latin filler text.  ``lipsum`` returns 500 words of filler
    text, right now in HTML

    :todo: Write lipsum to actually output some of the words from lorem ipsum
    """
    html_str = '<p>'
    for i in range(0, 500):
        html_str += 'word '
    html_str += '</p>'
    return display(HTML(html_str))

class bib(object):
    def __init__(self, filename='bibs/dissertation', style='unsrt'):
        self.bib_dict = {}
        self.style = style
        self.cited_labels = []
        self.full_filename = os.path.expanduser('~/') + filename
        self.add_bib(self.full_filename)

    def __eq__(self, other):
        eq = True
        for key, val in self.__dict__.iteritems():
            if other.__dict__[key] != val and not hasattr(other.__dict__[key], '__dict__'):
                print(val, other.__dict__[key])
                return False
            else:
                print(val, other.__dict__[key])
        return isinstance(other, type(self)) and self.__dict__ == other.__dict__

    def add_bib(self, filename):
        self.bib_fname = filename
        if run_from_ipython():
            with open(self.bib_fname, 'r') as bib_file:
                self.bib_db = bibtexparser.load(bib_file)
                for entry in self.bib_db.entries:
                    self.bib_dict[entry['ID']] = entry

    def fullcite(self, label):
        if label not in self.bib_dict.keys():
            pcitestr = '\[%s\]' % label
            todo('fix {citation} citation'.format(citation=label))
            if need_markdown():
                return pcitestr
            elif need_latex():
                return pcitestr# r'\cite{%s}' % label
            else:
                return display(HTML(pcitestr))
        if not need_latex():
            d = self.bib_dict[label]
            if label not in self.cited_labels:
                self.cited_labels.extend([label])
            pcitestr = '('
            pcitestr += '<a href="{link}">'.format(link='#' + label)
            pcitestr += d['author'].partition(' ')[0] + ' '
            if len(d['author'].split(',')) > 2:
                pcitestr += ' et. al.'
            pcitestr += ' ' + d['year']
            pcitestr += '</a>'
            pcitestr += ')'
            pcitestr = self.html_citation(label)
            if need_markdown():
                return pcitestr
            elif need_latex():
                return display(Latex('\[%s\]' % label))
            else:
                return display(HTML(pcitestr))
        elif need_latex():
            pcitestr = self.html_citation(label)
            return r'%s' % (pcitestr)

    def pcite(self, label, page=None):
        if isinstance(label, str) and label not in self.bib_dict.keys():
            pcitestr = '\[%s\]' % label
            todo('fix {citation} citation'.format(citation=label))
            if need_markdown():
                return pcitestr
            elif need_latex():
                return pcitestr# r'\cite{%s}' % label
            else:
                return display(HTML(pcitestr))
        if not need_latex():
            d = self.bib_dict[label]
            if label not in self.cited_labels:
                self.cited_labels.extend([label])
            pcitestr = '('
            pcitestr += '<a href="{link}">'.format(link='#' + label)
            pcitestr += d['author'].partition(' ')[0] + ' '
            if len(d['author'].split(',')) > 2:
                pcitestr += ' et. al.'
            pcitestr += ' ' + d['year']
            pcitestr += '</a>'
            pcitestr += ')'
            if need_markdown():
                return pcitestr
            elif need_latex():
                if isinstance(label, list):
                    labelstr = ''
                    for _label in label:
                        labelstr += '%s,' % _label
                    labelstr = labelstr[:-1]
                    label = labelstr
                if page is not None:
                    pagestr = '[%s]' % page
                else:
                    pagestr = ''
                return display(Latex(r'\cite%s{%s}' % (pagestr, label)))
            else:
                return display(HTML(pcitestr))
        elif need_latex():
            if isinstance(label, list):
                labelstr = ''
                for _label in label:
                    labelstr += '%s,' % _label
                labelstr = labelstr[:-1]
                label = labelstr
            if page is not None:
                pagestr = '[%s]' % page
            else:
                pagestr = ''
            return r'\cite%s{%s}' % (pagestr, label)

    def html_citation(self, label):
        bibdb = BibDatabase()
        bibdb.entries = [self.bib_dict[label]]
        bibtex_str = bibtexparser.dumps(bibdb)
        from subprocess import Popen, PIPE
        import shlex
        f = tempfile.NamedTemporaryFile(suffix=".bib", delete=False)
        f.write(bibtex_str)
        f.close()
        system_str = 'bibtex2html -nokeys -o - -s plain -nodoc -q {fname}'.format(fname=f.name)
        args = shlex.split(system_str)
        proc = Popen(args, stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()
        exitcode = proc.returncode
        f.close()
        os.remove(f.name)
        result = out.replace("""<!-- This document was automatically generated with bibtex2html 1.98
(see http://www.lri.fr/~filliatr/bibtex2html/),
with the following command:
bibtex2html -nokeys -o - -s plain -nodoc -q temp.bib  -->




""", '').replace("""<hr><p><em>This file was generated by
<a href="http://www.lri.fr/~filliatr/bibtex2html/">bibtex2html</a> 1.98.</em></p>""", '')
        #print out, err, exitcode
        htmlstr = '<li name="{name}">{citation}</li>\n'.format(name=label, citation=result)
        return htmlstr


    def bibliography(self, header_level=2, force_string=False):
        if run_from_ipython() and not need_latex():
            htmlstr = '<h{hl}>Bibliography</h{hl}>\n'.format(hl=header_level)
            htmlstr += '<ol>\n'
            for label in self.cited_labels:
                htmlstr += self.html_citation(label)
            htmlstr += '</ol>\n'
            if need_markdown():
                return display(HTML(htmlstr))
            elif need_latex():
                return r'\bibliographystyle{%s} \bibliography{%s}' % (self.style, self.full_filename)
            else:
                return display(HTML(htmlstr))
        elif need_latex():
            os.system('iconv -f utf-8 -t ascii -c {0} -o {1}'.format(self.full_filename, self.full_filename.replace('.bib', 'bak.bib')))
            if force_string:
                return r'\bibliographystyle{%s} \bibliography{%s}' % (self.style, self.full_filename.replace('.bib', 'bak.bib'))
            return Latex(r'\bibliographystyle{%s} \bibliography{%s}' % (self.style, self.full_filename.replace('.bib', 'bak.bib')))


def figures():
    print(__tables__.val)
    print(__figures__.val)
    print(__labels__.val)


def ack(person, task=''):
    """Acknowledge a person for doing a task.

    :param str person: The person to acknowledge.
    :param str task: The the person is being acknowledged for.
    """
    return '\invis{%s: %s}' % (person, task)


def todo(task):
    """Add a task to a saved todo list that can be referenced latex.

    :param str task: The task to be saved.
    """
    if task not in todos.val:
        todos.val.extend([task])
    if run_from_ipython() and not need_latex():
        if need_markdown():
            return display(Markdown(''))
        elif need_latex():
            return r'\todo{%s}' % task
        else:
            return display(HTML(''))
    else:
        return r'\todo{%s}' % task


def ul(text, color='000000'):
    """Underline text.

    :param str text: The text to underline
    :param str color: The color of the underline - defaults to black
    """
    latexstr = (r'\definecolor{ulcolor}{HTML}{%s}\setulcolor{ulcolor}' % color)
    latexstr += (r'\ul{%s}' % text)
    return latexstr

def fixme(task):
    if task not in todos.val:
        todos.val.extend([task])
    if run_from_ipython() and not need_latex():
        if need_markdown():
            return display(Markdown(''))
        elif need_latex():
            return r'\todo{%s}' % task
        else:
            return display(HTML(''))
    else:
        return r'\todo{%s}' % task

def export_todos():
    with open('todos.md', 'w') as f:
        f.write('# Todos \n')
        for task in todos.val:
            f.write('- [ ] {task}\n'.format(task=task))
    os.system('pandoc todos.md -t latex -o todos.pdf')
    with open('todos.tex', 'w') as f:
        f.write(r"""\documentclass{article}
\usepackage{enumitem,amssymb}
\newlist{todolist}{itemize}{2}
\setlist[todolist]{label=$\square$}
\begin{document}
\section{ToDos}

\begin{todolist}""")
        for task in todos.val:
            f.write("\item {task}\n".format(task=task))
        f.write(r'\end{todolist}' + '\n')
        f.write(r'\end{document}')
    os.system('pdflatex todos.tex')

def print_todos():
    if not need_latex():
        html_str = ''
        for task in bi.__todos__:
            html_str += "<li>{task}</li>\n".format(task=task)
        if need_markdown():
            return html_str
        elif need_latex():
            # we should write to another file here!
            # export_todos()
            return display(FileLink('todos.pdf'))
    elif need_latex():
        export_todos()
        return display(FileLink('todos.pdf'))

def label(label):
    if run_from_ipython() and not need_latex():
        if 'fig:' not in label and 'tab:' not in label:
            number = __labels__.val
    elif need_latex():
        return r'\label{%s}' % label

def cref(label, rename=None):
    if run_from_ipython() and not need_latex():
        if label in __tables__.val.keys():
            number = __tables__.val[label]
            text = 'table'
        elif label in __figures__.val.keys():
            number = __figures__.val[label]
            text = 'figure'
        else:
            text = 'ref'
            number = 0
        html_str = '<a href="#%s">%s %d</a>' % (label, text, number)
        if need_markdown():
            return html_str
        elif need_latex():
            if label in __tables__.val.keys():
                number = __tables__.val[label]
                text = 'tab:'
            elif label in __figures__.val.keys():
                number = __figures__.val[label]
                text = 'fig:'
            else:
                text = ''
                number = 0
            return r'\ref{%s%s}' % (text, label)
        else:
            return display(HTML(html_str))
    elif run_from_ipython() and need_latex():
        if label in __tables__.val.keys():
            number = __tables__.val[label]
            text = 'tab:'
            name = 'table '
        elif label in __figures__.val.keys():
            number = __figures__.val[label]
            text = 'fig:'
            name = 'figure '
        else:
            text = ''
            number = 0
            if rename is None:
                name = ''
                return r'\cref{%s%s}' % (text, label)
            else:
                name = rename + ' '
                return r'%s\ref{%s%s}' % (name, text, label)
        return r'%s\ref{%s%s}' % (name, text, label)


def scinot(number, unit='', precision='2e', math=True):
    """Convert a number and unit into a scientific notation LaTeX string.

    :param float number: the number to convert
    :param str unit: a legal LaTeX string defining the units
    :param str precision: the precision without the ``'.'``, defaults to
        ``'2e'``
    """
    string = r'{1:.{0}}'.format(precision, number)
    string = r'%s}\unit{%s}' % (string, unit)
    if math:
        string = r'$' + string + r'$'
    string = string.replace('e+0', r'\times 10^{')\
        .replace('e-0', r'\times 10^{-')\
        .replace('e+', r'\times 10^{')\
        .replace('e-', r'\times 10^{-')
    return string


def figures(figures, captions=[], caption='', filenames=[], labels=[],
            widths=[], label=''):
    __context__.val = 'thesis'
    __figcount__ = 1
    for figure, filename, width, label in zip(figures, filenames, widths, labels):
        figure.export(filename, sizes=[width], formats=['pgf'], force=True,
                      context='thesis')
        __figures__.val[label] = __figcount__
        __figcount__ += 1
    string = r'''
    \begin{figure*}%%
        \centering
        \subfloat[%s\label{fig:%s}]{{\input{%s} }}%%
        \subfloat[%s\label{fig:%s}]{{\input{%s} }}%%
        \caption{%s}%%
        \label{%s}%%
    \end{figure*}
    ''' % (captions[0], labels[0], figures[0].pgf_filename,
           captions[1], labels[1], figures[1].pgf_filename,
           caption, label)
    return display(Latex(string))

def fnote(content):
    if run_from_ipython() and not need_latex():
        return r'<span class="fnote">%s</span>' % content
    elif need_latex():
        return r'\footnote{%s}' % content

def video(path, replace=None, width='7.5in', height='5.0in',
          caption='', label=''):
    if 'http' not in path:
        resource = 'addresource%s,' % path
    else:
        resource = ''
        path.replace('~', r'\textasciitilde{}')
    latexstr = r'''
    \begin{figure}
        \centering
        \includemedia[width=%s, activate=onclick,
                      transparent,
                      %s keepaspectratio,
                      flashvars={source=%s&autoPlay=true}
                      ]{\includegraphics[width=%s]{%s}}{VPlayer.swf}
        \caption{%s\label{fig:%s}}
    \end{figure}''' % (width, resource, path, width, replace, caption, label)
    return latexstr

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def pyf2tex(func, deps=False, f_syntax=False, show=False, rename=False):
    string = inspect.getsource(func)
    # remove any decorators
    x = find_between(string, '@', '\n')
    string = string.replace('@' + x, '')
    _deps = ','.join([pytexit.py2tex(_dep, print_latex=False, print_formula=False).replace('$$', '') for _dep in string.split('(')[1].split(')')[0].replace('self, ', '').split(',')])
    if f_syntax:
        if not deps:
            _name = 'f12345'
            _replace = 'f({})'.format(_deps)
            deps = True
        else:
            _name = string.split('(')[0].replace('def ', '')
            texname = pytexit.py2tex(_name, print_latex=False, print_formula=False).replace('$$', '')
            _replace = '{}({})'.format(texname, _deps)
            _name = 'f12345'
    elif rename:
        if not deps:
            _name = string.split('(')[0].replace('def ', '')
            _replace = '{}'.format(rename)
            _name = 'f12345'
        else:
            _name = string.split('(')[0].replace('def ', '')
            _replace = '{}({})'.format(rename, _deps)
            _name = 'f12345'
    else:
        _name = string.split('(')[0].replace('def ', '')
        _replace = r'{}({})'.format(_name, _deps)
    _return = string.split('return')[-1]
    string = '{variable} = {function}'.format(variable=_name, function=_return)
    string = pytexit.py2tex(string, print_latex=False, print_formula=False)
    if deps or rename:
        string = string.replace(_name, _replace)
    if show:
        display(Latex(string))
    return string

def equation(**kwargs):
    def real_equation(function):
        function.__latex__ = pyf2tex(function, **kwargs)
        def wrapper(*args, **kwargs):
            pass
        return function
    return real_equation
