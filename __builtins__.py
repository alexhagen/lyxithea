__nom__ = {'abbr': {}, 'symb': {}, 'unit': {}, 'supsub': {}, 'defs': {}}
__todos__ = []
from IPython.display import Markdown
__formatter__ = Markdown
__need_latex__ = True

__cdis__ = None
__cdoc__ = None
__cslides__ = None
__regex__ = r"{% ([\s\w\d\(\)\[\]=\+\^\'\"\{\}\.\%\*\\\-\,\;\:\$]*?) %}"
__regex2__ = r"\(\(\. ([\s\w\d\(\)\[\]=\+\^\'\"\{\}\.\%\*\\\-\,\;\:\$]*?) \.\)\)"

__latex_template__ = r"""
((*- extends 'article.tplx' -*))

((* block input_group *))
    ((*- if cell.metadata.get('nbconvert', {}).get('show_code', False) -*))
        ((( super() )))
    ((*- endif -*))
((* endblock input_group *))

((* block data_latex -*))
    ((( output.data['text/latex'] | strip_files_prefix )))
((* endblock data_latex *))

((* set cell_style = 'style_bw_python.tplx' *))

((* block packages *))
  \usepackage[T1]{fontenc}
  % Nicer default font (+ math font) than Computer Modern for most use cases
  \usepackage{mathpazo}
  \usepackage{graphicx}
  \usepackage{adjustbox} % Used to constrain images to a maximum size
  \usepackage{xcolor} % Allow colors to be defined
  \usepackage{enumerate} % Needed for markdown enumerations to work
  \usepackage{geometry} % Used to adjust the document margins
  \usepackage{amsmath} % Equations
  \usepackage{amssymb} % Equations
  \usepackage{textcomp} % defines textquotesingle
  \AtBeginDocument{%
      \def\PYZsq{\textquotesingle}% Upright quotes in Pygmentized code
  }
  \usepackage{upquote} % Upright quotes for verbatim code
  \usepackage{eurosym} % defines \euro
  \usepackage[mathletters]{ucs} % Extended unicode (utf-8) support
  \usepackage[utf8x]{inputenc} % Allow utf-8 characters in the tex document
  \usepackage{fancyvrb} % verbatim replacement that allows latex
  \usepackage{grffile} % extends the file name processing of package graphics
                       % to support a larger range
  % The hyperref package gives us a pdf with properly built
  % internal navigation ('pdf bookmarks' for the table of contents,
  % internal cross-reference links, web links for URLs, etc.)
  \usepackage{hyperref}
  \usepackage{longtable} % longtable support required by pandoc >1.10
  \usepackage{booktabs}  % table support for pandoc > 1.12.2
  \usepackage[inline]{enumitem} % IRkernel/repr support (it uses the enumerate* environment)
  \usepackage[normalem]{ulem} % ulem is needed to support strikethroughs (\sout)
                              % normalem makes italics be italics, not underlines
  \usepackage{tikz}
  \usepackage{nicefrac}
  \usepackage{gensymb}
  \usepackage{cleveref}
  %\usepackage{nomencl}
  %\makenomenclature
  \usepackage{import}
  \usepackage[english]{babel}
  \newcommand{\unit}[1]{\mathrm{#1}}
  \newcommand{\ce}[1]{\mathrm{#1}}
  \newcommand{\cc}{\unit{cm^{3}}}
  \newcommand{\invis}[1]{}
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
((* endblock maketitle *))
"""

