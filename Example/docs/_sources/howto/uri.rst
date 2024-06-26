Uniform Resource Identifier (URI)
=================================

*TSF-563: URI New in version 2.4.9.*

A Uniform Resource Identifier (URI) is a unique set of characters that identifies
a logical or physical resource used by web technologies. URIs may be used to identify anything,
including real-world objects, such as people and places, concepts, or information
resources such as web pages and books etc.

TSF currently uses the reference class path as a means to identify testcases, teststeps, events, and assessments.
With the URI approach, test engineers can refactor their package structure without worrying about changed class paths.
This would be helpful in certain deployment scenarios where a change in classpath might affect during execution and
therefore resulting in unforeseen issues in the pipeline.

.. note::

   If you are interested finding out more about URI you can check this `wiki <https://en.wikipedia.org/wiki/Uniform_Resource_Identifier>`_

UUID
####

A universally unique identifier (UUID) is a 128-bit label used for information in computer systems.
When generated according to the standard methods, UUIDs are, practically unique.

In the following code block, you can easily generate a unique identifier (uuid4).

.. code-block:: python
    :emphasize-lines: 2,3

    import uuid
    uuid.uuid4()
    UUID('3042137c-284f-431a-9ab8-8dae293b5b77')


Using URI
^^^^^^^^^

In this section we would briefly discuss how to decorate the classes.
.. code-block:: python

    @uri(object_type://component/uuid4)


Here,

* **@uri** is a class decorator for testcases, teststeps, events, and assessments.
* **object_type** is the type of object where the URI is used i.e. testcase, teststep, event, or assessment.
* **component** is a internal function used for development such as EBA, ACC, CVF, RDI, etc.
* **uuid4** is the universally unique identifier.

Now, we know how to decorate our classes with URIs. Let's have a look at the following sub-sections, how to register our
testcases, teststeps, events, and assessments with URI as a decorator.

Testcase
********

In testcases, the URI can be used in the following way,

for a generic testcase,

.. code-block:: python
   :emphasize-lines: 1,3

   @uri("testcase://component/e4d2a32b-76ed-4371-b00d-162f823cadc9")
   @register_inputs("/Project-1/example-2")
   class ExampleKpiTestCase(TestCase):
       @property
       def test_steps(self):
           return [ExampleTestStep1, ExampleTestStep2]

whereas for Parameterized Testcases with Parameterized Teststeps,

.. code-block:: python
   :emphasize-lines: 1,8,9,25,26,27,28

   class ExampleParameterizedTestCaseUri(ParameterizedTestCase):
       @classmethod
       def compute_parameters(cls) -> List[ParameterSet]:
           parameters_1 = [111, 222, 333]
           parameters_2 = [999, 888, 777]
           parameter_sets = [
               ParameterSet(
                   uri=f"testcase://component/455f53af-7a34-4e70-9add-81afb265c3da?
                   {urlencode(dict(parameter_1=parameter_1, parameter_2=parameter_2))}",
                   name=f"Parameterized testcase with first parameter: {parameter_1}, second parameter: {parameter_2}",
                   description="A generic parameterized testcase.",
                   assignments=[
                       Assignment(
                           ctype=ProcessingInputSet, name=f"/function-1/project-1/testcase-{parameter_1}-{parameter_2}"
                       )
                   ],
                   verifies=[
                       f"requirement_testcase-{parameter_1}-{parameter_2}",
                   ],
                   doors_url=f"ts_requirement_testcase-{parameter_1}-{parameter_2}",
                   teststep_parameters=[
                       TeststepParameter(
                           test_step=ExampleTestStep,
                           name="Check for activation",
                           uri=(
                               "teststep://component/dbc28e93-335f-43a0-b7ce-cd0b43ba9c16?"
                               f"{urlencode(dict(parameter_1=parameter_1, parameter_2=parameter_2))}"
                           ),
                           description="Checks the correct activation in time.",
                           expected_result=ExpectedResult(
                               50,
                               unit="%",
                               operator=RelationOperator.GREATER,
                               aggregate_function=AggregateFunction.ALL,
                           ),
                           doors_url="",
                       )
                   ],
                   parameter_1=parameter_1,
                   parameter_2=parameter_2,
               )
               for en_parameter_2, parameter_2 in enumerate(parameters_2)
               for en_parameter_1, parameter_1 in enumerate(parameters_1)
           ]
           return parameter_sets

       parameter_sets = compute_parameters


Teststep
********

In a Teststep the URI can be used in the following way,

for a generic teststep,

.. code-block:: python
   :emphasize-lines: 1,15

   @uri("teststep://component/091eccf7-c472-4bcd-8462-536151e80bb8")
   @teststep_definition(
       1,
       "Count activations of signal A",
       "Example for counting an activation rate. Over more than a single input.",
       ExpectedResult(
           0.3,
           unit="1/km",
           numerator_is_events=True,
           operator=RelationOperator.LESS_OR_EQUAL,
           aggregate_function=AggregateFunction.KPI,
       ),
   )
   @register_signals(EXAMPLE_1, ExampleSignals1)
   class ExampleTestStep1(TestStep):
       """Dummy test step."""
       pass

for a Confusion Matrix TestStep,

.. code-block:: python
   :emphasize-lines: 1,2

   @uri("teststep://component/7c782c1e-a268-43c9-8a67-c9a3300e29e4")
   class MyConfusionMatrixTestStep2(ConfusionMatrixTestStep):
       """Dummy confusion matrix test step."""
       pass

Event
*****

For events, the URI can be used in the following way,

.. code-block:: python
   :emphasize-lines: 1,2

   @uri("event://component/ad2b8d16-abfe-4bb0-83eb-2f4c9f49551e")
   class ExampleEvent(Event):
       """Example Event."""

       assessment_type = ExampleAssessment

       prop_1 = EventAttribute("Prop 1", AttributeType.FLOAT)
       prop_2 = EventAttribute("Prop 2", AttributeType.INTEGER)
       prop_3 = EventAttribute("Prop 3", AttributeType.STRING)


Assessment
**********

For Assessments, the URI can be used in the following way:

.. code-block:: python
   :emphasize-lines: 1,2

   @uri("assessment://component/fcda7c46-863d-40ed-8a9c-0e7c029950b0")
   class ExampleAssessment(ExplicitAssessment):
       """An example assessment."""

       states = {
           "TP": asf.state("True Positive", False),
           "Testing Ground": asf.state("Testing Ground", False),
           "Irrelevant": asf.state("Irrelevant", False),
           "FP": asf.state("False Positive", True),
       }
       comment = aaf.string_attribute("Comment")