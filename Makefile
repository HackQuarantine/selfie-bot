.PHONY: env run clean
.DEFAULT: env
SHELL := /bin/bash
# List and check for commands.
COMMANDS = make
COMMAND_CHECK := $(foreach exec,$(COMMANDS), $(if $(shell which $(exec)),some string,$(error "No $(exec) in PATH")))
env:
	@echo "Building the python environment..."
	@python3 -m venv .venv
	@source .venv/bin/activate
	@pip install -r requirements.txt
	@cat creds_template.json > creds.json
	@echo "Please edit creds.json with your information!"
run:
	@source .venv/bin/activate
	@python -m selfie_bot
clean:
	@rm -rf .venv