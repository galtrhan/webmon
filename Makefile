# WebMon Makefile
# Cross-platform commands for development

# Detect OS
ifeq ($(OS),Windows_NT)
    DETECTED_OS := Windows
else
    DETECTED_OS := $(shell uname -s)
endif

# Detect shell
ifeq ($(SHELL),/usr/bin/fish)
    DETECTED_SHELL := fish
else ifeq ($(SHELL),/bin/bash)
    DETECTED_SHELL := bash
else ifeq ($(DETECTED_OS),Windows)
    DETECTED_SHELL := cmd
else
    DETECTED_SHELL := bash
endif

# Virtual environment paths
VENV_DIR := venv
ifeq ($(DETECTED_OS),Windows)
    VENV_ACTIVATE := $(VENV_DIR)\Scripts\activate
    PYTHON := $(VENV_DIR)\Scripts\python
    PIP := $(VENV_DIR)\Scripts\pip
else
    VENV_ACTIVATE := $(VENV_DIR)/bin/activate
    PYTHON := $(VENV_DIR)/bin/python
    PIP := $(VENV_DIR)/bin/pip
endif

# Default target
.PHONY: help
help:
	@echo "WebMon Development Commands:"
	@echo "  dev      - Activate virtual environment"
	@echo "  install  - Create venv and install dependencies"
	@echo "  run      - Run the WebMon application"
	@echo "  clean    - Remove virtual environment"
	@echo "  deps     - Show installed dependencies"
	@echo ""
	@echo "Detected OS: $(DETECTED_OS)"
	@echo "Detected Shell: $(DETECTED_SHELL)"

# Activate virtual environment
.PHONY: dev
dev:
ifeq ($(DETECTED_OS),Windows)
	@echo "Activating virtual environment for Windows..."
	@echo "Run: $(VENV_ACTIVATE)"
	@echo "Or use: make run"
else ifeq ($(DETECTED_SHELL),fish)
	@echo "Activating virtual environment for Fish shell..."
	@echo "Run: source $(VENV_ACTIVATE).fish"
	@echo "Or use: make run"
else
	@echo "Activating virtual environment for Bash/Zsh..."
	@echo "Run: source $(VENV_ACTIVATE)"
	@echo "Or use: make run"
endif

# Install dependencies (create venv + install packages)
.PHONY: install
install:
	@echo "Setting up WebMon development environment..."
ifeq ($(DETECTED_OS),Windows)
	@echo "Creating virtual environment for Windows..."
	python -m venv $(VENV_DIR)
	@echo "Installing dependencies..."
	$(VENV_DIR)\Scripts\pip install -r requirements.txt
else
	@echo "Creating virtual environment for Unix..."
	python3 -m venv $(VENV_DIR)
	@echo "Installing dependencies..."
	$(VENV_DIR)/bin/pip install -r requirements.txt
endif
	@echo "Installation complete!"
	@echo "Run 'make run' to start the application"

# Run the application
.PHONY: run
run:
	@echo "Starting WebMon..."
ifeq ($(DETECTED_OS),Windows)
	$(PYTHON) main.py
else
	$(PYTHON) main.py
endif

# Clean virtual environment
.PHONY: clean
clean:
	@echo "Removing virtual environment..."
ifeq ($(DETECTED_OS),Windows)
	@if exist $(VENV_DIR) rmdir /s /q $(VENV_DIR)
else
	@rm -rf $(VENV_DIR)
endif
	@echo "Virtual environment removed"

# Show installed dependencies
.PHONY: deps
deps:
	@echo "Installed dependencies:"
ifeq ($(DETECTED_OS),Windows)
	$(PIP) list
else
	$(PIP) list
endif

# Check if config.json exists, create from sample if not
.PHONY: setup-config
setup-config:
	@if [ ! -f config.json ]; then \
		echo "Creating config.json from sample..."; \
		cp config.sample.json config.json; \
		echo "Please edit config.json with your settings"; \
	else \
		echo "config.json already exists"; \
	fi

# Full setup (install + config)
.PHONY: setup
setup: install setup-config
	@echo "Setup complete! Edit config.json and run 'make run'"