Development
===========

To start developing, clone the repository:

.. code-block:: text

   git clone https://github.com/mvnmgrx/kiutils.git
   cd kiutils

For generating test reports as well as the documentation, install the development requirements:

.. code-block:: text

  pip install -r requirements_dev.txt

Tests
-----

Unittests are used to test ``kiutils``. To run the test framework and generate an HTML report, start 
the test script:

.. code-block:: text

   python3 test.py

When adding a feature to ``kiutils``, be sure to provide unittests that explicitly test the 
functionality you want to implement.

Generate documentation
----------------------

The documentation is generated using the ``sphinx`` module with autodoc enabled. Generate it by
running:

.. code-block:: text

   cd docs
   make html

The HTML output can then be accessed via ``docs/_build/html/index.html``. 