__article_template__ = r"""
((*- extends 'article.tplx' -*))

((* block docclass *))
\documentclass[english]{article}
((* endblock docclass *))

((* block input_group *))
    ((*- if cell.metadata.get('nbconvert', {}).get('show_code', False) -*))
        ((( super() )))
    ((*- endif -*))
((* endblock input_group *))

((* block data_latex -*))
    ((( output.data['text/latex'] | strip_files_prefix )))
((* endblock data_latex *))

((* set cell_style = 'style_bw_python.tplx' *))

((* block packages *))
  \usepackage[T1]{fontenc}
  % Nicer default font (+ math font) than Computer Modern for most use cases
  \usepackage{graphicx}
  \usepackage{rotfloat}
  \usepackage{adjustbox} % Used to constrain images to a maximum size
  \usepackage{xcolor} % Allow colors to be defined
  \usepackage{enumerate} % Needed for markdown enumerations to work
  \usepackage{geometry} % Used to adjust the document margins
  \usepackage{amsmath} % Equations
  \usepackage{amssymb} % Equations
  \usepackage{textcomp} % defines textquotesingle
  \AtBeginDocument{%
      \def\PYZsq{\textquotesingle}% Upright quotes in Pygmentized code
  }
  \usepackage{upquote} % Upright quotes for verbatim code
  \usepackage{eurosym} % defines \euro
  \usepackage[mathletters]{ucs} % Extended unicode (utf-8) support
  \usepackage[utf8x]{inputenc} % Allow utf-8 characters in the tex document
  \usepackage{fancyvrb} % verbatim replacement that allows latex
  \usepackage{grffile} % extends the file name processing of package graphics
                       % to support a larger range
  % The hyperref package gives us a pdf with properly built
  % internal navigation ('pdf bookmarks' for the table of contents,
  % internal cross-reference links, web links for URLs, etc.)
  \usepackage{hyperref}
  \usepackage{longtable} % longtable support required by pandoc >1.10
  \usepackage{booktabs}  % table support for pandoc > 1.12.2
  \usepackage[inline]{enumitem} % IRkernel/repr support (it uses the enumerate* environment)
  \usepackage[normalem]{ulem} % ulem is needed to support strikethroughs (\sout)
                              % normalem makes italics be italics, not underlines
  \usepackage{tikz}
  \usepackage{nicefrac}
  \usepackage{gensymb}
  \usepackage{cleveref}
  %\usepackage{nomencl}
  %\makenomenclature
  \usepackage{import}
  \usepackage[english]{babel}
  \newcommand{\unit}[1]{\mathrm{#1}}
  \newcommand{\ce}[1]{\mathrm{#1}}
  \newcommand{\cc}{\unit{cm^{3}}}
  \newcommand{\invis}[1]{}
  \makeatletter
  \def\appendicestext{}
  \newcommand\saveappendix[1]{\g@addto@macro\appendicestext{#1}}
  \makeatother
((* endblock packages *))

% Author and Title from metadata
((* block maketitle *))

((*- if nb.metadata: -*))
((*- if nb.metadata["author"]: -*))
    \author{((( nb.metadata["author"] )))}
((*- endif *))
((*- else -*))
    \author{Alex Hagen}
((*- endif *))

((*- if nb.metadata["latex_metadata"]: -*))
((*- if nb.metadata["latex_metadata"]["affiliation"]: -*))
    \affiliation{((( nb.metadata["latex_metadata"]["affiliation"] )))}
((*- endif *))
((*- endif *))

((*- if nb.metadata: -*))
((*- if nb.metadata["title"]: -*))
    \title{((( nb.metadata["title"] )))}
((*- endif *))
((*- else -*))
    \title{((( resources.metadata.name )))}
((*- endif *))

\date{\today}
\maketitle
((* endblock maketitle *))
"""

