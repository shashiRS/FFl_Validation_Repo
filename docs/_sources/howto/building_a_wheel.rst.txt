.. _TSF Build a wheel:

Build a Wheel
=====================
To create a wheel in the TSF organisation, follow the following steps:

#. Create a repo.

#. Add a webhook at :code:`repo/Settings/Hooks/Add Webhook`.

    * *Payload URL:* https://ams-adas-tsf-aws-jenkins.eu1.agileci.conti.de/github-webhook/

    * *Content type:* application/json

    * Select *Send me everything* under "**Which events would you like to trigger this webhook?**"

    * **Add Webhook**

#. Files needed for wheel creation:(these files were copied from tsf and was extended as required)

    * setup.py
        * packages define the folder to be wheeled

        * name of the wheel

        * description of the wheel

        * long description

        * url of the repo

        * *package_data* (extensions you would like to add to the wheel)

        * *entry_points* define the function which needs to be executed with the wheel

    * noxfile.py
        * In the nox file add the folder(s) which needs to be wheeled during linting.

        * In the tests you must run with :code:`"pytest", "--junitxml", "report.xml". "--cache-clear", "tests/{your folder name}/"`

    * requirements.txt
    * requirements_development.txt
    * pyproject.toml (needed for pre-commit)
    * Jenkinsfile
    * .flake8

#. Copy the pip.ini to :code:`C:\ProgramData\pip`  to make pip aware of the artifactory.

#. Execute the following commands:

    * :code:`pip install nox` in the vnev of the wheel

    * :code:`nox -s lint`

    * :code:`pip install build`

    * :code:`python -m build -w` (creates the wheel and a dist folder which has the wheel)

#. Check the wheel if all the files and folders in the repo are part of the wheel

    * If  any folders are missing then add :code:`__init__.py` file to those folders

#. Execute the following commands:

    * :code:`nox -s tests` (this tests the tests locally)

#. After successful tests, push all the changes to the branches.

#. In the Jenkins file, add :code:`publishCoverage` adapter and add :code:`archiveArtifacts` for coverage.

#. Create a batch file to run the tests locally with coverage.

#. In the nox file add the commands to run coverage for the repo.

#. Check-in everything and publish to the branch.
