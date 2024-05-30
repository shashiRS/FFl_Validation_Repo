Command line arguments for report.py
####################################

Here is the list of command line arguments that can be used with the report.py script with their definitions:

General arguments (report)
**************************

.. list-table::
    :widths: 25 15 50
    :header-rows: 1

    * - Parameter
      - Argument (Type)
      - Description

    * - "out_directory"
      - path
      - *mandatory* directory where the report is created in (temp_dir of runner.py)

    * - "testrun_id"
      - int
      - *mandatory* testrun ID

    * - "-s" "\-\-run-spec"
      -
      - full path to the run_spec.json file

    * - "-d" "\-\-development-details"
      - 
      - if set will create a report containing development details

    * - "-i" "\-\-input-directory" "\-\-input-directories"
      - str
      - optional directory to the runner output data (only needed for development report)

    * - "-m" "\-\-matchbox-directory"
      - str
      - optional path to the matchbox directory (only needed for development report)

    * - "\-\-video-directory"
      - str
      - optional path to the video directory (only needed for development report)

    * - "\-\-video-suffix"
      - str
      - optional file suffix to the videos (only needed for development report)

    * - "\-\-video-prefix"
      - str
      - optional file prefix to the videos (only needed for development report)

    * - "\-\-overview-plugins"
      - str
      - optional list of custom overview classes

    * - "\-\-statistic-plugins"
      - str
      - optional list of statistics classes

    * - "\-\-custom-resource-dir"
      - str
      - optional directory with custom resources, which will be copied into the report folder

    * - "\-\-custom-template-dir"
      - str
      - optional directories with custom templates, which will be made available to Jinja2

    * - "\-\-clean-dir"
      - 
      - if set deletes all contents from the report directory

    * - "\-\-redo-all"
      - 
      - if set re-computes all fragments, this is very slow

    * - "\-\-copy-local"
      - 
      - if set robocopy the input locally before starting

    * - "\-\-regression"
      - 
      - if set regression reporting is done

    * - "\-\-zip"
      - str
      - pack report into given the zip path and delete the contents

    * - "\-\-store-location"
      - str
      - path to the final report location

    * - "\-\-with-online-assessment"
      - 
      - enable assessment in the browser

    * - "\-\-quiet" "-q"
      - (repeat_count)
      - lowers the logging level to stdout by one level for every count (e.g. -q will lower the logging level from the default WARNING to ERROR)

HPC specific arguments (report)
*******************************

.. list-table::
    :widths: 25 15 50
    :header-rows: 1

    * - Parameter
      - Argument (Type)
      - Description

    * - "\-\-hpc"
      -
      - if set submit report generation to HPC

    * - "\-\-processing-headnode" "\-\-processing_headnode"
      - str
      - choose a dedicated Head-node for TSF HPC processing, \-\-hpc option required

    * - "\-\-runspec-headnode" "\-\-runspec_headnode"
      - select from "LU00160VMA", "LU00156VMA", "LSAS003A", or "OZAS012A"
      - HPC Head-node

    * - "\-\-runspec-jobid"
      - int
      - HPC Job ID

    * - "\-\-from-hpc-preprocessing" "\-\-from_hpc_preprocessing"
      -
      - if set only uses what is there from HPC

Development/Debugging arguments (report)
****************************************

.. list-table::
    :widths: 25 15 50
    :header-rows: 1

    * - Parameter
      - Argument (Type)
      - Description

    * - "\-\-debug-local"
      -
      - flag to generate a local report for debugging purposes

    * - "\-\-verbose" "-v"
      - (repeat_count)
      - raise the logging level to stdout by one level for every count (e.g. -v will raise the logging level from the default WARNING to INFO, -vv will raise the level to DEBUG)



.. note::
    The following arguments have been deprecated to opt for more standard versions of the same.
    "\-\-development_details", "\-\-statistic_plugins", "\-\-overview_plugins", "\-\-copy_local", "\-\-processing_headnode", "\-\-from_hpc_preprocessing", "\-\-runspec_headnode", "\-\-input_directory", "\-\-matchbox_directory", "\-\-clean_dir", "\-\-video_directory", "\-\-video_suffix", "\-\-video_prefix", "\-\-custom_resource_dir", "\-\-custom_template_dir", "\-\-redo_all, and "\-\-run_spec"

.. hint::
    If you are an advanced user and would like to override TSF's default connection parameters or you would like to work with a local database for report.py.
    Then check out the :ref:`custom database connection parameters<Command line arguments for custom database connection (Optional)>`.


Examples of report.py CLI commands
**********************************

Below are some example arguments which you can use for your report.py.

* Running **report.py**, for local reporting with no development details using Oracle database with the logging level set to INFO: (KPI report)

.. code-block:: bash

    "<path-to-your-temp-dir>\report"
    00000                                           // testrun id
    -i
    "<path-to-your-temp-dir>"

* Running **report.py**, for local reporting with no development details using local SQLite database with the logging level set to WARNING: (KPI report)

.. code-block:: bash

    "<path-to-your-temp-dir>\report"
    1                                               // testrun id as per SQLite database
    -i
    "<path-to-your-temp-dir>"
    --debug-local
    -v

* Running **report.py**, for local reporting with development details using Oracle database: (Development report)

.. code-block:: bash

    "<path-to-your-temp-dir>\report"
    00000                                           // testrun id
    -i
    "<path-to-your-temp-dir>"
    --development-details

* Running **report.py**, for local development report using Oracle database with HPC pre-processing:

.. code-block:: bash

    "<path-to-your-temp-dir>\report"
    00000                                           // testrun id
    -i
    "<path-to-your-temp-dir>"
    --development-details
    --from-hpc-preprocessing

* Running **report.py**, for local development report using Oracle database with HPC pre-processing with the logging level set to DEBUG:

.. code-block:: bash

    "<path-to-your-temp-dir>\report"
    00000                                           // testrun id
    -i
    "<path-to-your-temp-dir>"
    --development-details
    --from-hpc-preprocessing
    -vv

* Running **report.py**, for local development report with statistics and overview plugins using Oracle database with HPC pre-processing:

.. code-block:: bash

    "<path-to-your-temp-dir>\report"
    00000                                           // testrun id
    -i
    "<path-to-your-temp-dir>"
    --development-details
    --from-hpc-preprocessing
    --statistic-plugins
    <reference.path.of.your.statistic.plugin.class>
    --overview-plugins
    <reference.path.of.your.overview.plugin.class>


.. hint::
    Use the **"backhaul.bat"** in your output location to quickly generate the report without running the "report.py" separately.
    The batch file executes the report for you with all the required arguments thus saving a lot of time.

    This batch file is only generated if you execute the report processing with **runner.py**.


