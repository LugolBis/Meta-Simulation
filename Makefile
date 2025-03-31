PYTHON = venv/bin/python3
TEX_DIR = tex
VENV = venv

all: rapport.pdf $(VENV)/pygame_installed src/cellular_automata.py
	@$(PYTHON) src/main.py res/elargissement.cel

$(VENV)/pygame_installed: $(VENV)
	@$(PYTHON) -m pip install pygame
	@touch $(VENV)/pygame_installed

$(VENV): 
	@python3 -m venv $(VENV)

clean:
	-@rm $(TEX_DIR)/rapport.log
	-@rm $(TEX_DIR)/rapport.aux
	-@rm rapport.pdf
	-@rm -r $(VENV)
	-@rm res/example.txt

rapport.pdf: $(TEX_DIR)/rapport.tex
	@echo "Compilation du fichier latex..."
	@cd $(TEX_DIR);pdflatex -interaction=nonstopmode rapport.tex
	@mv $(TEX_DIR)/rapport.pdf .
	@echo "Compilation terminée !"


.PHONY: all clean
