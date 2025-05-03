PYTHON = venv/bin/python3
TEX_DIR = tex
VENV = venv

"": all

all: rapport.pdf $(VENV)/pygame_installed src/cellular_automata.py demo

$(VENV)/pygame_installed: $(VENV)
	@$(PYTHON) -m pip install pygame
	@touch $(VENV)/pygame_installed

$(VENV):
	@python3 -m venv $(VENV)

tm:
	@$(PYTHON) src/turing_machine.py
	@$(PYTHON) src/turing_machine.py -q11 3
	@$(PYTHON) src/turing_machine.py -q12 11110111

ac:
	@$(PYTHON) src/cellular_automata.py
	@$(PYTHON) src/cellular_automata.py res/cycle.cel
	@$(PYTHON) src/cellular_automata.py res/palindrome.cel
	@$(PYTHON) src/cellular_automata.py res/pingpong.cel

translate:
	@$(PYTHON) src/translate.py
	@$(PYTHON) src/cellular_automata.py res/translated.cel

clean:
	-@rm $(TEX_DIR)/rapport.log
	-@rm $(TEX_DIR)/rapport.aux
	-@rm rapport.pdf
	-@rm -r $(VENV)

rapport.pdf: $(TEX_DIR)/rapport.tex
	@echo "Compilation du fichier latex..."
	@cd $(TEX_DIR);pdflatex -interaction=nonstopmode rapport.tex
	@mv $(TEX_DIR)/rapport.pdf .
	@echo "Compilation terminée !"

demo: tm ac translate