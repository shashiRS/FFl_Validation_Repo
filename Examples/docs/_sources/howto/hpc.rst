Submit to HPC
=============

This page describes how to submit TSF processing (``runner.py``) and report generation (``report.py``) to HPC.

For general information on HPC see the documentation at `High Performance Computing <https://confluence.auto.continental.cloud/display/GITTE/High+Performance+Computing>`_

Prerequisites (HPC submit)
--------------------------

- You need permissions/credentials to submit jobs to HPC. See the HPC documentation (link above) on how to aquire permission and set the credentials.
- Your repository must conform to Pythons import system. Especially it must be properly set up according to `Python rules for packages <https://docs.python.org/3/reference/import.html#regular-packages>`_ (`__init__py`)
- Processing and report generation should be working locally using ``runner.py`` and ``report.py`` (for testing you can reduced inputs only exemplary recording(s)).

Settings in run_spec.json
-------------------------

The specification you provide to processing and report generation (``run_spec.json``) must include three 
mandatory parameters for submitting to HPC:

.. code-block:: json
   :emphasize-lines: 4-6

    {
        // ...

        "hpc_jobname": "some HPC job name",         // HPC resources requested for processing and reporting
        "hpc_project": "project-1",
        "hpc_template": "PROJECT_VAL",

        // ...
    }

The HPC job name **must** follow a naming convention.
`HPC job name validation <https://github-am.geo.conti.de/pages/ADAS/HPC_two/hpc.core.html#hpc.core.tds.validate_name>`_

The HPC template **must** be one of the available templates on the HPC cluster that are allowed to be used for TSF (or your project).
At the time of this writing ``ARS_SRR`` and ``PROJECT_VAL`` can be used for TSF.

Start processing and report generation locally with submit to HCP
-----------------------------------------------------------------

To submit to HPC you just need to add the ``--hpc`` command line argument when calling ``runner.py`` and ``report.py``

For additional arguments specific to HPC see :ref:`HPC specific arguments for runner.py <HPC specific arguments (runner)>` and 
:ref:`HPC specific arguments for report.py <HPC specific arguments (report)>`

"Backhaul" for mixing HPC processing and local report generation
----------------------------------------------------------------

... (explain backhaul magic)


Tipps for troubleshooting and debugging
---------------------------------------

...

Special consideration for using HPC via automation pipeline
-----------------------------------------------------------

... (packaging in wheel and deployment to artifactory)