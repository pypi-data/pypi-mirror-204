====================
Qt Multimedia Editor
====================

Copyright (c) 2023 Jérémie DECOCK (www.jdhp.org)

* Web site: http://www.jdhp.org/software_en.html#qtme
* Online documentation: https://jdhp.gitlab.io/qtme
* Examples: https://jdhp.gitlab.io/qtme/gallery/

* Notebooks: https://gitlab.com/jdhp/qt-multimedia-editor-notebooks
* Source code: https://gitlab.com/jdhp/qt-multimedia-editor
* Issue tracker: https://gitlab.com/jdhp/qt-multimedia-editor/issues
* Pytest code coverage: https://jdhp.gitlab.io/qtme/htmlcov/index.html
* Qt Multimedia Editor on PyPI: https://pypi.org/project/qtme
* Qt Multimedia Editor on Anaconda Cloud: https://anaconda.org/jdhp/qtme


Description
===========

Multimedia editor for PyQt/PySide

Note:

    This project is still in beta stage, so the API is not finalized yet.


Dependencies
============

C.f. requirements.txt

.. _install:

Installation
============

Posix (Linux, MacOSX, WSL, ...)
-------------------------------

From the Qt Multimedia Editor source code::

    conda deactivate         # Only if you use Anaconda...
    python3 -m venv env
    source env/bin/activate
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
    python3 setup.py develop


Windows
-------

From the Qt Multimedia Editor source code::

    conda deactivate         # Only if you use Anaconda...
    python3 -m venv env
    env\Scripts\activate.bat
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
    python3 setup.py develop


Documentation
=============

* Online documentation: https://jdhp.gitlab.io/qtme
* API documentation: https://jdhp.gitlab.io/qtme/api.html


Example usage
=============

* Examples: https://jdhp.gitlab.io/qtme/gallery/


Build and run the Python Docker image
=====================================

Build the docker image
----------------------

From the Qt Multimedia Editor source code::

    docker build -t qtme:latest .

Run unit tests from the docker container
----------------------------------------

From the Qt Multimedia Editor source code::

    docker run qtme pytest

Run an example from the docker container
----------------------------------------

From the Qt Multimedia Editor source code::

    docker run qtme python3 /app/examples/hello.py


Bug reports
===========

To search for bugs or report them, please use the Qt Multimedia Editor Bug Tracker at:

    https://gitlab.com/jdhp/qt-multimedia-editor/issues


License
=======

This project is provided under the terms and conditions of the `MIT License`_.


.. _MIT License: http://opensource.org/licenses/MIT
.. _command prompt: https://en.wikipedia.org/wiki/Cmd.exe
