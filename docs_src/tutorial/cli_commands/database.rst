Command line arguments for custom database connection (Optional) 
################################################################

As an advanced user you can override the TSFs defaults database login parameters. These parameters can be used in the command line in addition to
arguments used for runner.py and report.py.

The table below lists them in detail:

.. list-table:: Command line arguments for custom database connection
    :widths: 25 15 50
    :header-rows: 1

    * - Parameter
      - Argument (Type)
      - Description

    * - "\-\-sqlite"
      - str
      - if a custom connection to SQLite is required

    * - "\-\-login"
      - str
      - if you would like to override the current login user

    * - "\-\-dialect"
      - str
      - database dialect if a custom connection is used

    * - "\-\-user"
      - str
      - database user if a custom connection is used

    * - "\-\-password"
      - str
      - database password if a custom connection is used

    * - "\-\-host"
      - str
      - database host if a custom connection is used

    * - "\-\-port"
      - str
      - database port if a custom connection is used

    * - "\-\-service"
      - str
      - oracle service if a custom connection is used

    * - "\-\-dsn"
      - str
      - oracle DSN if a custom connection is used

    * - "\-\-database"
      - str
      - database name if a custom connection is used

    * - "\-\-token"
      - str
      - if all the details are already in a token

.. hint::
    If these terms don't make much sense then you are the wrong place. Please continue using TSFs default database login parameters.