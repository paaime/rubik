NAME = rubik_env
PYTHON = python3
VENV = $(NAME)/bin/activate
PIP = $(NAME)/bin/pip

REQUIREMENTS = vpython

.PHONY: all clean fclean re

all: $(NAME)
	@echo "Virtual environment created and dependencies installed"

$(NAME):
	@echo "Creating virtual environment..."
	@$(PYTHON) -m venv $(NAME)
	@echo "Installing dependencies..."
	@. $(VENV) && $(PIP) install --upgrade pip
	@. $(VENV) && $(PIP) install $(REQUIREMENTS)
	@echo "Configuration completed"

clean:
	@echo "Cleaning compiled Python files..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete

fclean: clean
	@echo "Deleting virtual environment..."
	@rm -rf $(NAME)
	@echo "Deleting saved models..."
	@rm -f *.npy
	@rm -f *.png
	@rm -rf models

re: fclean all

help:
	@echo "Available commands:"
	@echo "  make        : Create virtual environment and install dependencies"
	@echo "  make clean  : Delete compiled Python files"
	@echo "  make fclean : Delete virtual environment and generated files"
	@echo "  make re     : Reset everything"
	@echo "  make help   : Display this help"
