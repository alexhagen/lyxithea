import lyxithea as lyx
from IPython.display import display, Latex, HTML
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
import numpy as np
from mwe import mwe

ip = get_ipython()

ip = get_ipython()

def cslides():
    if bi.__cslides__ is not None:
        return bi.__cslides__
    else:
        return puslides()


class puslides(lyxdoc.document):
    """ A purdue slides class """
    slidetypes = {'onecolumnslide': {'size': [(7.5, 5.25)], 'number': 1},
                  'twocolumnslide': {'size': [(3.375, 5.25), (3.375, 5.25)],
                                     'number': 2},
                  'twocolumnshiftleft': {'size': [(2.25, 5.25), (4.5, 5.25)], 'number': 2},
                  'twocolumnshiftright': {'size': [(4.5, 5.25), (2.25, 5.25)], 'number': 2},
                  'tworow': {'size': [(7.5, 2.375), (7.5, 2.375)], 'number': 2},
                  'tworowpushdown': {'size': [(7.5, 3.75), (7.5, 1.125)], 'number': 2},
                  'tworowpushup': {'size': [(7.5, 1.125), (7.4, 4.25)], 'number': 2},
                  'tworowtoptwocolumn': {'size': [(3.375, 2.375), (3.375, 2.375), (7.5, 2.375)], 'number': 3},
                  'tworowbottomtwocolumn': {'size': [(3.375, 2.375), (3.375, 2.375), (7.5, 2.375)], 'number': 3},
                  'tworowleftsidebar': {'size': [(4.5, 2.375), (4.5, 2.375), (2.25, 5.125)], 'number': 3},
                  'tworowrightsidebar': {'size': [(4.5, 2.375), (4.5, 2.375), (2.25, 5.125)], 'number': 3},
                  'tworowtwocolumn': {'size': [(3.375, 2.375), (3.375, 2.375), (3.375, 2.375), (3.375, 2.375)], 'number': 4}
                 }
    def __init__(self, bib=None):
        self.modulepath = osp.dirname(__file__)
        self.content_one = None
        self.content_two = None
        self.content = [None, None, None, None, None, None, None]
        self.slide = 1
        self._title = None
        self._affiliation = None
        self._author = None
        self._venue = None
        self._subtitle = None
        self._city = None
        self._slidetype = None
        super(puslides, self).__init__(bib=bib)
        bi.__cslides__ = self

    def export(self, filename, engine='lualatex'):
        # copy the classfile over
        shutil.copy(osp.join(self.modulepath, 'puslides.cls'), './')
        # copy the css files over
        shutil.rmtree('fonts/', ignore_errors=True)
        shutil.rmtree('css/', ignore_errors=True)
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
        self.finish_title()

    def author(self, author):
        self._author = author
        self.finish_title()

    def affiliation(self, affiliation):
        self._affiliation = affiliation
        self.finish_title()

    def subtitle(self, subtitle):
        self._subtitle = subtitle
        self.finish_title()

    def venue(self, venue):
        self._venue = venue
        self.finish_title()

    def city(self, city):
        self._city = city
        self.finish_title()

    def part(self, title):
        self.current_part = title
        latex_str = r'\part{%s}' % title
        return display(Latex(latex_str))

    def chapter(self, title):
        self.current_chapter = title
        latex_str = r'\def\nameofchapter{%s}' % title
        return display(Latex(latex_str))

    def chapterslidetitle(self, content, **kwargs):
        self.slide_title = content
        self.process_content(content, 0, **kwargs)
        self.finish_slide('chapterslide', 2)

    def chapterslidesubtitle(self, content, **kwargs):
        self.process_content(content, 1, **kwargs)
        self.finish_slide('chapterslide', 2)


    def bibliography(self):
        return super(puslides, self).bibliography(header_level=3, force_string=True)

    def process_content(self, content, index, filename=None, latex=False,
                        **kwargs):
        if latex:
            self.content[index] = content
            return content
        if isinstance(content, str):
            self.content[index] = \
                pypandoc.convert_text(self.process_markdown(content), 'latex',
                                      format='md')
            latex_str = self.content[index]
            return latex_str
        elif isinstance(content, pyg2d.pyg2d):
            lyx.latex()
            content.export(filename, force=True, sizes=['cs'],
                           customsize=(self.width, self.height - 0.125))
            string = content.show(need_string=True, **kwargs)
            self.content[index] = string
            return string
        elif isinstance(content, pyg2d.svg):
            lyx.latex()
            string = content.show(width=self.width, need_string=True,
                                  bbox=(self.width, self.height - 0.125),
                                  **kwargs)
            self.content[index] = string
            return string

    def clear_slide(self):
        self.slide_title = None
        self.content = [None for x in self.content]

    ### generic

    def slidetype(self, slidetype='onecolumnslide'):
        self._slidetype = slidetype
        self._contentno = 0

    def slidetitle(self, content):
        self.slide_title = content
        self.finish_slide(self._slidetype, 1)

    def t(self, content):
        self.slidetitle(content)

    def slidecontent(self, content, **kwargs):
        w, h = self.slidetypes[self._slidetype]['size'][self._contentno]
        self.size(w, h)
        self.process_content(content, self._contentno, **kwargs)
        self.finish_slide(self._slidetype, self.slidetypes[self._slidetype]['number'])
        self._contentno += 1

    def c(self, content, **kwargs):
        self.slidecontent(content, **kwargs)

    ### All Slide Types

    def listslidetypes(self):
        print self.slidetypes.keys()

    def onecolumnslide(self):
        self.slidetype('onecolumnslide')

    def twocolumnslide(self):
        self.slidetype('twocolumnslide')

    def twocolumnshiftleft(self):
        self.slidetype('twocolumnshiftleft')

    def twocolumnshiftright(self):
        self.slidetype('twocolumnshiftright')

    def tworow(self):
        self.slidetype('tworow')

    def tworowpushdown(self):
        self.slidetype('tworowpushdown')

    def tworowpushup(self):
        self.slidetype('tworowpushup')

    def tworowtoptwocolumn(self):
        self.slidetype('tworowtoptwocolumn')

    def tworowbottomtwocolumn(self):
        self.slidetype('tworowbottomtwocolumn')

    def tworowleftsidebar(self):
        self.slidetype('tworowleftsidebar')

    def tworowrightsidebar(self):
        self.slidetype('tworowrightsidebar')

    def tworowtwocolumn(self):
        self.slidetype('tworowtwocolumn')

    ### One Content Slides

    def onecolumn(self):
        self.slidetype('onecolumnslide')

    def onecolumntitle(self, content):
        self.slide_title = content
        self.finish_slide('onecolumnslide', 1)

    def onecolumn1(self, content, **kwargs):
        self.size(7.5, 5.25)
        self.process_content(content, 0, **kwargs)
        self.finish_slide('onecolumnslide', 1)

    ### Two content slides

    def twocolumn(self):
        self.slidetype('twocolumnslide')

    def twocolumntitle(self, content):
        self.slide_title = content
        self.finish_slide('twocolumnslide', 2)

    def twocolumn1(self, content, **kwargs):
        self.size(3.375, 5.25)
        self.process_content(content, 0, **kwargs)
        self.finish_slide('twocolumnslide', 2)

    def twocolumn2(self, content, **kwargs):
        self.size(3.375, 5.25)
        self.process_content(content, 1, **kwargs)
        self.finish_slide('twocolumnslide', 2)

    def twocolumnshiftleft(self):
        self.slidetype('twocolumnshiftleft')

    def twocolumnshiftlefttitle(self, content):
        self.slide_title = content
        self.finish_slide('twocolumnshiftleft', 2)

    def twocolumnshiftleft1(self, content, **kwargs):
        self.size(2.25, 5.25)
        self.process_content(content, 0, **kwargs)
        self.finish_slide('twocolumnshiftleft', 2)

    def twocolumnshiftleft2(self, content, **kwargs):
        self.size(4.5, 5.25)
        self.process_content(content, 1, **kwargs)
        self.finish_slide('twocolumnshiftleft', 2)

    def twocolumnshiftright(self):
        self.slidetype('twocolumnshiftright')

    def twocolumnshiftrighttitle(self, content):
        self.slide_title = content
        self.finish_slide('twocolumnshiftright', 2)

    def twocolumnshiftright1(self, content, **kwargs):
        self.size(4.5, 5.25)
        self.process_content(content, 0, **kwargs)
        self.finish_slide('twocolumnshiftright', 2)

    def twocolumnshiftright2(self, content, **kwargs):
        self.size(2.25, 5.25)
        self.process_content(content, 1, **kwargs)
        self.finish_slide('twocolumnshiftright', 2)

    def tworowtitle(self, content):
        self.slide_title = content
        self.finish_slide('tworow', 2)

    def tworow1(self, content, **kwargs):
        self.size(7.5, 2.375)
        self.process_content(content, 0, **kwargs)
        self.finish_slide('tworow', 2)

    def tworow2(self, content, **kwargs):
        self.size(7.5, 2.375)
        self.process_content(content, 1, **kwargs)
        self.finish_slide('tworow', 2)

    def tworowpushdowntitle(self, content):
        self.slide_title = content
        self.finish_slide('tworowpushdown', 2)

    def tworowpushdown1(self, content, **kwargs):
        self.size(7.5, 3.75)
        self.process_content(content, 0, **kwargs)
        self.finish_slide('tworowpushdown', 2)

    def tworowpushdown2(self, content, **kwargs):
        self.size(7.5, 1.125)
        self.process_content(content, 1, **kwargs)
        self.finish_slide('tworowpushdown', 2)

    def tworowpushuptitle(self, content):
        self.slide_title = content
        self.finish_slide('tworowpushdown', 2)

    def tworowpushup1(self, content, **kwargs):
        self.size(7.5, 1.125)
        self.process_content(content, 0, **kwargs)
        self.finish_slide('tworowpushup', 2)

    def tworowpushup2(self, content, **kwargs):
        self.size(7.5, 4.25)
        self.process_content(content, 1, **kwargs)
        self.finish_slide('tworowpushup', 2)

    def tworowtoptwocolumntitle(self, content):
        self.slide_title = content
        self.finish_slide('tworowtoptwocolumn', 3)

    def tworowtoptwocolumn1(self, content, **kwargs):
        self.size(3.375, 2.375)
        self.process_content(content, 0, **kwargs)
        self.finish_slide('tworowtoptwocolumn', 3)

    def tworowtoptwocolumn2(self, content, **kwargs):
        self.size(3.375, 2.375)
        self.process_content(content, 1, **kwargs)
        self.finish_slide('tworowtoptwocolumn', 3)

    def tworowtoptwocolumn3(self, content, **kwargs):
        self.size(7.5, 2.375)
        self.process_content(content, 2, **kwargs)
        self.finish_slide('tworowtoptwocolumn', 3)

    def tworowbottomtwocolumntitle(self, content):
        self.slide_title = content
        self.finish_slide('tworowbottomtwocolumn', 3)

    def tworowbottomtwocolumn1(self, content, **kwargs):
        self.size(3.375, 2.375)
        self.process_content(content, 0, **kwargs)
        self.finish_slide('tworowbottomtwocolumn', 3)

    def tworowbottomtwocolumn2(self, content, **kwargs):
        self.size(3.375, 2.375)
        self.process_content(content, 1, **kwargs)
        self.finish_slide('tworowbottomtwocolumn', 3)

    def tworowbottomtwocolumn3(self, content, **kwargs):
        self.size(7.5, 2.375)
        self.process_content(content, 2, **kwargs)
        self.finish_slide('tworowbottomtwocolumn', 3)

    def tworowleftsidebartitle(self, content, **kwargs):
        self.slide_title = content
        self.finish_slide('tworowleftsidebar', 3)

    def tworowleftsidebar1(self, content, **kwargs):
        self.size(4.5, 2.375)
        self.process_content(content, 0, **kwargs)
        self.finish_slide('tworowleftsidebar', 3)

    def tworowleftsidebar2(self, content, **kwargs):
        self.size(4.5, 2.375)
        self.process_content(content, 1, **kwargs)
        self.finish_slide('tworowleftsidebar', 3)

    def tworowleftsidebar3(self, content, **kwargs):
        self.size(2.25, 5.125)
        self.process_content(content, 2, **kwargs)
        self.finish_slide('tworowleftsidebar', 3)

    def tworowrightsidebartitle(self, content, **kwargs):
        self.slide_title = content
        self.finish_slide('tworowrightsidebar', 3)

    def tworowrightsidebar1(self, content, **kwargs):
        self.size(4.5, 2.375)
        self.process_content(content, 0, **kwargs)
        self.finish_slide('tworowrightsidebar', 3)

    def tworowrightsidebar2(self, content, **kwargs):
        self.size(4.5, 2.375)
        self.process_content(content, 1, **kwargs)
        self.finish_slide('tworowrightsidebar', 3)

    def tworowrightsidebar3(self, content, **kwargs):
        self.size(2.25, 5.125)
        self.process_content(content, 2, **kwargs)
        self.finish_slide('tworowrightsidebar', 3)

    ### Four arguments
    def tworowtwocolumn(self):
        self.slidetype('tworowtwocolumn')

    def tworowtwocolumntitle(self, content, **kwargs):
        self.slide_title = content
        self.finish_slide('tworowtwocolumn', 4)

    def tworowtwocolumn1(self, content, **kwargs):
        self.size(3.375, 2.375)
        self.process_content(content, 0, **kwargs)
        self.finish_slide('tworowtwocolumn', 4)

    def tworowtwocolumn2(self, content, **kwargs):
        self.size(3.375, 2.375)
        self.process_content(content, 1, **kwargs)
        self.finish_slide('tworowtwocolumn', 4)

    def tworowtwocolumn3(self, content, **kwargs):
        self.size(3.375, 2.375)
        self.process_content(content, 2, **kwargs)
        self.finish_slide('tworowtwocolumn', 4)

    def tworowtwocolumn4(self, content, **kwargs):
        self.size(3.375, 2.375)
        self.process_content(content, 3, **kwargs)
        self.finish_slide('tworowtwocolumn', 4)

    ### Generic things

    def size(self, width, height):
        self.width = width
        self.height = height

    def pocket_on(self):
        display(Latex(r'\savepocketslide{'))
        prelatex_str = '\def\\nameofchapter{%s}\n' % self.current_chapter
        display(Latex(prelatex_str))

    def pocket_off(self):
        display(Latex(r'}'))

    def pocket_slides(self):
        display(Latex('\\pocketslides\n'))

    def finish_title(self):
        # check if all the title slide stuff is done
        if self._title is not None and self._subtitle is not None and \
            self._author is not None and self._venue is not None and \
            self._affiliation is not None and self._city is not None:
            self.clear_slide()
            if not lyx.is_exporting():
                preamble_str = '\def\\theauthorsforbottom{%s}\n' % self._author
                preamble_str += '\\providecommand{\\tightlist}{\\renewcommand{\\\\}{\\vspace{0pt}}}\n'
                # copy the classfile over
                shutil.copy(osp.join(self.modulepath, 'puslides.cls'), './')
                prelatex_str = '\\title{%s}\n' % self._title
                prelatex_str += '\subtitle{%s}\n' % self._subtitle
                prelatex_str += '\\author{%s}\n' % self._author
                prelatex_str += '\\venue{%s}\n' % self._venue
                prelatex_str += '\\city{%s}\n' % self._city
                prelatex_str += '\\maketitle\n'
                # copy the css files over
                shutil.rmtree('fonts/', ignore_errors=True)
                shutil.rmtree('css/', ignore_errors=True)
                shutil.copytree(osp.join(self.modulepath, 'css/'), 'css/')
                # copy the fonts over
                shutil.copytree(osp.join(self.modulepath, 'fonts/'), 'fonts/')
                thisslide = mwe.mwe(prelatex_str, texcls='puslides',
                                    texclsopts={'english': None, '20pt': None},
                                    preamble=preamble_str)
                try:
                    thisslide.show(alone=True, filename='slide_%d' % self.slide,
                                   engine='lualatex')
                except IOError:
                    display(HTML('<h2>Latex Error</h2>'))
                self.slide += 1
                shutil.rmtree('fonts/')
                shutil.rmtree('css/')


    def finish_slide(self, latexname, numargs):
        bools = [_content is not None for _content in self.content[:numargs]]
        if np.all(bools) and self.slide_title is not None:
            latex_str = '\\' + latexname
            for i in range(0, numargs):
                latex_str += r'{\begin{content} %s \end{content}}' % \
                    self.content[i]
            latex_str += r'{%s}' % self.slide_title
            if lyx.is_exporting():
                display(Latex(latex_str))
            self.clear_slide()
            if not lyx.is_exporting():
                preamble_str = '\def\\theauthorsforbottom{%s}\n' % self._author
                preamble_str += '\\providecommand{\\tightlist}{\\renewcommand{\\\\}{\\vspace{0pt}}}\n'
                # copy the classfile over
                shutil.copy(osp.join(self.modulepath, 'puslides.cls'), './')
                prelatex_str = '\\title{%s}\n' % self._title
                prelatex_str += '\subtitle{%s}\n' % self._subtitle
                prelatex_str += '\\author{%s}\n' % self._author
                prelatex_str += '\\venue{%s}\n' % self._venue
                prelatex_str += '\\city{%s}\n' % self._city
                prelatex_str += '\\part{%s}\n' % self.current_part
                prelatex_str += '\def\\nameofchapter{%s}\n' % self.current_chapter
                # copy the css files over
                shutil.rmtree('fonts/', ignore_errors=True)
                shutil.rmtree('css/', ignore_errors=True)
                shutil.copytree(osp.join(self.modulepath, 'css/'), 'css/')
                # copy the fonts over
                shutil.copytree(osp.join(self.modulepath, 'fonts/'), 'fonts/')
                thisslide = mwe.mwe(prelatex_str + latex_str, texcls='puslides',
                                    texclsopts={'english': None, '20pt': None},
                                    preamble=preamble_str)
                try:
                    thisslide.show(alone=True, filename='slide_%d' % self.slide,
                                   engine='lualatex')
                except IOError:
                    display(HTML('<h2>Latex Error</h2>'))
                self.slide += 1
                shutil.rmtree('fonts/')
                shutil.rmtree('css/')

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
