dls-utilpack
=======================================================================

Collection of various useful Python classes and functions

Intended advantages:

- reusable components
- hide complexity of oft-used patterns
- focused testing

Installation
-----------------------------------------------------------------------
::

    pip install git+https://gitlab.diamond.ac.uk/scisoft/dls-utilpack.git 

    dls-utilpack --version

Summary
-------------------------------------------------

callsign functions
    Extract and compose object identification used in logging.

datatype functions
    Validate strings according to expected data types.
    

Documentation
-----------------------------------------------------------------------

See http://www.cs.diamond.ac.uk/reports/gitlab-ci/dls-utilpack/index.html for more detailed documentation.

Building and viewing the documents locally::

    git clone git+https://gitlab.diamond.ac.uk/scisoft/dls-utilpack.git 
    cd dls-utilpack
    virtualenv /scratch/$USER/venv/dls-utilpack
    source /scratch/$USER/venv/dls-utilpack/bin/activate 
    pip install -e .[dev]
    make -f .dls-utilpack/Makefile validate_docs
    browse to file:///scratch/$USER/venvs/dls-utilpack/build/html/index.html

Topics for further documentation:

- TODO list of improvements
- change log


..
    Anything below this line is used when viewing README.rst and will be replaced
    when included in index.rst

