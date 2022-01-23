# VARIABLES THAT CAN BE OVERWRITTEN
# venv directory
VENV = env
# python binary path
PYTHON = $(VENV)/bin/python3
# pip binary path
PIP = $(VENV)/bin/pip

# TARGETS
run: env/bin/activate
	$(PYTHON) ./src/main.py
env/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt
clean:
	rm -rf __pycache__
	rm -rf $(VENV)