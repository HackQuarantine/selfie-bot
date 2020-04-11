.PHONY: run
SHELL := /bin/bash

# List and check for commands.
COMMANDS = make convert git
COMMAND_CHECK := $(foreach exec,$(COMMANDS), $(if $(shell which $(exec)),some string,$(error "No $(exec) in PATH")))

run: montage

.venv:
	git submodule init
	git submodule update
	virtualenv -p python3 .venv
	source .venv/bin/activate
	pip install -r requirements.txt

clean:
	rm -rf .venv images images-cropped logs contrib
	rm -f montage.jpg

images: .venv
	. .venv/bin/activate
	python -m selfie_bot

images-cropped: images
	mkdir images-cropped | true
	convert -trim 'images/*' ./images-cropped/%04d.png

montage: images-cropped
	python ./contrib/collage_maker/collage_maker.py -f ./images-cropped -o montage.jpg -w 1920 -i 360 -s
