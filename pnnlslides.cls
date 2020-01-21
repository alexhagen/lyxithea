
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{puslides}[2014/04/03 Purdue slides class]

\RequirePackage{ifthen}

\newboolean{conf}
\setboolean{conf}{false}
\DeclareOption{confidential}{\setboolean{conf}{true}}
\ProcessOptions\relax

%% Load base
\LoadClass[english, 10pt]{book}

\RequirePackage{graphicx}
\RequirePackage{color}
\RequirePackage{lipsum}
\RequirePackage{datetime}
\RequirePackage{etoolbox}
\RequirePackage{forloop}
\RequirePackage{pbox}
\RequirePackage{fontspec}
\RequirePackage{tikz}
\RequirePackage{framed}
\RequirePackage{wallpaper}
\RequirePackage{fancyhdr}
\RequirePackage{import}
\RequirePackage{algorithmic}
\RequirePackage{multicol}
\RequirePackage{url}
\usepackage[absolute,overlay]{textpos}
\RequirePackage{anyfontsize}
\usepackage{amstext}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{fontspec}
\usepackage[landscape,paperwidth=7in,paperheight=9in]{geometry}
\geometry{verbose,tmargin=0cm,bmargin=0cm,lmargin=0cm,rmargin=0cm,headheight=0cm,headsep=0cm,footskip=0cm}
\setcounter{secnumdepth}{3}
\setcounter{tocdepth}{3}
\usepackage{float}
\usepackage{units}
\usepackage{hyperref}
\usepackage{graphicx}
\usepackage{media9}
\usepackage{array}
\PassOptionsToPackage{version=3}{mhchem}
\usepackage{mhchem}
\usepackage[numbers]{natbib}
%\usepackage{biblatex}
\usepackage{luatex85}
\usepackage{pgf}
\usepackage{xcolor}
\usepackage{color}
\usepackage{xparse}
\usepackage{soul}
\usepackage{tikz}
\usetikzlibrary{shapes,arrows,calc,positioning,automata}
\usetikzlibrary{shapes.geometric}   % For trapezium
\usetikzlibrary{patterns, snakes}%
\usetikzlibrary{backgrounds,scopes}%
\usepackage{pdfpages}
\usepackage{float}
\usepackage{ifthen}
\usepackage{xunicode}
\usepackage{polyglossia}
\setdefaultlanguage[variant=american]{english}
\usepackage{bibentry}
\nobibliography*
\usepackage{makecell}
\usepackage{outlines}
\usepackage{adjustbox}

\renewcommand{\theenumi}{\Roman{enumi}. }
\renewcommand{\labelenumi}{\theenumi}

\renewcommand{\theenumii}{\Alph{enumii}. }
\renewcommand{\labelenumii}{\theenumii}

\renewcommand{\theenumiii}{\roman{enumiii}. }
\renewcommand{\labelenumiii}{\theenumiii}

\renewcommand{\theenumiv}{\alph{enumiv}) }
\renewcommand{\labelenumiv}{\theenumiv}

\newcounter{cenum}
\newcounter{cenumsaved}
\setcounter{cenumsaved}{0}
\newcommand{\labelcenum}{\arabic{cenum}.}
\newenvironment{cenumerate}%
{\begin{list}{\labelcenum}{\usecounter{cenum}}%
\setcounter{cenum}{\value{cenumsaved}}}%
{\setcounter{cenumsaved}{\value{cenum}}%
\end{list}}

\vfuzz = 500pt

