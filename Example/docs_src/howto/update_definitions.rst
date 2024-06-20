.. _TSF Update Definitions Page:

Update definitions
==================

When to use
###########

   * Enables users to sync definitions [testcases/ teststeps/ statistics/ events/ assessments] with Database without having to run these implementations all over again

   * Users can choose to update definitions in single-go or choose to update them selectively or in an iterative manner

   * To scan the packages(local repository or artifactory packages) for the presence of new, deleted, migrated, or intact definitions

   * Upon request, user can have a holistic view of all different categories listed above

   * In automated workflows like CAEdge, this feature can be deployed with minimal configuration setup and the flow is entirely automated


How to run
##########
User should execute update_definitions.py by providing optional command line arguments for **sqlite** and **root**. If not provided, user will be prompted to provide one. 

.. code-block:: none

   python update_definitions.py --root="Some:\\Path\\eba" --sqlite="Some:\\Path\\tsf.sqlite"

.. note::
   * If *'root'* command line arg is not provided, user will be prompted to provide root repository/package which needs to be scanned
   * If *'sqlite'* command line arg is not provided, user will be prompted to provide local DB for sync. If user chooses not to provide local DB, TSF production DB will be used by default


Workflow
########
After performing all necessary configurations specified above, the following interactive workflow is encountered.

#. User need to select either of these definitions **(TestCases / TestSteps or Parameterized Testcase or Statistics or Events or Assessments)** to begin with the comprehensive scan

#. User is prompted to enter the component to be scanned. Ex: *eba*

#. If component/package entered is valid/present, based on user's choice, (considering **TestCases**) all the implementations (for TestCase) will be scanned for its availabiity in the component/package specified.

#. If scan returns no entries/ unresolved entries, they will be shown in red color and the workflow ends

#. If scan returns valid/resolved entries of implementations(**TestCases**), user can proceed to update definitions further:

   * A nicer categorization of resolved entries of definitions would be available for the user. Categorization is based on new, deleted, migrated or intact definitions, more info on them is available in the next section

   * Here, user can view the list of resolved entries under each category by making relevant selections and proceed further to update definitions for them

      * User has the option to update all the scanned item definitions in one-go

                                 or
      
      * User can decide to update the scanned item definitions iteratively

                                 or
      
      * User can update definitions in silos/standalone by entering the particular item using custom class reference path

                                 or
      
      * User can update definitions using run_spec.json available handy

#. After done with above step, user is prompted to either to sync/reject the changes to the referenced DB.


Categorization
##############

1. Newly-added :
^^^^^^^^^^^^^^^^

.. note::
   These are definitions which are found in package/repo of user implementation but not in DB


User prompted with the choice of ingesting the newly found item directly in DB

2. Migrated:
^^^^^^^^^^^^

.. note::
   These are definitions that are migrated by user to a different location but the implementation is still intact


* User prompted to re-run the definitions and to provide uri if its missing in the implementation

* If URI is present already, then they will be mentioned in a separate category

3. Deleted:
^^^^^^^^^^^

.. note::
   These are definitions which are found in DB but not in package/repo of user implementation

User is only notified that the definition is no more available on user side

4. Intact:
^^^^^^^^^^

.. note::
   These are definitions that are found in DB and present in package/repo of user implementation

Please note that these definitions can still have modifications which are updated while running this utility


Automated Workflows (like CAEdge)
#################################
 * Ensure that root repository and sqlite information is provided
 
 * Provide information on the definition to be scanned.

   .. note::
      * Currently, scan/update definitions is available for chosen definitions in one go

      * User cannot decide to choose a specific implementation to update
