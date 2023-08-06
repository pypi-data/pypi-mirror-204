PWD = $(shell pwd)
VERSION = 0.1.3
VERBOSE ?= 

# ------------------------------------------------------------------
# Set up path local clone of dependencies supercede the installed ones.
# The paths should be absolute since tasks can be launched in their own working directories.
BASIC_PATH=$(PWD)/src:$(PWD)/../dls-logformatter/src
PYTHONPATH=$(BASIC_PATH)


pytest:
	PYTHONPATH=$(PYTHONPATH) \
	python3 -m pytest

# ------------------------------------------------------------------
# Tests individually (lib)

test:
	PYTHONPATH=tests:$(PYTHONPATH) \
	python3 -m pytest -sv -ra --tb=line tests/$(t)


# ------------------------------------------------------------------
# Rsync.

rsync:	
	../kbp43231_scripts/myrsync.py dls-utilpack

# ------------------------------------------------------------------
# Documentation.

sphinx:
	mkdir -p build/html
	PYTHONPATH=$(PYTHONPATH) \
	sphinx-build -EWT --keep-going docs build/html
	touch build/html/.nojekyll
 
publish_docs:
	git subtree push --prefix build/html origin gh-pages

# ------------------------------------------------------------------
# Utility.

tree:
	tree -I "__*" dls_bxflow_cli

	tree -I "__*" tests

.PHONY: list
list:
	@awk "/^[^\t:]+[:]/" Makefile | grep -v ".PHONY"

clean:
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '__pycache__' -exec rm -rf {} \;

show_version:
	PYTHONPATH=$(PYTHONPATH) python3 src/dls_utilpack/version.py --json
	PYTHONPATH=$(PYTHONPATH) python3 src/dls_utilpack/version.py

# ------------------------------------------------------------------
# Version bumping.  Configured in setup.cfg. 
# Thanks: https://pypi.org/project/bump2version/
bump-patch:
	bump2version --list patch

bump-minor:
	bump2version --list minor

bump-major:
	bump2version --list major
	
bump-dryrun:
	bump2version --dry-run patch

# Saved 44

