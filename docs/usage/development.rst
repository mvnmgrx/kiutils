Development
===========

To start developing, clone the repository and install ``kiutils`` from source while being in the
repository root folder:

.. code-block:: text

   git clone https://github.com/mvnmgrx/kiutils.git
   cd kiutils
   pip install -e .

Doing it this way, changes in the source will be reflected to the current Python environment
automatically. No need to reinstall after making changes.

For generating test reports as well as the documentation, install development requirements:

.. code-block:: text

  pip install -r requirements_dev.txt

Tests
-----

To run the test framework and generate an HTML report, start the test script:

.. code-block:: text

   python3 test.py

To only run the unittests, use:

.. code-block:: text

   python3 -m unittest

Generate documentation
----------------------

The documentation is generated using the ``sphinx`` module with autodoc enabled. Generate it by
running:

.. code-block:: text

   cd docs
   make html

The HTML output can then be accessed via ``docs/_build/html/index.html``. 