__article2_template__ = r"""
((*- extends 'article.tplx' -*))

((* block docclass *))
\documentclass[english, twocolumn]{article}
((* endblock docclass *))

((* block input_group *))
    ((*- if cell.metadata.get('nbconvert', {}).get('show_code', False) -*))
        ((( super() )))
    ((*- endif -*))
((* endblock input_group *))

((* block data_latex -*))
    ((( output.data['text/latex'] | strip_files_prefix )))
((* endblock data_latex *))

((* set cell_style = 'style_bw_python.tplx' *))

((* block packages *))
  \usepackage[T1]{fontenc}
  % Nicer default font (+ math font) than Computer Modern for most use cases
  \usepackage{mathpazo}
  \usepackage{graphicx}
  \usepackage{rotfloat}
  \usepackage{adjustbox} % Used to constrain images to a maximum size
  \usepackage{xcolor} % Allow colors to be defined
  \usepackage{enumerate} % Needed for markdown enumerations to work
  \usepackage{geometry} % Used to adjust the document margins
  \usepackage{amsmath} % Equations
  \usepackage{amssymb} % Equations
  \usepackage{textcomp} % defines textquotesingle
  \usepackage{array}
  \usepackage[utopia]{mathdesign}
  \usepackage[OMLmathrm,OMLmathbf]{isomath}
  \usepackage{subfig}
  \AtBeginDocument{%
      \def\PYZsq{\textquotesingle}% Upright quotes in Pygmentized code
  }
  \usepackage{upquote} % Upright quotes for verbatim code
  \usepackage{eurosym} % defines \euro
  \usepackage[mathletters]{ucs} % Extended unicode (utf-8) support
  \usepackage[utf8x]{inputenc} % Allow utf-8 characters in the tex document
  \usepackage{fancyvrb} % verbatim replacement that allows latex
  \usepackage{grffile} % extends the file name processing of package graphics
                       % to support a larger range
  % The hyperref package gives us a pdf with properly built
  % internal navigation ('pdf bookmarks' for the table of contents,
  % internal cross-reference links, web links for URLs, etc.)
  \usepackage{hyperref}
  \usepackage{longtable} % longtable support required by pandoc >1.10
  \usepackage{booktabs}  % table support for pandoc > 1.12.2
  \usepackage[inline]{enumitem} % IRkernel/repr support (it uses the enumerate* environment)
  \usepackage[normalem]{ulem} % ulem is needed to support strikethroughs (\sout)
                              % normalem makes italics be italics, not underlines
  \usepackage{tikz}
  \usepackage{nicefrac}
  \usepackage{gensymb}
  \usepackage{cleveref}
  %\usepackage{nomencl}
  %\makenomenclature
  \usepackage{import}
  \usepackage[english]{babel}
  \newcommand{\unit}[1]{\mathrm{#1}}
  \newcommand{\ce}[1]{\mathrm{#1}}
  \newcommand{\cc}{\unit{cm^{3}}}
  \newcommand{\invis}[1]{}
  \makeatletter
  \def\appendicestext{}
  \newcommand\saveappendix[1]{\g@addto@macro\appendicestext{#1}}
  \makeatother
  \usepackage{outlines}

  \renewcommand{\theenumi}{\Roman{enumi}. }
  \renewcommand{\labelenumi}{\theenumi}

  \renewcommand{\theenumii}{\Alph{enumii}. }
  \renewcommand{\labelenumii}{\theenumii}

  \renewcommand{\theenumiii}{\roman{enumiii}. }
  \renewcommand{\labelenumiii}{\theenumiii}

  \renewcommand{\theenumiv}{\alph{enumiv}) }
  \renewcommand{\labelenumiv}{\theenumiv}
  \usepackage{todonotes}
  \usepackage{authblk}
  \renewcommand\Affilfont{\itshape\small}
  %\renewcommand\Authsep{ \and }
  %\renewcommand\Authand{ \and }
  %\renewcommand\Authands{ \and }
((* endblock packages *))

% Author and Title from metadata
((* block maketitle *))

((*- if nb.metadata: -*))
((*- if nb.metadata["author"]: -*))
    ((( nb.metadata["author"] )))
((*- if nb.metadata["affiliation"]: -*))
    ((( nb.metadata["affiliation"] )))
((*- endif *))
((*- endif *))
((*- else -*))
    \author{Alex Hagen}
((*- endif *))

((*- if nb.metadata: -*))
((*- if nb.metadata["title"]: -*))
    \title{((( nb.metadata["title"] )))}
((*- endif *))
((*- else -*))
    \title{((( resources.metadata.name )))}
((*- endif *))

\date{\today}
\maketitle
((* endblock maketitle *))
"""

