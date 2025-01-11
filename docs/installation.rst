Installation
============

Requirements
-----------

* Python 3.12 or higher
* Poetry (for development)

Using pip
--------

You can install Mix Tools SDK using pip:

.. code-block:: bash

   pip install mix-tools-sdk

Using Poetry (for development)
---------------------------

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/yourusername/mix-tools-sdk.git
      cd mix-tools-sdk

2. Install dependencies using Poetry:

   .. code-block:: bash

      poetry install

This will install all required dependencies including development packages.

Dependencies
-----------

Core Dependencies:
~~~~~~~~~~~~~~~~

* httpx: For making HTTP requests
* pydantic: For data validation and settings management

Development Dependencies:
~~~~~~~~~~~~~~~~~~~~~~

* pytest: For running tests
* pytest-asyncio: For testing async code
* black: For code formatting
* isort: For import sorting
* mypy: For static type checking
* pytest-cov: For test coverage reporting
