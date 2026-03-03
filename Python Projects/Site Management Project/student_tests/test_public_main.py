from autograder_utils.Decorators import Weight, Number
from test_public_common import TestCommon
from Executors.Executor import Executor
from Executors.Environment import ExecutionEnvironmentBuilder, getResults
from StudentSubmissionImpl.Python.Runners import PythonRunnerBuilder

class ConstructionMaterialsPublicTests(TestCommon):
    def setUp(self) -> None:
        self.environmentBuilder = ExecutionEnvironmentBuilder() \
            .setTimeout(5) \
            .setDataRoot(self.autograderConfig.build.data_files_source)
   
    def assertStdIO(self, inputs: list, expectedOutput: list):
        environment = self.environmentBuilder \
            .addFile(f"public/{inputs[0]}", f"./{inputs[0]}") \
            .addFile(f"public/{inputs[1]}", f"./{inputs[1]}") \
            .setStdin(inputs) \
            .build()

        runner = PythonRunnerBuilder(self.studentSubmission) \
            .setEntrypoint(module=True) \
            .build()

        Executor.execute(environment, runner)
        actualOutput = getResults(environment).stdout
        
        self.assertListEqual(expectedOutput, actualOutput)
    

    @Number(1.1)
    @Weight(.33)
    def test_sample_exeuction_1(self):
        """Sample Execution #1"""

        inputList = ["mat1.txt", "materialList.txt"]
        expectedList = [
            "Bloom site in Arvada has 333 materials, with a value of 164160.",
            "Wood:105 Steel:119 Brick:109",
            "Beck site in Golden has 19 materials, with a value of 549.",
            "Wood:7 Steel:6 Brick:6",
            "Bloom site in Arvada has 352 materials, with a value of 164709."
        ]

        self.assertStdIO(inputList, expectedList)

    @Number(1.2)
    @Weight(.33)
    def test_sample_exeuction_2(self):
        """Sample Execution #2"""

        inputList = ["long.txt", "materialList.txt"]
        expectedList = [
            "Crazy site in Longmont has 100000 materials, with a value of 49993483.",
            "Wood:33361 Steel:33350 Brick:33289",
            "Beck site in Golden has 19 materials, with a value of 549.",
            "Wood:7 Steel:6 Brick:6",
            "Crazy site in Longmont has 100019 materials, with a value of 49994032."
        ]

        self.assertStdIO(inputList, expectedList)

    @Number(1.3)
    @Weight(.34)
    def test_sample_exeuction_3(self):
        """Sample Execution #3"""

        inputList = ["materialList.txt", "mat1.txt"]
        expectedList = [
            "Beck site in Golden has 19 materials, with a value of 549.",
            "Wood:7 Steel:6 Brick:6",
            "Bloom site in Arvada has 333 materials, with a value of 164160.",
            "Wood:105 Steel:119 Brick:109",
            "Beck site in Golden has 352 materials, with a value of 164709."
        ]

        self.assertStdIO(inputList, expectedList)

    # Tests 2.x are class tests, see 'test_public_materials.py' & 'test_public_construction_site.py'

    @Number(3.1)
    @Weight(1)
    def test_sites_blue_and_shine(self):
        """Sites: Blue & Shine"""

        inputList = ["blue_puno.txt", "shine_seattle.txt"]
        expectedList = [
            "Blue site in Puno has 5500 materials, with a value of 2755541.",
            "Wood:1842 Steel:1847 Brick:1811",
            "Shine site in Seattle has 250 materials, with a value of 128611.",
            "Wood:86 Steel:80 Brick:84",
            "Blue site in Puno has 5750 materials, with a value of 2884152."
        ]

        self.assertStdIO(inputList, expectedList)

    @Number(3.2)
    @Weight(1)
    def test_sites_dazzle_and_cozy(self):
        """Sites: Dazzle & Cozy"""

        inputList = ["dazzle_taiki.txt", "cozy_juneau.txt"]
        expectedList = [
            "Dazzle site in Taiki has 3335 materials, with a value of 1663673.",
            "Wood:1039 Steel:1116 Brick:1180",
            "Cozy site in Juneau has 1200 materials, with a value of 606240.",
            "Wood:397 Steel:401 Brick:402",
            "Dazzle site in Taiki has 4535 materials, with a value of 2269913."
        ]

        self.assertStdIO(inputList, expectedList)

    @Number(3.3)
    @Weight(1)
    def test_sites_starry_and_northpoint(self):
        """Sites: Starry & Northpoint"""

        inputList = ["starry_pattaya.txt", "northpoint_drammen.txt"]
        expectedList = [
            "Starry site in Pattaya has 539 materials, with a value of 270765.",
            "Wood:165 Steel:205 Brick:169",
            "Northpoint site in Drammen has 25 materials, with a value of 10791.",
            "Wood:6 Steel:6 Brick:13",
            "Starry site in Pattaya has 564 materials, with a value of 281556."
        ]

        self.assertStdIO(inputList, expectedList)

    @Number(3.4)
    @Weight(1)
    def test_sites_cozy_and_dazzle(self):
        """Sites: Cozy & Dazzle"""

        inputList = ["cozy_juneau.txt", "dazzle_taiki.txt"]
        expectedList = [
            "Cozy site in Juneau has 1200 materials, with a value of 606240.",
            "Wood:397 Steel:401 Brick:402",
            "Dazzle site in Taiki has 3335 materials, with a value of 1663673.",
            "Wood:1039 Steel:1116 Brick:1180",
            "Cozy site in Juneau has 4535 materials, with a value of 2269913."
        ]

        self.assertStdIO(inputList, expectedList)

    @Number(3.5)
    @Weight(1)
    def test_sites_starry_and_blue(self):
        """Sites: Starry & Blue"""

        inputList = ["starry_pattaya.txt", "blue_puno.txt"]
        expectedList = [
            "Starry site in Pattaya has 539 materials, with a value of 270765.",
            "Wood:165 Steel:205 Brick:169",
            "Blue site in Puno has 5500 materials, with a value of 2755541.",
            "Wood:1842 Steel:1847 Brick:1811",
            "Starry site in Pattaya has 6039 materials, with a value of 3026306."
        ]

        self.assertStdIO(inputList, expectedList)
