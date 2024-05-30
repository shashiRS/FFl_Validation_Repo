Setup Python
============

This page will guide you through the python setup for ADAS TSF.

Preconditions
-------------
Installed python interpreter (>= 3.6). We need to setup pip to make use of the internal artifactory PYPI mirror.
Please download the https://github-am.geo.conti.de/ADAS-Test-Scripting-Foundation/tsf/blob/develop/utilities/pip.ini and place it to

.. code-block:: console

   %APPDATA%\pip\pip.ini

or any of the other config locations.

Virtual Environment
-------------------

Create a virtual requirement

.. code-block:: console

   cd <path_to_example_repository>
   python -m venv my_venv
   my_venv\Scripts\activate.bat
   pip install -r requirements.txt

the requirements.txt should contain the tsf version you would like to use. For ex.

.. code-block:: console

      adas-tsf==2.2.0
      numpy
      pandas
      plotly


Usage
-----

From the commandline (e.g. cmd, powershell, git bash) make sure to call

.. code-block:: console

   my_venv\Scripts\activate.bat

Before running any of the examples.

When using an IDE you can point the interpret to the venv directly:


.. figure:: pycharm_add_interpreter.png
      :align: left

      Add interpreter in PyCharm




.. figure:: vs_code_add_interpreter.png
      :align: left

      Add interpreter in Visualstudio Code



..
   .. code-block:: ruby
      :linenos:

      Some more Ruby code.