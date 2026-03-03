from autograder_utils.Decorators import Weight, Number
from StudentSubmissionImpl.Python.Runners import PythonRunnerBuilder
from test_public_common import TestCommon
from Executors.Executor import Executor
from Executors.Environment import getResults
import test_public_grids
import os

class ImageCompressionPublicTests(TestCommon):
    def assertFunctionReturn(self, funcName: str, parameters: list, expectedReturn: list):
        environment = self.environmentBuilder.build()

        self.runnerBuilder.setEntrypoint(function=funcName)
        [self.runnerBuilder.addParameter(param) for param in parameters]
        runner = self.runnerBuilder.build()

        Executor.execute(environment, runner)
        actualReturns = getResults(environment).return_val
        
        self.assertListEqual(expectedReturn, actualReturns)

    def assertProgramExecution(self, inputs: list, expectedValues: list):
        # Assert Stdio
        environment = self.environmentBuilder \
            .addFile(f"./{inputs[0]}", f"./{inputs[0]}") \
            .setStdin(inputs) \
            .build()
        
        programRunner = self.runnerBuilder \
            .setEntrypoint(module=True) \
            .build()

        Executor.execute(environment, programRunner)
        actualStdout = getResults(environment).stdout

        self.assertCorrectNumberOfOutputLines(expectedValues[0], actualStdout)
        [self.assertEqual(expectedValues[0][i], actualStdout[i]) for i in range(len(expectedValues[0]))]

        # Assert File Exists
        outputFiles = getResults(environment).file_out.files
        try:
            self.assertTrue(os.path.isfile(outputFiles[f"compressed_{inputs[0]}"]))
        except KeyError:
            raise AssertionError("Compressed image file was not found. Make sure it is outputted & named correctly.")

        # Assert `output_image` Called Properly
        grid = self.image_to_list(f"student_tests/data/public/{inputs[0]}")
        CIRparameters = [grid, 0, 0, len(grid[0]), len(grid), int(inputs[1])]
        
        compressImageRunnerBuilder = PythonRunnerBuilder(self.studentSubmission) \
            .setEntrypoint(function="compress_image")
        [compressImageRunnerBuilder.addParameter(param) for param in CIRparameters]
        compressImageRunner = compressImageRunnerBuilder.build()

        Executor.execute(environment, compressImageRunner)
        actualCompressedGrid = getResults(environment).return_val

        for idx1, depthOne in enumerate(expectedValues[1]):
            for idx2, depthTwo in enumerate(depthOne):
                for idx3, depthThree in enumerate(depthTwo):
                    self.assertAlmostEquals(depthThree, actualCompressedGrid[idx1][idx2][idx3], delta=10)


    @Number(1.1)
    @Weight(.33)
    def test_flowersOne_five(self):
        """Flowers #1 - Threshold: 5"""

        imageFilename = "flowers_1.jpg"
        threshold = "5"

        expectedStdout = ["Width: 640", "Height: 640", "Threshold: 5"]
        expectedGrid = test_public_grids.getOneOneGrid()

        self.assertProgramExecution([imageFilename, threshold], [expectedStdout, expectedGrid])

    @Number(1.2)
    @Weight(.33)
    def test_flowersOne_ten(self):
        """Flowers #1 - Threshold: 10"""

        imageFilename = "flowers_1.jpg"
        threshold = "10"

        expectedStdout = ["Width: 640", "Height: 640", "Threshold: 10"]
        expectedGrid = test_public_grids.getOneTwoGrid()

        self.assertProgramExecution([imageFilename, threshold], [expectedStdout, expectedGrid])

    @Number(1.3)
    @Weight(.34)
    def test_flowersOne_twoHundred(self):
        """Flowers #1 - Threshold: 200"""

        imageFilename = "flowers_1.jpg"
        threshold = "200"

        expectedStdout = ["Width: 640", "Height: 640", "Threshold: 200"]
        expectedGrid = test_public_grids.getOneThreeGrid()

        self.assertProgramExecution([imageFilename, threshold], [expectedStdout, expectedGrid])

    @Number(2.1)
    @Weight(.5)
    def test_blockAverage_exampleUsage(self):
        """`block_average` - Example Usage"""

        grid = [
            [[73, 70, 70], [82, 78, 79], [82, 78, 79], [86, 82, 83]],
            [[78, 75, 75], [81, 78, 78], [80, 76, 77], [82, 77, 79]],
            [[77, 76, 74], [77, 74, 74], [78, 75, 75], [79, 74, 76]],
            [[76, 75, 73], [77, 76, 74], [78, 75, 75], [81, 76, 77]],
        ]
        x = 0
        y = 0
        width = 2
        height = 2

        expectedReturn = [78, 75, 75]

        self.assertFunctionReturn("block_average", [grid, x, y, width, height], expectedReturn)

    @Number(2.2)
    @Weight(.5)
    def test_createCompressedBlock_exampleUsage(self):
        """`create_compressed_block` - Example Usage"""

        avg_color = [78, 75, 75]
        width = 2
        height = 2

        expectedReturn = [
            [[78, 75, 75], [78, 75, 75]],
            [[78, 75, 75], [78, 75, 75]]
        ]

        self.assertFunctionReturn("create_compressed_block", [avg_color, width, height], expectedReturn)

    @Number(2.3)
    @Weight(.5)
    def test_mergeLists_exampleUsage(self):
        """`merge_lists` - Example Usage"""

        lst1 = [
            [1, 2], [3, 4]
        ]
        lst2 = [
            [5, 6, 7], [8, 9, 10]
        ]

        expectedReturn = [
            [1, 2, 5, 6, 7], [3, 4, 8, 9, 10]
        ]

        self.assertFunctionReturn("merge_lists", [lst1, lst2], expectedReturn)

    @Number(2.4)
    @Weight(.5)
    def test_compressImage_exampleUsage(self):
        """`compress_image` - Example Usage"""

        grid = [
            [[73, 70, 70], [82, 78, 79], [82, 78, 79], [86, 82, 83]],
            [[78, 75, 75], [81, 78, 78], [80, 76, 77], [82, 77, 79]],
            [[77, 76, 74], [77, 74, 74], [78, 75, 75], [79, 74, 76]],
            [[76, 75, 73], [77, 76, 74], [78, 75, 75], [81, 76, 77]],
        ]
        x = 0
        y = 0
        width = 4
        height = 4
        threshold = 2

        expectedReturn = [
            [[78, 75, 75], [78, 75, 75], [82, 78, 79], [82, 78, 79]],
            [[78, 75, 75], [78, 75, 75], [82, 78, 79], [82, 78, 79]],
            [[76, 75, 73], [76, 75, 73], [79, 75, 75], [79, 75, 75]],
            [[76, 75, 73], [76, 75, 73], [79, 75, 75], [79, 75, 75]]
        ]

        self.assertFunctionReturn("compress_image", [grid, x, y, width, height, threshold], expectedReturn)

    @Number(3.1)
    @Weight(.5)
    def test_blockAverage_singlePixel(self):
        """`block_average` - Single Pixel"""

        grid = [
            [[128, 128, 128]],
        ]
        x = 0
        y = 0
        width = 1
        height = 1

        expectedReturn = [128, 128, 128]

        self.assertFunctionReturn("block_average", [grid, x, y, width, height], expectedReturn)

    @Number(3.2)
    @Weight(.5)
    def test_blockAverage_smallGrid(self):
        """`block_average` - Small Grid"""

        grid = [
            [[0, 0, 0], [85, 85, 85]],
            [[170, 170, 170], [255, 255, 255]]
        ]
        x = 0
        y = 0
        width = 2
        height = 2

        expectedReturn = [127, 127, 127]

        self.assertFunctionReturn("block_average", [grid, x, y, width, height], expectedReturn)

    @Number(3.3)
    @Weight(.5)
    def test_createCompressedBlock_singlePixel(self):
        """`create_compressed_block` - Single Pixel"""

        avg_color = [64, 128, 192]
        width = 1
        height = 1

        expectedReturn = [
            [[64, 128, 192]]
        ]

        self.assertFunctionReturn("create_compressed_block", [avg_color, width, height], expectedReturn)

    @Number(3.4)
    @Weight(.5)
    def test_createCompressedBlock_tenByTen(self):
        """`create_compressed_block` - Large Expansion"""

        avg_color = [0, 127, 255]
        width = 10
        height = 10

        expectedReturn = [
            [[0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255]],
            [[0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255]],
            [[0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255]],
            [[0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255]],
            [[0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255]],
            [[0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255]],
            [[0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255]],
            [[0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255]],
            [[0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255]],
            [[0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255], [0, 127, 255]]
        ]

        self.assertFunctionReturn("create_compressed_block", [avg_color, width, height], expectedReturn)

    @Number(3.5)
    @Weight(.5)
    def test_mergeLists_firstListLarger(self):
        """`merge_lists` - First List Larger"""

        lst1 = [
            [1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]
        ]
        lst2 = [
            [16, 17], [18, 19], [20, 21]
        ]

        expectedReturn = [
            [1, 2, 3, 4, 5, 16, 17], [6, 7, 8, 9, 10, 18, 19], [11, 12, 13, 14, 15, 20, 21]
        ]

        self.assertFunctionReturn("merge_lists", [lst1, lst2], expectedReturn)

    @Number(3.6)
    @Weight(.5)
    def test_mergeLists_firstListEmpty(self):
        """`merge_lists` - First List Empty"""

        lst1 = [
            [], [], []
        ]
        lst2 = [
            [5, 17, 12], [18, 3, 0], [9, 20, 133]
        ]

        expectedReturn = [
            [5, 17, 12], [18, 3, 0], [9, 20, 133]
        ]

        self.assertFunctionReturn("merge_lists", [lst1, lst2], expectedReturn)

    @Number(3.7)
    @Weight(.5)
    def test_compressImage_singlePixel(self):
        """`compress_image` - Single Pixel"""

        grid = [
            [[37, 99, 218]]
        ]
        x = 0
        y = 0
        width = 1
        height = 1
        threshold = 25

        expectedReturn = [
            [[37, 99, 218]]
        ]

        self.assertFunctionReturn("compress_image", [grid, x, y, width, height, threshold], expectedReturn)
 
    @Number(3.8)
    @Weight(.5)
    def test_compressImage_fiveByFive(self):
        """`compress_image` - Larger Compression"""

        grid = [
            [[37, 99, 218], [250, 16, 77], [50, 128, 120], [111, 196, 224], [67, 67, 242]],
            [[250, 16, 77], [50, 128, 120], [111, 196, 224], [67, 67, 242], [37, 99, 218]],
            [[50, 128, 120], [111, 196, 224], [67, 67, 242], [37, 99, 218], [250, 16, 77]],
            [[111, 196, 224], [67, 67, 242], [37, 99, 218], [250, 16, 77], [50, 128, 120]],
            [[67, 67, 242], [37, 99, 218], [250, 16, 77], [50, 128, 120], [111, 196, 224]]
        ]
        x = 0
        y = 0
        width = 4
        height = 4
        threshold = 1

        expectedReturn = [
            [[37, 99, 218], [250, 16, 77], [50, 128, 120], [111, 196, 224]],
            [[250, 16, 77], [50, 128, 120], [111, 196, 224], [67, 67, 242]],
            [[50, 128, 120], [111, 196, 224], [67, 67, 242], [37, 99, 218]],
            [[111, 196, 224], [67, 67, 242], [37, 99, 218], [250, 16, 77]]
        ]

        self.assertFunctionReturn("compress_image", [grid, x, y, width, height, threshold], expectedReturn)
 
    @Number(4.1)
    @Weight(1)
    def test_flowersThree_ten(self):
        """Flowers #3 - Threshold: 10"""

        imageFilename = "flowers_3.jpg"
        threshold = "10"

        expectedStdout = ["Width: 640", "Height: 640", "Threshold: 10"]
        expectedGrid = test_public_grids.getFourOneGrid()

        self.assertProgramExecution([imageFilename, threshold], [expectedStdout, expectedGrid])


    @Number(4.2)
    @Weight(1)
    def test_flowersThree_oneHundred(self):
        """Flowers #3 - Threshold: 100"""

        imageFilename = "flowers_3.jpg"
        threshold = "100"

        expectedStdout = ["Width: 640", "Height: 640", "Threshold: 100"]
        expectedGrid = test_public_grids.getFourTwoGrid()

        self.assertProgramExecution([imageFilename, threshold], [expectedStdout, expectedGrid])

    @Number(4.3)
    @Weight(1)
    def test_flowersTwo_twentyFive(self):
        """Flowers #2 - Threshold: 25"""

        imageFilename = "flowers_2.jpg"
        threshold = "25"

        expectedStdout = ["Width: 640", "Height: 640", "Threshold: 25"]
        expectedGrid = test_public_grids.getFourThreeGrid()

        self.assertProgramExecution([imageFilename, threshold], [expectedStdout, expectedGrid])
