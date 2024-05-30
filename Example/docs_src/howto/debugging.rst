Debugging
=========

Debug a test case implementation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This demos demonstrate how to call your test case implementation and process
it with a couple of bsigs and produce a report on the processed results.

This is very useful during development since it won't require access to the oracle
database or HPC.

All you need is a couple of processing outputs (e.g. BSIGs) with function output
of the component you want to test.

.. literalinclude:: ../../src/examples/debug/single_bsig.py
    :linenos:
    :pyobject: main
    :language: python

The full example can be found in `examples/debug/single_bsig.py <https://github-am.geo.conti.de/ADAS-Test-Scripting-Foundation/examples/src/examples/debug/single_bsig.py>`_.


Process two BSIGs in parallel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Many simulations output more than one BSIG file but multiple either
split by processing cycle, device, ...

To process two (or more) input files you need to define Path


.. literalinclude:: ../../src/examples/debug/single_bsig.py
    :linenos:
    :pyobject: main
    :language: python

The full example can be found in `examples/debug/single_bsig.py <https://github-am.geo.conti.de/ADAS-Test-Scripting-Foundation/examples/src/examples/debug/single_bsig.py>`_.
