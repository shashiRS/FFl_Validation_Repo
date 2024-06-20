Understanding run_spec.json
###########################

You will need a specification (Json file) for the testrun to use the runner script (usually named run_spec.json).
It mainly specifies which test cases should be executed and which inputs should be consumed. 

This section lists the parameters in a testrun specification and shows two examples that can be taken as a starting point.

* run_spec parameters
* basic run_spec
* advanced run_spec


run_spec parameters
*******************
Below you can find the list of possible run spec keys which the user can use to define their report settings, such as:

.. list-table:: run_spec.json parameters
    :widths: 25 15 50
    :header-rows: 1

    * - Parameter
      - (Json) Type
      - Description

    * - "project"
      - str
      - define your project

    * - "subject_under_test"
        "name"
        "test_discipline"
        "git_repo_url"
        "git_hash"
        "sw_creation_date_time"
        "tags"
      - str
      - define the simulation software used
        name of your software version
        define your test discipline
        if available, the git repository URL of the software
        if available, git commit hash of the software
        if available, the date of the software created
        if available, the tag of the software used

    * - "testrun"
      - str
      - name of the testrun you would like to use

    * - "testrun_id"
      - int
      - define the testrun_id if already known

    * - "processing_input"
      - str / list
      - define the processing input set(s) to use

    * - "recording_collection"
      - str
      - *deprecated*. Use "processing_input" instead

    * - "generic_input_collection"
      - str
      - *deprecated*. Use "processing_input" instead

    * - "versioned_input_collection"
      - str
      - *deprecated*. Use "processing_input" instead

    * - "testcases"
      - list
      - list of testcases that are to be executed using reference path from the repository root

    * - "statistics"
      - list
      - list of statistic testcases

    * - "custom_overviews"
      - str
      - list of custom overview testcases

    * - "custom_resource_dir"
      - str
      - if required, you can provide your own custom resource for your reports

    * - "custom_template_dir"
      - str
      - if required, you can provide your own custom report template

    * - "path_spec"/"input"
        "directory"
        "extension"
        "prefix"
        "suffix"
        "mount_point"
      - list of dicts
      - list of input simulation data
        path of the folder containing the input data
        extension of the input data
        any prefix you would like to add to the bsig names
        any suffix you would like to add to the bsig names (use * for split recordings)

    * - "temp_dir"
      - str
      - location of local temporary directory"

    * - "clean_dir"
      - flag
      - a clean dir flag to wipe the temp_dir"

    * - "hpc_jobname"
      - str
      - (for HPC reports) define the name HPC job you would like to create

    * - "hpc_project"
      - str
      - (for HPC reports) define the project of this report

    * - "hpc_template"
      - str
      - (for HPC reports) define HPC template to use

    * - "matchbox_directory"
      - str
      - matchbox directory for birdeye view

    * - "video_directory"
      - str
      - video directory for recordings for extracting images and video snippets

    * - "regression_path_spec" / "regression_input"
      - list
      - similar to "path_spec" for regression inputs

    * - "sync_assessments"
      - flag
      - flag to sync assessments to local DB

    * - "table_overview_additonal_info"
      - list of lists
      - key-value pair for adding additional report information

    * - "remarks"
      - str
      - remark text to add to the report

    * - "with_online_assessment"
      - flag
      - flag to use an online assessment method in place of matchbox

    * - "dev_report"
      - flag
      - flag to generate a development report

    * - "kpi_report"
      - flag
      - flag to generate a management report

    * - "open_explorer"
      - flag
      - flag to output location after the report is generated


Basic run_spec
**************

You can use this kind of run spec for basic implementations in which you are either debugging certain implementations of yours or you are just starting with TSF. You can later add on various features which can help you really help you utilize all TSF features.
The basic structure of a run_spec.json looks as the following:

.. code-block:: json

      {
      "project": "ARS5XX",                          // define your project
      "subject_under_test":  {                      // define the simulation software used
         "name": "001.002.345",                     // name of your software version
         "test_discipline": "algo"                  // define your test discipline
      },
      "processing_input": [
          "/ARS5XX/branch-1/child-1"                // define the input processing set to use
      ]
      "testrun": "Frankfurt_MERGE_Report",          // name of the testrun you would like to use

      "testcases": [                                // list of testcases that are to be executed
      "examples.quarantine.legacy.basic.minimal_example.CCrb"
      ],                                            // use reference path from repo root

      "input": [                                    // list of input simulation data
          {
            "directory": "D:\\examples\\data",      // path of the folder containing the input data
            "extension": ".bsig"                    // extension of the input data
          }
      ],
      "temp_dir":  "D:\\temp\\tsf",                 // location of the local temporary directory
      "clean_dir": false,                           // a clean dir flag to wipe the temp_dir
      "dev_report": true,                           // a flag to output a development report
    }

.. hint::
    You can use this run_spec as a template to start your implementation. (copy and paste this into new JSON file)

Advanced run_spec
*****************

You can use this kind of run spec for advanced implementations or project reports where you might have to submit HPC jobs with a large amount of data.
The advanced run_spec looks as the following:

.. code-block:: json

      {
      "project": "ARS5XX",
      "subject_under_test":  {                // subject under test with more information
         "name": "001.002.345",
         "test_discipline": "algo",
          "git_repo_url": "https://github-am.geo.conti.de/ADAS-Test-Scripting-Foundation"
          "git_hash": "s768sd"
      },
      "processing_input": [
          "/ARS5XX/branch-1/child-1"
      ]
      "testrun": "MERGE_Report",

      "table_overview_additonal_info": [        // additional information is added
      ["Report planned date", "20.02.2100"],
      ["Report executed date", "22.02.2101"]
      ],
      "remarks": "videos not available",        // remark is added to the report

      "testcases": [                            // multiple testcases that are planned to be executed for the report
      "examples.quarantine.legacy.basic.minimal_example.CCrb"
      "examples.quarantine.legacy.basic.minimal_example.CCrm"
      "examples.quarantine.legacy.basic.minimal_example.CCrs"
      ],

      "input": [                                // here we have defined multiple bsig locations as input for the report
          {
            "directory": "D:\\examples\\dataccrb",
            "extension": ".bsig"
          }
          {
            "directory": "D:\\examples\\dataccrs",
            "extension": ".bsig"
          }
          {
            "directory": "D:\\examples\\dataccrm",
            "extension": ".bsig"
          }
      ],
      "temp_dir":  "D:\\temp\\tsf",
      "hpc_jobname": "some HPC job name",         // HPC resources requested for processing and reporting
      "hpc_project": "project-1",
      "hpc_template": "PROJECT_VAL",
      "clean_dir": true,
      "kpi_report": false,
      "dev_report": true,
      "open_explorer": false,
      // custom matchbox and video directory provided
      "matchbox_directory": "some local matchbox directory",
      "video_directory": "some video directory"
    }

