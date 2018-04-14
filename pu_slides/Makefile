all: handheld_ctmfd_design

latex: latex.lyx
	lyx --export xetex latex.lyx
	xelatex latex
	xelatex latex
	rm -f *.aux *.bbl *.blg *.log *.nlo *.tex *.ilg *.nls

handheld_ctmfd_design: handheld_ctmfd_design.lyx
		lyx --export xetex handheld_ctmfd_design.lyx
		xelatex handheld_ctmfd_design
		xelatex handheld_ctmfd_design
		rm -f *.aux *.bbl *.blg *.log *.nlo *.tex *.ilg *.nls
