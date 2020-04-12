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
	source .venv/bin/activate; pip install -r requirements.txt

cleanvenv:
	rm -rf .venv

cleanimages:
	rm -rf images images-cropped logs contrib
	rm -f montage.jpg

clean: cleanvenv cleanimages

images: .venv
	. .venv/bin/activate; python -m selfie_bot

images-cropped: images
	mkdir images-cropped | true
	convert -trim 'images/*' ./images-cropped/%04d.png

montage: images-cropped
	. .venv/bin/activate; python ./contrib/collage_maker/collage_maker.py -f ./images-cropped -o montage.jpg -w 1920 -i 360 -s


montage-horizontal: images-cropped
	ls -d ./images-cropped/* | xargs -n 10 echo | xargs -I% bash -c "montage -background none -geometry 1920x1080 -tile x1 % out/montage-horizontal-\`dd if=/dev/urandom bs=1 count=4 2>/dev/null| xxd -ps\`.png"
