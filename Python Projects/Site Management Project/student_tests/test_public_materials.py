from typing import Any
from autograder_utils.Decorators import Weight, Number
from test_public_common import TestCommon
from Executors.Executor import Executor
from Executors.Environment import ExecutionEnvironmentBuilder, getResults
from StudentSubmissionImpl.Python.Runners import PythonRunnerBuilder, Parameter
import dill

class MaterialClassPublicTests(TestCommon):
    def setUp(self) -> None:
        self.environmentBuilder = ExecutionEnvironmentBuilder() \
            .setTimeout(5)

    def assertExecution(self, func, parameters: list, expectedOutput: Any):
        environment = self.environmentBuilder.build()

        runnerBuilder = PythonRunnerBuilder(self.studentSubmission) \
            .addInjectedCode(func.__name__,
                             dill.source.getsource(func, lstrip=True)) \
            .setEntrypoint(function=func.__name__) \
            .addParameter(parameter=Parameter(autowiredName="Material"))
        [runnerBuilder.addParameter(param) for param in parameters]
        runner = runnerBuilder.build()

        Executor.execute(environment, runner)
        actualOutput = getResults(environment).return_val

        self.assertEqual(expectedOutput, actualOutput)


    @Number(2.1)
    @Weight(.5)
    def test_material_class_initialization(self):
        """`Material Class` - Initialization"""

        givenID = 3

        def INJECTED_testMaterial_21(materialClass, ID):
            mat = materialClass(ID)
            return mat.getID()

        self.assertExecution(INJECTED_testMaterial_21, [givenID], givenID)

    @Number(2.2)
    @Weight(.5)
    def test_material_class_pricing(self):
        """`Material Class` - setPrice & getPrice"""

        givenID = 7
        givenPrice = 150

        def INJECTED_testMaterial_22(materialClass, ID, price):
            mat = materialClass(ID)
            mat.setPrice(price)
            return mat.getPrice()

        self.assertExecution(INJECTED_testMaterial_22, [givenID, givenPrice], givenPrice)

    @Number(2.3)
    @Weight(.5)
    def test_material_class_material_type(self):
        """`Material Class` - setMaterialType & getMaterialType"""

        givenID = 5
        givenType = 'BRICK'

        def INJECTED_testMaterial_23(materialClass, ID, type):
            mat = materialClass(ID)
            mat.setMaterialType(type)
            return mat.getMaterialType()

        self.assertExecution(INJECTED_testMaterial_23, [givenID, givenType], givenType)

    @Number(2.4)
    @Weight(.5)
    def test_material_class_ids(self):
        """`Material Class` - setID & getID"""

        arbitraryID = 5
        givenID = 633

        def INJECTED_testMaterial_24(materialClass, initialID, newID):
            mat = materialClass(initialID)
            mat.setID(newID)
            return mat.getID()

        self.assertExecution(INJECTED_testMaterial_24, [arbitraryID, givenID], givenID)