\definecolor{grey20}{RGB}{225, 225, 225}
\definecolor{grey40}{RGB}{179, 179, 179}
\definecolor{grey60}{RGB}{97, 98, 101}
\definecolor{gold}{RGB}{244, 170, 0}
\definecolor{copper}{RGB}{215, 118, 0}
\definecolor{652C}{RGB}{114,153,198}
\definecolor{1675C}{RGB}{185,89,21}
\definecolor{teal}{RGB}{0, 129, 171}
\definecolor{green}{HTML}{007836}
\definecolor{yellow}{RGB}{215, 170, 0}
\definecolor{red}{HTML}{BE0F34}
\NewDocumentCommand{\sotwo}{O{red}O{black}+m}
    {%
        \begingroup
        \setulcolor{#1}%
        \setul{-.6ex}{2pt}%
        \def\SOUL@uleverysyllable{%
            \rlap{%
                \color{#2}\the\SOUL@syllable
                \SOUL@setkern\SOUL@charkern}%
            \SOUL@ulunderline{%
                \phantom{\the\SOUL@syllable}}%
        }%
        \ul{#3}%
        \endgroup
    }

%\providecommand{\tightlist}{}

\providecommand{\tightlist}{}
\providecommand{\invis}[1]{}
\providecommand{\todo}[1]{}

\def\pocketslides{}
\newcommand\savepocketslide[1]{\g@addto@macro\pocketslides{#1}}

\floatname{algorithm}{Source Code}
\newcommand{\algorithmname}{Source Code}

\AtBeginDocument{
  \def\labelitemi{\(\Rightarrow\)}
  \def\labelitemii{\(\rightarrow\)}
  \def\labelitemiii{\(\rightarrow\)}
}


\newcommand{\nameofsubtitle}{}
\newcommand{\nameofvenue}{}
\newcommand{\nameofcity}{}

\newfontfamily\champion[Path = fonts/]{champion-htf-featherweight.otf}
\newfontfamily\myriad[Path = fonts/,
  ItalicFont=MyriadPro-CondIt.otf,
  BoldFont=MyriadPro-BoldCond.otf,
  BoldItalicFont=MyriadPro-BoldCondIt.otf]{MyriadPro-Cond.otf}
\newfontfamily\chaparral[Path=fonts/,
  ItalicFont=ChaparralPro-Italic.otf,
  BoldFont=ChaparralPro-Bold.otf,
  BoldItalicFont=ChaparralPro-BoldIt.otf]{ChaparralPro-Regular.otf}
\setmainfont[Path=fonts/,
  ItalicFont=MyriadPro-CondIt.otf,
  BoldFont=MyriadPro-BoldCond.otf,
  BoldItalicFont=MyriadPro-BoldCondIt.otf]{MyriadPro-Cond.otf}
\setsansfont[Path=fonts/,
  ItalicFont=MyriadPro-CondIt.otf,
  BoldFont=MyriadPro-BoldCond.otf,
  BoldItalicFont=MyriadPro-BoldCondIt.otf]{MyriadPro-Cond.otf}

%\DeclareMathSizes{10}{14}{10}{6}
%\DeclareMathSizes{12}{14}{10}{6}
%\DeclareMathSizes{14.4}{20}{14}{10}


\newcommand\pucopper[1]{\textcolor{copper}{\textbf{#1}}}
\newcommand\teal[1]{\textcolor{teal}{#1}}
\newcommand\pucite[1]{\textcolor{grey60}{#1}}

\newcounter{numberpart}
\newcounter{index}

\newcounter{cnt}
\newcommand\textlist{}
\newcommand\settext[2]{%
  \csdef{text#1}{#2}}
\newcommand\addtext[1]{%
  \stepcounter{cnt}%
  \csdef{text\thecnt}{#1}}
\newcommand\gettext[1]{%
  \csuse{text#1}}

\renewcommand{\part}[1]{%
\addtocounter{numberpart}{1}%
\addtext{#1}%
\global\def\nameofpart{#1}}

\renewcommand{\section}[1]{\global\def\nameofsection{#1}}
\renewcommand{\title}[1]{\global\def\nameoftitle{#1}}
\renewcommand{\author}[1]{\global\def\nameofauthor{#1}}
\renewcommand{\maketitle}{}

\newcommand*\quotesize{60} % if quote size changes, need a way to make shifts relative
% Make commands for the quotes
\newcommand*{\openquote}
   {\tikz[remember picture,overlay,xshift=-1ex,yshift=0.5ex]
   \node (OQ) {\color{grey20}\chaparral\fontsize{\quotesize}{\quotesize}\selectfont“};\kern0pt}

\newcommand*{\closequote}[1]
  {\tikz[remember picture,overlay,xshift=1ex,yshift={#1}]
   \node (CQ) {\color{grey20}\chaparral\fontsize{\quotesize}{\quotesize}\selectfont”};}

% select a colour for the shading
\colorlet{shadecolor}{white!0}

\newcommand*\shadedauthorformat{\chaparral\emph} % define format for the author argument

% Now a command to allow left, right and centre alignment of the author
\newcommand*\authoralign[1]{%
  \if#1l
    \def\authorfill{}\def\quotefill{\hfill}
  \else
    \if#1r
      \def\authorfill{\hfill}\def\quotefill{}
    \else
      \if#1c
        \gdef\authorfill{\hfill}\def\quotefill{\hfill}
      \else\typeout{Invalid option}
      \fi
    \fi
  \fi}

% wrap everything in its own environment which takes one argument (author) and one optional argument
% specifying the alignment [l, r or c]
%
\newenvironment{shadequote}[2][r]%
{\authoralign{#1}
\ifblank{#2}
   {\def\shadequoteauthor{}\def\yshift{-2ex}\def\quotefill{\hfill}}
   {\def\shadequoteauthor{\par\authorfill\shadedauthorformat{#2}}\def\yshift{2ex}}
\begin{snugshade}\begin{quote}\openquote\chaparral\Large}
{\normalfont{\color{grey40}\shadequoteauthor}\quotefill\closequote{\yshift}\end{quote}\end{snugshade}}

\newcommand{\squote}[2]{
  \begin{shadequote}[r]{#1}
  #2
  \end{shadequote}
}

\newlength\tindent
\setlength{\tindent}{\parindent}
\setlength{\parindent}{0pt}
\renewcommand{\indent}{\hspace*{\tindent}}

\newcommand{\nameofpagenumber}{\thepage}

\newenvironment{content}{}{}

\newcommand{\subtitle}[1]{\def\nameofsubtitle{#1}}
\newcommand{\venue}[1]{\def\nameofvenue{#1}}
\newcommand{\city}[1]{\def\nameofcity{#1}}

\newcommand{\puhf}{
    % Page Number
  \begin{textblock}{0.25}(4.375,6.54)
    \begin{minipage}[t][0.30 in][c]{0.25 in}\centering
      \color{white}\champion\LARGE{\nameofpagenumber}
    \end{minipage}
  \end{textblock}
    % Confidential
    \ifthenelse{\boolean{conf}}{
      \begin{textblock}{3}(3,6.25)
        \begin{minipage}[t][0.30 in][c]{3 in}\centering
          \small{\color{grey60} Confidential - Not for Dissemination}
        \end{minipage}
      \end{textblock}
    }{}
  % Author and Venue
  \begin{textblock}{4}(4.85,6.54)
    \begin{minipage}[t][0.30 in][c]{4 in}\raggedright
      \color{grey40} \small{\theauthorsforbottom}\\ \today\hspace{0.1em}at \nameofvenue
    \end{minipage}
  \end{textblock}
  % Title of Paper
  \begin{textblock}{4}(0.15,6.54)
    \begin{minipage}[t][0.30 in][c]{4 in}\raggedleft
      \color{grey40} \small{\nameoftitle}
    \end{minipage}
  \end{textblock}
  % Section Title
  \begin{textblock}{8.5}(0.25,0.4)
    \begin{minipage}[b][0.75 in][c]{8.5 in}\raggedright
      \champion \Huge{\color{copper} \nameofchapter : \color{grey40} \nameofsection}
    \end{minipage}
  \end{textblock}
  % Part Titles
  \begin{textblock}{8.5}(0.00,0.00)
    \raggedright
    \forloop[1]{index}{1}{\value{index} < \value{numberpart}}{%
          \chaparral\colorbox{grey20}{\color{white}{\textsc{\gettext{\arabic{index}}}}}}
          \chaparral\colorbox{copper}{\color{white}{\textsc{\gettext{\arabic{numberpart}}}}}
  \end{textblock}
}

\newcommand{\puchapthf}{
    % Page Number
  \begin{textblock}{0.25}(4.375,6.54)
    \begin{minipage}[t][0.30 in][c]{0.25 in}\centering
      \color{white}\champion\LARGE{\nameofpagenumber}
    \end{minipage}
  \end{textblock}
    % Confidential
    \ifthenelse{\boolean{conf}}{
      \begin{textblock}{3}(3,6.25)
        \begin{minipage}[t][0.30 in][c]{3 in}\centering
          \small{\color{grey60} Confidential - Not for Dissemination}
        \end{minipage}
      \end{textblock}
    }{}
  % Author and Venue
  \begin{textblock}{4}(4.85,6.54)
    \begin{minipage}[t][0.30 in][c]{4 in}\raggedright
      \color{grey40} \small{\nameofauthor}\\ \today\hspace{0.1em}at \nameofvenue
    \end{minipage}
  \end{textblock}
  % Title of Paper
  \begin{textblock}{4}(0.15,6.54)
    \begin{minipage}[t][0.30 in][c]{4 in}\raggedleft
      \color{grey40} \small{\nameoftitle}
    \end{minipage}
  \end{textblock}
  % Part Titles
  \begin{textblock}{8.5}(0.00,0.00)
    \raggedright
    \forloop[1]{index}{1}{\value{index} < \value{numberpart}}{%
          \chaparral\colorbox{grey20}{\color{white}{\textsc{\gettext{\arabic{index}}}}}}
          \chaparral\colorbox{copper}{\color{white}{\textsc{\gettext{\arabic{numberpart}}}}}
  \end{textblock}
}

\renewcommand{\chapter}[2]{\def\nameofchapter{#2} \def\nameoflongchapter{#1}
  \newpage
  \ThisCenterWallPaper{1}{css/pnnl_chapter_outer.pdf}
  \thispagestyle{fancy}
  \renewcommand{\headrulewidth}{0pt}
  \fancyhf{}

  \hspace{1in}
  \begin{textblock}{8}(0.75,1.75)
    \begin{minipage}[s][1.0 in][c]{7.5 in}\raggedright {\fontsize{60}{80}\selectfont \color{grey60} \champion
      #1
    }
    \end{minipage}
  \end{textblock}

  \puchapthf
  \newpage

  %chapterslide
}

\newcommand{\chapterslide}[3]{\def\nameofchapter{#3} \def\nameoflongchapter{#1}
  \newpage
  \ThisCenterWallPaper{1}{css/pnnl_chapter_outer.pdf}
  \thispagestyle{fancy}
  \renewcommand{\headrulewidth}{0pt}
  \fancyhf{}

  \hspace{1in}
  \begin{textblock}{8}(0.75,1.75)
    \begin{minipage}[s][1.0 in][c]{7.5 in}\raggedright {\fontsize{60}{80}\selectfont \color{grey60} \champion
      #1
    }
    \end{minipage}
  \end{textblock}

  \hspace{1in}
  \begin{textblock}{8}(0.75,4.25)
    \begin{minipage}[s][1.0 in][c]{7.5 in}\raggedright {\fontsize{16}{18}\selectfont \color{black} \chaparral
      #2
    }
    \end{minipage}
  \end{textblock}

  \puchapthf
  \newpage

  %chapterslide
}

\newcommand{\putitle}{
    % Subtitle
    \begin{textblock}{6}(1.5,5.35)
      \begin{minipage}[c][0.5 in][s]{6 in}\centering
        \large{\myriad\emph{\nameofsubtitle}}
      \end{minipage}
    \end{textblock}
    % Venue and Date
    \begin{textblock}{6}(1.5,5.6)
      \fontsize{20}{20}
      \begin{minipage}[c][0.5 in][s]{6 in}\centering
        \large{\today\hspace{0.2em}at \nameofvenue}\\ \normalsize{\nameofcity}
      \end{minipage}
    \end{textblock}%
    % Author
    \begin{textblock}{6}(1.5,4.75)
      \begin{minipage}[c][0.5 in][s]{6 in}\centering
        \chaparral \color{grey60} \Large{\nameofauthor}
      \end{minipage}
    \end{textblock}%
    % Title
    \begin{textblock}{7}(1,2.0)
      \begin{minipage}[c][1.5 in][c]{7 in}\centering
        {\champion \color{copper} \fontsize{60}{54}\selectfont \nameoftitle}
      \end{minipage}
    \end{textblock}%
}

  \setlength{\TPHorizModule}{1in}
  \setlength{\TPVertModule}{\TPHorizModule}

\def\maketitle{
  \ThisCenterWallPaper{1}{css/pnnl_title_page.pdf}
  \thispagestyle{fancy}
  \renewcommand{\headrulewidth}{0pt}
  \fancyhf{}

  \hspace{1in}
  \putitle

  \setcounter{numberpart}{0}
  \newpage
}

\newcommand{\onecolumnslide}[2]
  {
  \newpage
  \ThisCenterWallPaper{1}{css/pnnl_slide_outer.pdf}
  \thispagestyle{fancy}
  \renewcommand{\headrulewidth}{0pt}
  \fancyhf{}

  \def\nameofsection{#2}
  \hspace{1in}
  % Column
  \begin{textblock}{7.5}(0.75,1.0)
    \begin{minipage}[s][5.25 in][c]{7.5 in}\raggedright { \LARGE
      #1
    }
    \end{minipage}
  \end{textblock}
  \puhf
  \newpage
  }

\newcommand{\twocolumnslide}[3]
  {
  \newpage
  \ThisCenterWallPaper{1}{css/pnnl_slide_outer.pdf}
  \thispagestyle{fancy}
  \renewcommand{\headrulewidth}{0pt}
  \fancyhf{}

  \def\nameofsection{#3}
  \hspace{1in}
  % Left Column
  \begin{textblock}{3.375}(0.75,1.0)
    \begin{minipage}[s][5.25 in][c]{3.375 in}\raggedright { \LARGE
      #1
    }
    \end{minipage}
  \end{textblock}
  % Right Column
  \begin{textblock}{3.375}(4.875,1.0)
    \begin{minipage}[s][5.25 in][c]{3.375 in}\raggedright { \LARGE
      #2
    }
    \end{minipage}
  \end{textblock}
  \puhf
  \newpage
  }

\newcommand{\twocolumnshiftright}[3]
  {
  \newpage
  \ThisCenterWallPaper{1}{css/pnnl_slide_outer.pdf}
  \thispagestyle{fancy}
  \renewcommand{\headrulewidth}{0pt}
  \fancyhf{}

  \def\nameofsection{#3}
  \hspace{1in}
  % Left Column
  \begin{textblock}{4.5}(0.75,1.0)
    \begin{minipage}[s][5.25 in][c]{4.5 in}\raggedright { \LARGE
      #1
    }
    \end{minipage}
  \end{textblock}
  % Right Column
  \begin{textblock}{2.25}(5.625,1.0)
    \begin{minipage}[s][5.25 in][c]{2.25 in}\raggedright { \LARGE
      #2
    }
    \end{minipage}
  \end{textblock}
  \puhf
  }

\newcommand{\twocolumnshiftleft}[3]
  {
  \newpage
  \ThisCenterWallPaper{1}{css/pnnl_slide_outer.pdf}
  \thispagestyle{fancy}
  \renewcommand{\headrulewidth}{0pt}
  \fancyhf{}

  \def\nameofsection{#3}
  \hspace{1in}
  % Left Column
  \begin{textblock}{2.25}(0.75,1.0)
    \begin{minipage}[s][5.25 in][c]{2.25 in}\raggedright { \LARGE
      #1
    }
    \end{minipage}
  \end{textblock}
  % Right Column
  \begin{textblock}{4.5}(3.375,1.00)
    \begin{minipage}[s][5.25 in][c]{4.5 in}\raggedright { \LARGE
      #2
    }
    \end{minipage}
  \end{textblock}
  \puhf
  }

\newcommand{\tworow}[3]
  {
  \newpage
  \ThisCenterWallPaper{1}{css/pnnl_slide_outer.pdf}
  \thispagestyle{fancy}
  \renewcommand{\headrulewidth}{0pt}
  \fancyhf{}

  \def\nameofsection{#3}
  \hspace{1in}
  % Top Row
  \begin{textblock}{7.5}(0.75,1.0)
    \begin{minipage}[s][2.375 in][c]{7.5 in}\raggedright { \LARGE
      #1
    }
    \end{minipage}
  \end{textblock}
  % Bottom Row
  \begin{textblock}{7.5}(0.75,3.75)
    \begin{minipage}[s][2.375 in][c]{7.5 in}\raggedright { \LARGE
      #2
    }
    \end{minipage}
  \end{textblock}
  \puhf
  }

  \newcommand{\tworowpushdown}[3]
    {
    \newpage
    \ThisCenterWallPaper{1}{css/pnnl_slide_outer.pdf}
    \thispagestyle{fancy}
    \renewcommand{\headrulewidth}{0pt}
    \fancyhf{}

    \def\nameofsection{#3}
    \hspace{1in}
    % Top Row
    \begin{textblock}{7.5}(0.75,1.0)
      \begin{minipage}[s][3.75 in][c]{7.5 in}\raggedright { \LARGE
        #1
      }
      \end{minipage}
    \end{textblock}
    % Bottom Row
    \begin{textblock}{7.5}(0.75,5.125)
      \begin{minipage}[s][1.125 in][c]{7.5 in}\raggedright { \LARGE
        #2
      }
      \end{minipage}
    \end{textblock}
    \puhf
    }

    \newcommand{\tworowpushup}[3]
      {
      \newpage
      \ThisCenterWallPaper{1}{css/pnnl_slide_outer.pdf}
      \thispagestyle{fancy}
      \renewcommand{\headrulewidth}{0pt}
      \fancyhf{}

      \def\nameofsection{#3}
      \hspace{1in}
      % Top Row
      \begin{textblock}{7.5}(0.75,1.0)
        \begin{minipage}[s][1.125 in][c]{7.5 in}\raggedright { \LARGE
          #1
        }
        \end{minipage}
      \end{textblock}
      % Bottom Row
      \begin{textblock}{7.5}(0.75,2.5)
        \begin{minipage}[s][3.75 in][c]{7.5 in}\raggedright { \LARGE
          #2
        }
        \end{minipage}
      \end{textblock}
      \puhf
      }


  \newcommand{\tworowtoptwocolumn}[4]
    {
    \newpage
    \ThisCenterWallPaper{1}{css/pnnl_slide_outer.pdf}
    \thispagestyle{fancy}
    \renewcommand{\headrulewidth}{0pt}
    \fancyhf{}

    \def\nameofsection{#3}
    \hspace{1in}
    \def\nameofsection{#4}
    \hspace{1in}
    % Top Left
    \begin{textblock}{3.375}(0.75,1.0)
      \begin{minipage}[s][2.375 in][c]{3.375 in}\raggedright { \LARGE
        #1
      }
      \end{minipage}
    \end{textblock}
    % Top Right
    \begin{textblock}{3.375}(4.75,1.0)
      \begin{minipage}[s][2.375 in][c]{3.375 in}\raggedright { \LARGE
        #2
      }
      \end{minipage}
    \end{textblock}
    % Bottom Row
    \begin{textblock}{7.5}(0.75,3.75)
      \begin{minipage}[s][2.375 in][c]{7.5 in}\raggedright { \LARGE
        #3
      }
      \end{minipage}
    \end{textblock}
    \puhf
    }

    \newcommand{\tworowbottomtwocolumn}[4]
    {
    \newpage
    \ThisCenterWallPaper{1}{css/pnnl_slide_outer.pdf}
    \thispagestyle{fancy}
    \renewcommand{\headrulewidth}{0pt}
    \fancyhf{}

    \def\nameofsection{#3}
    \hspace{1in}
    \def\nameofsection{#4}
    \hspace{1in}
    % Top Row
    \begin{textblock}{7.5}(0.75,1.0)
      \begin{minipage}[s][2.375 in][c]{7.5 in}\raggedright { \LARGE
        #3
      }
      \end{minipage}
    \end{textblock}
    % Bottom Left
    \begin{textblock}{3.375}(0.75,3.75)
      \begin{minipage}[s][2.375 in][c]{3.375 in}\raggedright { \LARGE
        #1
      }
      \end{minipage}
    \end{textblock}
    % Bottom Right
    \begin{textblock}{3.375}(4.75,3.75)
      \begin{minipage}[s][2.375 in][c]{3.375 in}\raggedright { \LARGE
        #2
      }
      \end{minipage}
    \end{textblock}
    \puhf
    }


\newcommand{\tworowleftsidebar}[4]
  {
  \newpage
  \ThisCenterWallPaper{1}{css/pnnl_slide_outer.pdf}
  \thispagestyle{fancy}
  \renewcommand{\headrulewidth}{0pt}
  \fancyhf{}

  \def\nameofsection{#4}
  \hspace{1in}
  % Top Row
  \begin{textblock}{4.5}(3.75,1.0)
    \begin{minipage}[s][2.375 in][c]{4.5 in}\raggedright { \LARGE
      #1
    }
    \end{minipage}
  \end{textblock}
  % Bottom Row
  \begin{textblock}{4.5}(3.75,3.75)
    \begin{minipage}[s][2.375 in][c]{4.5 in}\raggedright { \LARGE
      #2
    }
    \end{minipage}
  \end{textblock}
  % Left Sidebar
  \begin{textblock}{2.25}(0.75,1.0)
    \begin{minipage}[s][5.125 in][c]{2.25 in}\raggedright { \LARGE
      #3
    }
    \end{minipage}
  \end{textblock}
  \puhf
  }

\newcommand{\tworowrightsidebar}[4]
  {
  \newpage
  \ThisCenterWallPaper{1}{css/pnnl_slide_outer.pdf}
  \thispagestyle{fancy}
  \renewcommand{\headrulewidth}{0pt}
  \fancyhf{}

  \def\nameofsection{#4}
  \hspace{1in}
  % Top Row
  \begin{textblock}{4.5}(0.75,1.0)
    \begin{minipage}[s][2.375 in][c]{4.5 in}\raggedright { \LARGE
      #1
    }
    \end{minipage}
  \end{textblock}
  % Bottom Row
  \begin{textblock}{4.5}(0.75,3.75)
    \begin{minipage}[s][2.375 in][c]{4.5 in}\raggedright { \LARGE
      #2
    }
    \end{minipage}
  \end{textblock}
  % Right Sidebar
  \begin{textblock}{2.25}(5.625,1.0)
    \begin{minipage}[s][5.125 in][c]{2.25 in}\raggedright { \LARGE
      #3
    }
    \end{minipage}
  \end{textblock}
  \puhf
  }

\newcommand{\tworowtwocolumn}[5]
  {
  \newpage
  \ThisCenterWallPaper{1}{css/pnnl_slide_outer.pdf}
  \thispagestyle{fancy}
  \renewcommand{\headrulewidth}{0pt}
  \fancyhf{}

  \def\nameofsection{#5}
  \hspace{1in}
  % Top Left
  \begin{textblock}{3.375}(0.75,1.0)
    \begin{minipage}[s][2.375 in][c]{3.375 in}\raggedright { \LARGE
      #1
    }
    \end{minipage}
  \end{textblock}
  % Bottom Left
  \begin{textblock}{3.375}(0.75,3.75)
    \begin{minipage}[s][2.375 in][c]{3.375 in}\raggedright { \LARGE
      #2
    }
    \end{minipage}
  \end{textblock}
  % Top Right
  \begin{textblock}{3.375}(4.75,1.0)
    \begin{minipage}[s][2.375 in][c]{3.375 in}\raggedright { \LARGE
      #3
    }
    \end{minipage}
  \end{textblock}
  % Bottom Right
  \begin{textblock}{3.375}(4.75,3.75)
    \begin{minipage}[s][2.375 in][c]{3.375 in}\raggedright { \LARGE
      #4
    }
    \end{minipage}
  \end{textblock}
  \puhf
  }

  \newcommand{\twocolumnrighttworow}[4]
    {
    \newpage
    \ThisCenterWallPaper{1}{css/pnnl_slide_outer.pdf}
    \thispagestyle{fancy}
    \renewcommand{\headrulewidth}{0pt}
    \fancyhf{}

    \def\nameofsection{#4}
    \hspace{1in}
    % Left Column
    \begin{textblock}{3.375}(0.75,1.0)
      \begin{minipage}[s][5.25 in][c]{3.375 in}\raggedright { \LARGE
        #1
      }
      \end{minipage}
    \end{textblock}
    % Top Right
    \begin{textblock}{3.375}(4.75,1.0)
      \begin{minipage}[s][2.375 in][c]{3.375 in}\raggedright { \LARGE
        #2
      }
      \end{minipage}
    \end{textblock}
    % Bottom Right
    \begin{textblock}{3.375}(4.75,3.75)
      \begin{minipage}[s][2.375 in][c]{3.375 in}\raggedright { \LARGE
        #3
      }
      \end{minipage}
    \end{textblock}
    \puhf
    }

  \newcommand{\fourcolumn}[5]
    {
    \newpage
    \ThisCenterWallPaper{1}{css/pnnl_slide_outer.pdf}
    \thispagestyle{fancy}
    \renewcommand{\headrulewidth}{0pt}
    \fancyhf{}

    \def\nameofsection{#5}
    \hspace{1in}
    % Top Left
    \begin{textblock}{1.625}(0.75,1.0)
      \begin{minipage}[s][5.25 in][c]{1.625 in}\raggedright { \LARGE
        #1
      }
      \end{minipage}
    \end{textblock}
    % Bottom Left
    \begin{textblock}{1.625}(2.5,1.0)
      \begin{minipage}[s][5.25 in][c]{1.625 in}\raggedright { \LARGE
        #2
      }
      \end{minipage}
    \end{textblock}
    % Top Right
    \begin{textblock}{1.625}(4.75,1.0)
      \begin{minipage}[s][5.25 in][c]{1.625 in}\raggedright { \LARGE
        #3
      }
      \end{minipage}
    \end{textblock}
    % Bottom Right
    \begin{textblock}{1.625}(6.5,1.0)
      \begin{minipage}[s][5.25 in][c]{1.625 in}\raggedright { \LARGE
        #4
      }
      \end{minipage}
    \end{textblock}
    \puhf
    }

    \newcommand{\threecolumn}[4]
      {
      \newpage
      \ThisCenterWallPaper{1}{css/pnnl_slide_outer.pdf}
      \thispagestyle{fancy}
      \renewcommand{\headrulewidth}{0pt}
      \fancyhf{}

      \def\nameofsection{#4}
      \hspace{1in}
      % Left
      \begin{textblock}{2.333}(0.75,1.0)
        \begin{minipage}[s][5.25 in][c]{2.333 in}\raggedright { \LARGE
          #1
        }
        \end{minipage}
      \end{textblock}
      % Middle
      \begin{textblock}{2.333}(3.33,1.0)
        \begin{minipage}[s][5.25 in][c]{2.333 in}\raggedright { \LARGE
          #2
        }
        \end{minipage}
      \end{textblock}
      % Right
      \begin{textblock}{2.333}(5.916,1.0)
        \begin{minipage}[s][5.25 in][c]{2.333 in}\raggedright { \LARGE
          #3
        }
        \end{minipage}
      \end{textblock}
      \puhf
      }

    \newcommand{\tworowthreecolumn}[7]
      {
      \newpage
      \ThisCenterWallPaper{1}{css/pnnl_slide_outer.pdf}
      \thispagestyle{fancy}
      \renewcommand{\headrulewidth}{0pt}
      \fancyhf{}

      \def\nameofsection{#7}
      \hspace{1in}
      % Top Left
      \begin{textblock}{2.333}(0.75,1.0)
        \begin{minipage}[s][2.375 in][c]{2.333 in}\raggedright { \LARGE
          #1
        }
        \end{minipage}
      \end{textblock}
      % Bottom Left
      \begin{textblock}{2.333}(0.75,3.75)
        \begin{minipage}[s][2.375 in][c]{2.333 in}\raggedright { \LARGE
          #4
        }
        \end{minipage}
      \end{textblock}
      % Top Middle
      \begin{textblock}{2.333}(3.33,1.0)
        \begin{minipage}[s][2.375 in][c]{2.333 in}\raggedright { \LARGE
          #2
        }
        \end{minipage}
      \end{textblock}
      % Bottom Middle
      \begin{textblock}{2.333}(3.33,3.75)
        \begin{minipage}[s][2.375 in][c]{2.333 in}\raggedright { \LARGE
          #5
        }
        \end{minipage}
      \end{textblock}
      % Top Right
      \begin{textblock}{2.333}(5.916,1.0)
        \begin{minipage}[s][2.375 in][c]{2.333 in}\raggedright { \LARGE
          #3
        }
        \end{minipage}
      \end{textblock}
      % Bottom Right
      \begin{textblock}{2.333}(5.916,3.75)
        \begin{minipage}[s][2.375 in][c]{2.333 in}\raggedright { \LARGE
          #6
        }
        \end{minipage}
      \end{textblock}
      \puhf
      }

%% Bibliography stuff

\def\bibname{}

\newenvironment{milestone}[1][0]{
\renewcommand{\theenumi}{\champion \color{grey60} \Roman{enumi}}
 \LARGE \bf \color{copper} \begin{enumerate} \setcounter{enumi}{#1}}
 {\end{enumerate}
 \renewcommand{\theenumi}{\Arabic{enumi}}}

\newcommand{\heading}[1]{\LARGE{\champion #1}}

\renewcommand{\subsection}[1]{\heading{#1}}
\renewcommand{\subsubsection}[1]{\Large{\champion #1}}
\endinput