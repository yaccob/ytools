PACKAGE=ytools

VERSION=`python -c "import $(PACKAGE); print($(PACKAGE).__version__)"`

%PHONY: all clean upload tag commit

all: install

README.rst: README.md
	pandoc -f markdown_github -t rst $< -o $@

install: dist build
	pip install -e .

dist: $(wildcard $(PACKAGE)/*.py) README.rst setup.py requirements.txt MANIFEST.in
	rm -rf $@
	python setup.py sdist

build: $(wildcard $(PACKAGE)/*.py) README.rst setup.py requirements.txt MANIFEST.in
	rm -rf $@
	python setup.py bdist_wheel

commit:
	-git commit -m "Committing for Version $(VERSION)"

tag: commit
	-git tag -a "v$(VERSION)" -m "Version $(VERSION)"
	-git push origin "v$(VERSION)"

upload: install tag
	twine upload dist/*

clean:
	#@for pattern in `cat .gitignore`; do find . -name "*/$$pattern" -delete; done
	-rm -rf *.pyc
	-rm -rf $(PACKAGE)/*.pyc
	-rm -rf dist
	-rm -rf build
	-rm -rf $(PACKAGE).egg-info
	-rm -f README.rst
	-rm -f MANIFEST
