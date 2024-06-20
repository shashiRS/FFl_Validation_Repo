TSF Assessment sync tool
=================================

This Assement sync tool will help the user to sync the current assessments wrt to Recording collection to processing inputs.  

How Assessment sync tool works?

assessment_sync_tool reads the collection Id and fetches the recordings associated with it. Then it creates the new proc input for the recordings fetched.
Later a copy of assessment is created pointing to the proc_input. 

How to Execute assessment_sync_tool?

Pass the collection_id to the assessment_sync_tool with optional --sqlite param. 

.. code-block:: console

    python -m tsf.testbench.utilities.assessment_sync_tool --collection_id <collection_id> (This will use Dev DB)

.. code-block:: console

    python -m tsf.testbench.utilities.assessment_sync_tool --collection_id <collection_id> --sqlite <path_to_sqlite_db>