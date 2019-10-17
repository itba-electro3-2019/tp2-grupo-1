##################################################################
# Makefile for LaTeX
# Quiza es copy paste del github de Kevin...
##################################################################

REPORT_FILE = Informe
OTHER = *~ *.aux *.dvi *.toc *.bbl *.blg *.gz *.out *.thm *.ps *.idx *.ilg *.ind *.log *.fdb_latexmk *.fls

informe: $(REPORT_FILE).tex
	latexmk -synctex=1 -interaction=nonstopmode -f -file-line-error -pdf $(REPORT_FILE).tex
	rm -rf $(OTHER)
clean:
	rm -rf $(OTHER)
