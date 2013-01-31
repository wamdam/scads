APP = scads
HERE = $(shell pwd)
BUILD_DIRS = docs/html cover

all: build

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  docs                 to create the documentation in html"
	@echo "  clean                to delete the generated html docs"

clean:
	-rm -rf $(BUILD_DIRS)

docs/html/index.html: docs/*.rst src/$(APP)/*.py
	make -f docs/Makefile html

docs: docs/html/index.html

.PHONY: clean docs help
