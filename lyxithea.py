from tabulate import tabulate
from IPython.display import SVG, display, Latex, HTML, Javascript
import sys
import os
import os.path
import subprocess
import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
import __builtins__ as bi
import tempfile

def get_pname(id):
    p = subprocess.Popen(["ps -o cmd= {}".format(id)], stdout=subprocess.PIPE, shell=True)
    return str(p.communicate()[0])

def run_from_ipython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False

def need_latex():
    cmds = get_pname(os.getpid())
    cmds += get_pname(os.getppid())
    if 'jupyter-nbconvert' in cmds and ('to pdf' in cmds or 'to latex' in cmds):
        import IPython
        ip = IPython.core.getipython.get_ipython()
        ip.display_formatter.formatters['text/latex'].enabled = True
        return True
    else:
        return os.path.isfile('/tmp/need_latex')

def need_markdown():
    return os.path.isfile('/tmp/need_markdown')

def markdown(i=True):
    if i:
        os.system('touch /tmp/need_markdown')
    else:
        os.system('rm /tmp/need_markdown')

def table(array, caption='', label=None, headers=None, floatfmt=".2f"):
    if label is None:
        label = caption
    if run_from_ipython() and not need_latex():
        table = tabulate(array, headers=headers, tablefmt='html',
                         numalign='center', stralign='center',
                         floatfmt=floatfmt)
        fig_html = r"""
            <div class='table' style='align: center; margin-left: auto; margin-right: auto;'>
                <div style='margin: auto; text-align: center;' class='tablecaption' name='%s'><b>Table %d:</b> %s</div>
                %s
            </div>
        """ % (label, bi.__tabcount__, caption, table)
        bi.__tables__[label] = bi.__tabcount__
        bi.__tabcount__ += 1
        if need_markdown():
            return fig_html
        else:
            return display(HTML(fig_html))
    elif run_from_ipython() and need_latex():
        table = tabulate(array, headers=headers, tablefmt='latex',
                         numalign='center', stralign='center',
                         floatfmt=floatfmt)
        strlatex = r"""
        \begin{table}
            \centering
            %s
            \caption{%s}
            \label{tab:%s}
        \end{table}""" % (table, caption, label)
        display(Latex(strlatex))

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
    if abbr not in bi.__nom__[kind].keys():
        bi.__nom__[kind][abbr] = extended
    if run_from_ipython() and not need_latex():
        html_str = "<span>{abbr}</span>".format(abbr=abbr)
        if need_markdown():
            return html_str
        else:
            return display(HTML(html_str))
    elif run_from_ipython() and need_latex():
        pass

def lipsum():
    html_str = '<p>'
    for i in range(0, 500):
        html_str += 'word '
    html_str += '</p>'
    return display(HTML(html_str))

class bib(object):
    def __init__(self, filename='bibs/dissertation.bib', style='unsrt'):
        self.bib_dict = {}
        self.style = style
        self.cited_labels = []
        self.full_filename = os.path.expanduser('~/') + filename
        self.add_bib(self.full_filename)

    def add_bib(self, filename):
        self.bib_fname = filename
        if run_from_ipython() and not need_latex():
            with open(self.bib_fname, 'r') as bib_file:
                self.bib_db = bibtexparser.load(bib_file)
                for entry in self.bib_db.entries:
                    self.bib_dict[entry['ID']] = entry

    def pcite(self, label):
        if label not in self.bib_dict:
            pcitestr = '(??)'
            todo('fix {citation} citation'.format(citation=label))
            if need_markdown():
                return pcitestr
            else:
                return display(HTML(pcitestr))
        if run_from_ipython() and not need_latex():
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
            else:
                return display(HTML(pcitestr))
        elif run_from_ipython() and need_latex():
            return Latex(r'\cite{%s}' % label)

    def bibliography(self, header_level=2):
        if run_from_ipython() and not need_latex():
            htmlstr = '<h{hl}>Bibliography</h{hl}>\n'.format(hl=header_level)
            htmlstr += '<ol>\n'
            for label in self.cited_labels:
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
                htmlstr += '<li name="{name}">{citation}</li>\n'.format(name=label, citation=result)
            htmlstr += '</ol>\n'
            if need_markdown():
                return htmlstr
            else:
                return display(HTML(htmlstr))
        elif run_from_ipython() and need_latex():
            return display(Latex(r'\bibliographystyle{%s} \bibliography{"%s"}' % (self.style, self.full_filename)))


def figures():
    print bi.__tables__
    print bi.__figures__
    print bi.__labels__

def todo(task):
    if task not in bi.__todos__:
        bi.__todos__.extend([task])
    if run_from_ipython and not need_latex():
        if need_markdown():
            return ''
        else:
            return display(HTML(''))

def print_todos():
    if run_from_ipython and not need_latex():
        html_str = ''
        for task in bi.__todos__:
            html_str += "<li>{task}</li>\n".format(task=task)
        if need_markdown():
            return html_str
        else:
            return display(HTML(html_str))

def label(label):
    if run_from_ipython and not need_latex():
        if 'fig:' not in label and 'tab:' not in label:
            number = bi.__labels__

def cref(label):
    if run_from_ipython and not need_latex():
        if label in bi.__tables__.keys():
            number = bi.__tables__[label]
            text = 'table'
        elif label in bi.__figures__.keys():
            number = bi.__figures__[label]
            text = 'figure'
        else:
            text = 'ref'
            number = 0
        html_str = '<a href="#%s">%s %d</a>' % (label, text, number)
        if need_markdown():
            return html_str
        else:
            return display(HTML(html_str))
    elif run_from_ipython and need_latex():
        return display(Latex('\[fig:%s\]' % label))
