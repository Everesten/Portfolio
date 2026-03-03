from typing import Any
from autograder_utils.Decorators import Weight, Number
from test_public_common import TestCommon
from Executors.Executor import Executor
from Executors.Environment import ExecutionEnvironmentBuilder, getResults
from StudentSubmissionImpl.Python.Runners import PythonRunnerBuilder, Parameter
import dill

class ConstructionSiteClassPublicTests(TestCommon):
    def setUp(self) -> None:
        self.environmentBuilder = ExecutionEnvironmentBuilder()\
            .setTimeout(5)

    def assertExecution(self, func, parameters: list, expectedOutput: Any):
        environment = self.environmentBuilder.build()

        runnerBuilder = PythonRunnerBuilder(self.studentSubmission) \
            .addInjectedCode(func.__name__,
                             dill.source.getsource(func, lstrip=True)) \
            .setEntrypoint(function=func.__name__) \
            .addParameter(parameter=Parameter(autowiredName="ConstructionSite")) \
            .addParameter(parameter=Parameter(autowiredName="Material"))
        [runnerBuilder.addParameter(param) for param in parameters]
        runner = runnerBuilder.build()

        Executor.execute(environment, runner)
        actualOutput = getResults(environment).return_val

        self.assertEqual(expectedOutput, actualOutput)


    @Number(2.5)
    @Weight(.33)
    def test_construction_site_class_initialization_str(self):
        """`Construction Site` - Initialization & __str__"""

        givenName = "Rife"
        givenCity = "Golden"
        expectedStr = f"{givenName} site in {givenCity} has 0 materials, with a value of 0."

        def INJECTED_testConstructionSite_25(constructionSiteClass, materialClass, name, city):
            site = constructionSiteClass(name, city)
            return f"{site}"

        self.assertExecution(INJECTED_testConstructionSite_25, [givenName, givenCity], expectedStr)

    @Number(2.6)
    @Weight(.33)
    def test_construction_site_class_materials(self):
        """`Construction Site` - addMaterial & findMaterial"""

        givenName = "Rife"
        givenCity = "Golden"
        expectedID = 4

        def INJECTED_testConstructionSite_26(constructionSiteClass, materialClass, name, city, ID):
            site = constructionSiteClass(name, city)
            material = materialClass(ID)

            site.addMaterial(material)
            return site.findMaterial(ID).getID()

        self.assertExecution(INJECTED_testConstructionSite_26, [givenName, givenCity, expectedID], expectedID)

    @Number(2.7)
    @Weight(.34)
    def test_construction_site_class_prices(self):
        """`Construction Site` - calculatePrice"""

        givenName = "Rife"
        givenCity = "Golden"
        expectedPrice = 15392

        def INJECTED_testConstructionSite_27(constructionSiteClass, materialClass, name, city):
            site = constructionSiteClass(name, city)
            
            for id in range(3, 8, 2):
                newMaterial = materialClass(id)
                newMaterial.setPrice((id + 3) ** 4)
                site.addMaterial(newMaterial)
            site.calculatePrice()

            return site.price

        self.assertExecution(INJECTED_testConstructionSite_27, [givenName, givenCity], expectedPrice)

    @Number(2.8)
    @Weight(.5)
    def test_construction_site_class_material_count(self):
        """`Construction Site` - countMaterials"""

        givenName = "Rife"
        givenCity = "Golden"
        expectedCounts = [67, 67, 66]

        def INJECTED_testConstructionSite_28(constructionSiteClass, materialClass, name, city):
            site = constructionSiteClass(name, city)
            
            materialTypes = ["WOOD", "STEEL", "BRICK"]
            for id in range(200):
                newMaterial = materialClass(id)
                newMaterial.setMaterialType(materialTypes[id % 3])
                site.addMaterial(newMaterial)

            return site.countMaterials()

        self.assertExecution(INJECTED_testConstructionSite_28, [givenName, givenCity], expectedCounts)

    @Number(2.9)
    @Weight(.5)
    def test_construction_site_class_incorporation(self):
        """`Construction Site` - incorporateSite"""

        givenNameSiteOne, givenNameSiteTwo = "Rife", "Glitter"
        givenCitySiteOne, givenCitySiteTwo = "Golden", "Colorado Springs"
        expectedPrice = 739165
        expectedCounts = [184, 184, 182]

        def INJECTED_testConstructionSite_29(constructionSiteClass, materialClass, nameS1, cityS1, nameS2, cityS2):
            siteOne = constructionSiteClass(nameS1, cityS1)
            siteTwo = constructionSiteClass(nameS2, cityS2)

            materialTypes = ["WOOD", "STEEL", "BRICK"]
            for id in range(200):
                newMaterial = materialClass(id)
                newMaterial.setPrice((id + 7) * 34)
                newMaterial.setMaterialType(materialTypes[id % 3])
                siteOne.addMaterial(newMaterial)

            for id in range(350):
                newMaterial = materialClass(id)
                newMaterial.setPrice(id % 87)
                newMaterial.setMaterialType(materialTypes[id % 3])
                siteTwo.addMaterial(newMaterial)

            siteOne.incorporateSite(siteTwo)

            return [siteOne.price, siteOne.countMaterials()]

        self.assertExecution(INJECTED_testConstructionSite_29, [givenNameSiteOne, givenCitySiteOne, givenNameSiteTwo, givenCitySiteTwo], [expectedPrice, expectedCounts])