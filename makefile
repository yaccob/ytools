%PHONY: all clean upload

all: README.rst ytools.egg-info

upload: ytools.egg-info
	twine upload dist/*

clean:
	-rm -rf *.pyc
	-rm -rf ytools/*.pyc
	-rm -rf dist
	-rm -rf ytools.egg-info
	-rm -f README.rst
	-rm -f MANIFEST

ytools.egg-info: ytools/ytools.py setup.py requirements.txt MANIFEST.in README.rst
	rm -rf dist
	python setup.py sdist

README.rst: README.md
	pandoc -f markdown_github -t rst $< -o $@