__dissertation_template__ = r"""
((*- extends 'report.tplx' -*))

((* block input_group *))
    ((*- if cell.metadata.get('nbconvert', {}).get('show_code', False) -*))
        ((( super() )))
    ((*- endif -*))
((* endblock input_group *))

((* block data_latex -*))
    ((( output.data['text/latex'] | strip_files_prefix )))
((* endblock data_latex *))

((* set cell_style = 'style_bw_python.tplx' *))

((* block docclass *))
\documentclass[english, ne, dissertation]{puthesis}
((* endblock docclass *))

((* block margins *))
((* endblock margins *))
((* block packages *))
    \usepackage[T1]{fontenc}
    \usepackage[latin9]{inputenc}
    \setcounter{secnumdepth}{3}
    \setcounter{tocdepth}{1}
    \usepackage[english]{babel}
    \usepackage{array}
    \usepackage{varioref}
    \usepackage{refstyle}
    \usepackage{rotfloat}
    \usepackage{units}
    \usepackage{multirow}
    \usepackage{amsmath}
    \usepackage{graphicx}
    \usepackage{fancyvrb} % verbatim replacement that allows latex
    \PassOptionsToPackage{version=3}{mhchem}
    \usepackage{mhchem}
    \usepackage[numbers]{natbib}
    \usepackage{nomencl}
    \usepackage[disable]{todonotes}
    %\usepackage{fixmetodonotes}
    % the following is useful when we have the old nomencl.sty package
    \providecommand{\printnomenclature}{\printglossary}
    \providecommand{\makenomenclature}{\makeglossary}
    \def\@@@nomenclature[#1]#2#3{%
        \def\@tempa{#2}\def\@tempb{#3}%
        \protected@write\@nomenclaturefile{}%
        {\string\nomenclatureentry{#1\nom@verb\@tempa @{\nom@verb\@tempa}&%
        \begingroup\nom@verb\@tempb\protect\nomeqref{\theequation}%
        |nompageref}{\thepage}}%
        \endgroup
        \@esphack}
    \makenomenclature
    %\usepackage{glossaries}
    %\makeglossaries
    \usepackage[unicode=true,pdfusetitle,
     bookmarks=true,bookmarksnumbered=false,bookmarksopen=false,
     breaklinks=false,pdfborder={0 0 0},pdfborderstyle={},backref=page,colorlinks=false]
     {hyperref}
    \usepackage{breakurl}
    \usepackage{threeparttable}
    \usepackage{pdfpages}
    \usepackage{soul}
    \setul{0.5ex}{0.3ex}

    \makeatletter

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%% LyX specific LaTeX commands.

    \AtBeginDocument{\providecommand\figref[1]{\ref{fig:#1}}}
    \AtBeginDocument{\providecommand\chapref[1]{\ref{chap:#1}}}
    \AtBeginDocument{\providecommand\secref[1]{\ref{sec:#1}}}
    \AtBeginDocument{\providecommand\subsecref[1]{\ref{subsec:#1}}}
    \newcommand{\noun}[1]{\textsc{#1}}
    %% Because html converters don't know tabularnewline
    \providecommand{\tabularnewline}{\\}
    \RS@ifundefined{subsecref}
      {\newref{subsec}{name = \RSsectxt}}
      {}
    \RS@ifundefined{thmref}
      {\def\RSthmtxt{theorem~}\newref{thm}{name = \RSthmtxt}}
      {}
    \RS@ifundefined{lemref}
      {\def\RSlemtxt{lemma~}\newref{lem}{name = \RSlemtxt}}
      {}


    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%% User specified LaTeX commands.
    \campus{West Lafayette}

    % Automatically number all display equations
    \renewcommand\[{\begin{equation}}
    \renewcommand\]{\end{equation}}

    % For flower symbol
    \usepackage{bbding}
    \usepackage{graphicx}
    \usepackage{color}
    \usepackage{import}
    \usepackage{mhchem}
    \usepackage{algorithm}
    \usepackage{algorithmic}
    \usepackage{algolyx}
    \usepackage{listings}
    \usepackage{adjustbox}
    \usepackage{rotfloat}
    \usepackage{pdfpages}
    %\usepackage{pdfx}
    \makeatletter
    \newcommand{\invis}[1]{%
      \@bsphack
      \@esphack
    }
    \makeatother

    % HYPERREF AND APPENDICES?
    % OVERWRITES appendix command?
    %\usepackage{appendix}

    % TODO: Check if this is allowed
    \usepackage{setspace}
    %\singlespacing
    \onehalfspacing % my prefered.
    %\doublespacing
    %\setstretch{1.1}

    % Be bold when it comes to quotes...
    \makeatletter
    \renewenvironment{verse} % from quote env.
                   {\list{}
    {\rightmargin\leftmargin}%
                    \item\setlength{\itemsep}{0pt}%\relax
      \setlength{\topsep}{0pt}
      \setlength{\parskip}{0pt}
      \setlength{\parsep}{0pt}}
                   {\endlist}
    \makeatother
    %\renewenvironment{verse}
      %             {\let\\\@centercr
        %            \list{}{\itemsep      \z@
          %                  \itemindent   -1.5em%
    %                        \listparindent\itemindent
    %                        \rightmargin  \leftmargin
    %                        \advance\leftmargin 1.5em}%
    %                \item\relax}
    %               {\endlist}
    %\makeatother

    % all-caps chapters in TOC
    \makeatletter \def\@chapter[#1]#2{%
    \ifnum \c@secnumdepth >\m@ne \refstepcounter{chapter}%
     \typeout{\@chapapp\space\thechapter.}%
     \addcontentsline{toc}{chapter}{\protect\numberline{\thechapter}\uppercase{#1}} \fi \chaptermark{#1}%
     \@makechapterhead{#2} \@afterheading \ifthen{\not \boolean{@@inchapters}} { \pagenumbering{arabic}%
     \@@inchapterstrue } }
  \floatstyle{ruled}
    \newfloat{alg}{tbp}{lop}[chapter]
    \floatname{alg}{Algorithm}

    \definecolor{405C}{RGB}{116,108,102}

    %Add header for confidentiality
    \def\@@evenhead{\hfil\textrm{DRAFT - BUSINESS CONFIDENTIAL - NOT FOR DISSEMINATION}\hfil\textrm{\thepage}}
    \def\@@oddhead{\hfil\textrm{DRAFT - BUSINESS CONFIDENTIAL - NOT FOR DISSEMINATION}\hfil\textrm{\thepage}}

    %Make list of symbols, etc.
    \renewcommand{\nomname}{}
    \RequirePackage{ifthen}
    \newcommand{\abbrtitle}{\item[] \centering{ABBREVIATIONS} %
    \item[] \raggedright \addcontentsline{toc}{chapter}{ABBREVIATIONS}}
    \newcommand{\symtitle}{\clearpage \item[] \parbox[b][0.5 in][t]{\textwidth}{\hfill} \item[] \centering SYMBOLS%
    \item[] \raggedright \addcontentsline{toc}{chapter}{SYMBOLS}}
    \newcommand{\substitle}{\clearpage \item[] \parbox[b][0.5 in][t]{\textwidth}{\hfill} \item[] \centering SUBSCRIPTS AND SUPERSCRIPTS%
    \item[] \raggedright \addcontentsline{toc}{chapter}{SUBSCRIPTS AND SUPERSCRIPTS}}
    \newcommand{\unitstitle}{\item[] \centering{UNITS} %
    \item[] \raggedright \addcontentsline{toc}{chapter}{UNITS}}
    \newcommand{\defstitle}{\item[] \centering{DEFINITIONS} %
    \item[] \raggedright \addcontentsline{toc}{chapter}{DEFINITIONS}}

    \renewcommand{\nomgroup}[1]{%
    \ifthenelse{\equal{#1}{A}}{\abbrtitle}{%
    \ifthenelse{\equal{#1}{Y}}{\symtitle}{%
    \ifthenelse{\equal{#1}{S}}{\substitle}{%
    \ifthenelse{\equal{#1}{U}}{\unitstitle}{%
    \ifthenelse{\equal{#1}{D}}{\defstitle}{}}}}}}

    %\newcommand{\nomunit}[1]{%
    % \renewcommand{\nomentryend}{\hspace*{\fill}$\mathrm{#1}$}}

    \usepackage{xcolor}

    \definecolor{grey60}{HTML}{746C66}
    \definecolor{grey40}{HTML}{A7A9AC}

    \usepackage{pgf}

    %\usepackage{bibentry}

    \usepackage{pgf}
    \usepackage{tikz}
    \usepackage{listings}
    \usepackage{tikz}
    \usepackage{pdfpages}

    \usepackage{pgfplots}
    \usetikzlibrary{shapes,arrows,calc,shadings,positioning,fit, trees, decorations.pathreplacing,}

    % argument #1: any options
    \newenvironment{customlegend}[1][]{%
        \begingroup
        % inits/clears the lists (which might be populated from previous
        % axes):
        \csname pgfplots@init@cleared@structures\endcsname
        \pgfplotsset{#1}%
    }{%
        % draws the legend:
        \csname pgfplots@createlegend\endcsname
        \endgroup
    }%

    \def\addlegendimage{\csname pgfplots@addlegendimage\endcsname}
    \usepackage{threeparttable}
    \usepackage{gensymb}
    \usepackage{cleveref}

    \usepackage{newunicodechar}
    \newunicodechar{FFFD}{HEREIAM}

    \@ifundefined{showcaptionsetup}{}{%
     \PassOptionsToPackage{caption=false}{subfig}}
    \usepackage{subfig}
    \AtBeginDocument{
      \def\labelitemi{\(\Rightarrow\)}
      \def\labelitemii{\(\rightarrow\)}
    }

    \makeatother
  \usepackage{nicefrac}
  \usepackage{gensymb}
  \usepackage{textcomp}
  \usepackage{import}
  \usepackage{amsfonts}
  \providecommand{\unit}[1]{\;\color{grey60}{\mathrm{#1}}}
  \providecommand{\ce}[1]{\mathrm{#1}}
  \providecommand{\cc}{\unit{cm^{3}}}
  %\newcommand\inputpgf[2]{{
    %\let\pgfimageWithoutPath\pgfimage
    %\renewcommand{\pgfimage}[2][]{\pgfimageWithoutPath[##1]{#1/##2}}
    %\input{#1/#2}
    %}}
  \newcommand{\dt}{$\mathrm{T}\left(d, n\right)$ }
  \newcommand{\dd}{$\mathrm{D}\left(d, n\right)$ }
  \newcommand{\ftcc}{($15\unit{cm^{3}}$) }
((* endblock packages *))

((* block error *))
((* endblock error *))

((* block stream *))
((* endblock stream *))

((* block markdowncell scoped *))
    ((( cell.source | citation2latex | strip_files_prefix | convert_pandoc('markdown', 'json', extra_args=['--chapters']) | resolve_references | convert_pandoc('json', 'latex', extra_args=['--chapters']) )))
((* endblock markdowncell *))

((* block data_markdown *))
    ((( output.data['text/markdown'] | citation2latex | strip_files_prefix | convert_pandoc('markdown', 'json', extra_args=['--chapters']) | resolve_references | convert_pandoc('json', 'latex', extra_args=['--chapters']) )))
((* endblock data_markdown *))

% Author and Title from metadata
((* block maketitle *))
\pudegree{Doctorate of Philosophy in Nuclear Engineering}{Ph.D. Candidate}{April}{2018}

\majorprof{Dr. Rusi P. Taleyarkhan}

\campus{West Lafayette}

\author{Alexander R. Hagen}{Hagen, Alexander R.}

\title{Detection and Interdiction of Shielded and Unshielded Special Nuclear
Material using Tensioned Metastable Fluid Detectors}

\date{\today}

\maketitle
\begin{statement}
\noindent Dr. Rusi P. Taleyarkhan, Chair\\
\null\qquad School of Nuclear Engineering and School of Health Sciences

\smallskip{}

\noindent Dr. Shripad T. Revankar\\
\null\qquad School of Nuclear Engineering

\smallskip{}

\noindent Dr. James F. Schweitzer\\
\null\qquad Radiological and Environmental Management and School of Health Sciencies

\smallskip{}

\noindent Dr. Robert S. Bean\\
\null\qquad School of Nuclear Engineering

\smallskip{}

\noindent Dr. Brian C. Archambault\\
\null\qquad School of Nuclear Engineering

\bigskip{}

\noindent \textbf{Approved by:}\\
\null\qquad Dr. Seungjin Kim\\
\null\qquad \qquad Head of the Graduate Program
\end{statement}
((* endblock maketitle *))
"""