'''
    @Number(3.6)
    @Weight(1)
    def test_sites_northpoint_and_cozy(self):
        """Sites: Northpoint & Cozy"""

        inputList = ["northpoint_drammen.txt", "cozy_juneau.txt"]
        expectedList = [
            "Northpoint site in Drammen has 25 materials, with a value of 10791.",
            "Wood:6 Steel:6 Brick:13",
            "Cozy site in Juneau has 1200 materials, with a value of 606240.",
            "Wood:397 Steel:401 Brick:402",
            "Northpoint site in Drammen has 1225 materials, with a value of 617031."
        ]

        self.assertStdIO(inputList, expectedList)

    @Number(3.7)
    @Weight(1)
    def test_sites_shine_and_blue(self):
        """Sites: Shine & Blue"""

        inputList = ["shine_seattle.txt", "blue_puno.txt"]
        expectedList = [
            "Shine site in Seattle has 250 materials, with a value of 128611.",
            "Wood:86 Steel:80 Brick:84",
            "Blue site in Puno has 5500 materials, with a value of 2755541.",
            "Wood:1842 Steel:1847 Brick:1811",
            "Shine site in Seattle has 5750 materials, with a value of 2884152."
        ]

        self.assertStdIO(inputList, expectedList)

    @Number(3.8)
    @Weight(1)
    def test_sites_dazzle_and_northpoint(self):
        """Sites: Dazzle & Northpoint"""

        inputList = ["dazzle_taiki.txt", "northpoint_drammen.txt"]
        expectedList = [
            "Dazzle site in Taiki has 3335 materials, with a value of 1663673.",
            "Wood:1039 Steel:1116 Brick:1180",
            "Northpoint site in Drammen has 25 materials, with a value of 10791.",
            "Wood:6 Steel:6 Brick:13",
            "Dazzle site in Taiki has 3360 materials, with a value of 1674464."
        ]

        self.assertStdIO(inputList, expectedList)

    @Number(3.9)
    @Weight(1)
    def test_sites_starry_and_shine(self):
        """Sites: Starry & Shine"""

        inputList = ["starry_pattaya.txt", "shine_seattle.txt"]
        expectedList = [
            "Starry site in Pattaya has 539 materials, with a value of 270765.",
            "Wood:165 Steel:205 Brick:169",
            "Shine site in Seattle has 250 materials, with a value of 128611.",
            "Wood:86 Steel:80 Brick:84",
            "Starry site in Pattaya has 789 materials, with a value of 399376."
        ]

        self.assertStdIO(inputList, expectedList)
'''