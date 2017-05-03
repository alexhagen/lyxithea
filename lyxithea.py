from tabulate import tabulate
from IPython.display import SVG, display, Latex, HTML, display_latex
import sys
import os
import os.path
import subprocess
import bibtexparser
from bibtexparser.bibdatabase import BibDatabase

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
        return False

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
        display(HTML(fig_html))
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
        self.add_bib(os.path.expanduser('~/') + filename)

    def add_bib(self, filename):
        self.bib_fname = filename
        if run_from_ipython() and not need_latex():
            with open(self.bib_fname, 'r') as bib_file:
                self.bib_db = bibtexparser.load(bib_file)
                for entry in self.bib_db.entries:
                    self.bib_dict[entry['ID']] = entry

    def pcite(self, label):
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
            return display(HTML(pcitestr))

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
                with open('temp.bib', 'w') as f:
                    f.write(bibtex_str)
                system_str = 'bibtex2html -nokeys -o - -s plain -nodoc -q temp.bib'
                args = shlex.split(system_str)
                proc = Popen(args, stdout=PIPE, stderr=PIPE)
                out, err = proc.communicate()
                exitcode = proc.returncode
                result = out.replace("""<!-- This document was automatically generated with bibtex2html 1.98
     (see http://www.lri.fr/~filliatr/bibtex2html/),
     with the following command:
     bibtex2html -nokeys -o - -s plain -nodoc -q temp.bib  -->




""", '').replace("""<hr><p><em>This file was generated by
<a href="http://www.lri.fr/~filliatr/bibtex2html/">bibtex2html</a> 1.98.</em></p>""", '')
                #print out, err, exitcode
                htmlstr += '<li name="{name}">{citation}</li>\n'.format(name=label, citation=result)
            htmlstr += '</ol>\n'

            return display(HTML(htmlstr))


def figures():
    print bi.__tables__
    print bi.__figures__

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
        return display(HTML(html_str))
    elif run_from_ipython and need_latex():
        return display(Latex('\[fig:%s\]' % label))