__puslides_template__ = r"""((*- extends 'article.tplx' -*))

((* block input_group *))
    ((*- if cell.metadata.get('nbconvert', {}).get('show_code', False) -*))
        ((( super() )))
    ((*- endif -*))
((* endblock input_group *))

((* block data_latex -*))
    ((( output.data['text/latex'] | strip_files_prefix )))
((* endblock data_latex *))

((* set cell_style = 'style_bw_python.tplx' *))

((* block docclass *))

((*- if nb.metadata["confidential"]: -*))
    \documentclass[confidential,american,20pt]{puslides}
((*- else -*))
    \documentclass[american,20pt]{puslides}
((*- endif -*))
((* endblock docclass *))

((* block margins *))
((* endblock margins *))


((* block packages *))
((* endblock packages *))

((* block definitions *))
((* endblock definitions *))

((* block commands *))
((* endblock commands *))

((* block maketitle *))
((*- if nb.metadata["title"]: -*))
    \title{((( nb.metadata["title"] )))}
((*- else -*))
    \title{((( resources.metadata.name )))}
((*- endif -*))

((*- if nb.metadata["author"]: -*))
    \author{((( nb.metadata["author"] )))}
((*- else -*))
    \author{Alex Hagen}
((*- endif *))

\date{\today}

((*- if nb.metadata["affiliation"] and nb.metadata["subtitle"]: -*))
    \subtitle{((( nb.metadata["affiliation"] ))) \\ ((( nb.metadata["subtitle"])))}
((*- else -*))
    \subtitle{}
((*- endif *))

((*- if nb.metadata["venue"]: -*))
    \venue{((( nb.metadata["venue"] )))}
((*- else -*))
    \venue{}
((*- endif *))

((*- if nb.metadata["city"]: -*))
    \city{((( nb.metadata["city"] )))}
((*- else -*))
    \city{}
((*- endif *))

\maketitle


((*- if nb.metadata["author"]: -*))
    \def\theauthorsforbottom{((( nb.metadata["author"] )))}
((*- else -*))
    \def\theauthorsforbottom{A. Hagen}
((*- endif *))
((* endblock maketitle *))

((* block error *))
((* endblock error *))

((* block stream *))
((* endblock stream *))

((* block markdowncell scoped *))
    ((( cell.source | citation2latex | strip_files_prefix | convert_pandoc('markdown', 'json', extra_args=['--chapters']) | resolve_references | convert_pandoc('json', 'latex', extra_args=['--chapters']) )))
((* endblock markdowncell *))

((* block data_markdown *))
    ((( output.data['text/markdown'] | citation2latex | strip_files_prefix | convert_pandoc('markdown', 'json', extra_args=['--chapters']) | resolve_references | convert_pandoc('json', 'latex', extra_args=['--chapters']) )))
((* endblock data_markdown *))
"""

__templates__ = {'dissertation': __dissertation_template__,
                 'article': __article_template__,
                 'puslides': __puslides_template__,
                 'article2': __article2_template__}
