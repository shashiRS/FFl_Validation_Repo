Command line arguments for runner.py
####################################

Here are the list of arguments which can be used with the report.py script with their definitions:

General arguments (runner)
**************************

.. list-table::
    :widths: 25 15 50
    :header-rows: 1

    * - Parameter
      - Argument (Type)
      - Description

    * - "json"
      - path
      - *mandatory* full path to the run_spec.json file.

    * - "-m" "\-\-multiprocessing"
      - 
      - if set enable multiprocessing

    * - "\-\-reporting" "-r"
      - 
      - if set parts of the report generation are done already in processing stage (e.g. Birdseye's, Event pages, Video exports).
        This will usually be the case

    * - "\-\-testrun-append"
      - 
      - if set append to an already existing testrun in the database

    * - "\-\-testrun-update"
      - 
      - if set update an already existing testrun in the database

    * - "\-\-matchbox-directory"
      - str
      - optional path to the matchbox directory (only needed for development report)

    * - "\-\-video-directory"
      - str
      - optional path to the video directory (only needed for development report)

    * - "-w" "\-\-working-directory"
      - path
      - manually override the 'temp' dir from config

    * - "\-\-check-inputs"
      - 
      - if set check if recording is available in the configured locations.

    * - "\-\-report-directory"
      - path
      - manually override the default report directory (for the backhaul script).

    * - "\-\-clean-dir"
      - 
      - if set delete the already existing working directory. **Use with caution**.

    * - "\-\-quiet" "-q"
      - (repeat_count)
      - lowers the logging level to stdout by one level for every count (e.g. -q will lower the logging level from the default WARNING to ERROR).

    * - "\-\-update-definitions"
      - 
      - *deprecated* in version 2.3.14. Use module/script tsf.testbench.utilities.update_definitions instead. (Or from Windows command-line: tsf-update_definitions.exe)

HPC specific arguments (runner)
*******************************

.. list-table::
    :widths: 25 15 50
    :header-rows: 1

    * - Parameter
      - Argument (Type)
      - Description

    * - "\-\-hpc"
      - 
      - if set submit processing to HPC

    * - "\-\-processing-headnode"
      - str
      - choose a dedicated Head node for TSF HPC processing, \-\-hpc option required

    * - "\-\-max-sockets" default=200
      - int
      - to limit the number of simultaneous jobs for TSF HPC processing, \-\-hpc option required. The default is 200.

    * - "\-\-venv-requirements"
      - str
      - Additional python Packages to install into venv on HPC without listing the test packages. TSF and the tC packages will be automatically uploaded.

Development/Debugging arguments (runner)
****************************************

.. list-table::
    :widths: 25 15 50
    :header-rows: 1

    * - Parameter
      - Argument (Type)
      - Description

    * - "\-\-debug-local"
      - 
      - if set generate a debugging local report using SQLite

    * - "\-\-debug-processing-recipes-limit"
      - int
      -

    * - "\-\-debug-processing-recipes-skip"
      - int
      -

    * - "\-\-verbose" "-v"
      - (repeat_count)
      - raise the logging level to stdout by one level for every count (e.g. -v will raise the logging level from the default WARNING to INFO, -vv will raise the level to DEBUG).



.. hint::
    If you an advanced user and would like to override TSFs default connection parameters or you would like to work with a local database for runner.py.
    Then checkout the :ref:`custom database connection parameters<Command line arguments for custom database connection (Optional)>`.


Examples of runner.py CLI commands
**********************************

Below are some example arguments which you can use for your runner.py.

* Running **runner.py**, for local processing using Oracle database with the logging level set to INFO:

.. code-block:: bash

    "<path-to-your-run-spec-json>.json"
    --clean-dir
    --check-inputs

* Running **runner.py**, for local processing using a local SQLite database with the logging level set to WARNING:

.. code-block:: bash

    "<path-to-your-run-spec-json>.json"
    --clean-dir
    --check-inputs
    --debug-local

* Running **runner.py**, for HPC processing using Oracle database with report pre-processing with the logging level set to DEBUG:

.. code-block:: bash

    "<path-to-your-run-spec-json>.json"
    --check-inputs
    -r
    --hpc
    -vv

* Running **runner.py**, to update testcase and teststep definitions:*(would be deprecated in TSF 3.X.X)*

.. code-block:: bash

    "<path-to-your-run-spec-json>.json"
    --update-definitions
    -vv