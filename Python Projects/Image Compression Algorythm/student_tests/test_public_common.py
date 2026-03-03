import os
import sys
from typing import Dict, List

from Executors.Environment import ExecutionEnvironmentBuilder
from Executors.Executor import Executor
from StudentSubmissionImpl.Python import PythonEnvironment
from StudentSubmissionImpl.Python.PythonEnvironment import PythonResults, PythonEnvironmentBuilder
from StudentSubmissionImpl.Python.Runners import PythonRunnerBuilder
from StudentSubmissionImpl.Python.common import FileTypeMap
from StudentSubmissionImpl.Python.PythonSubmission import PythonSubmission
from TestingFramework.SingleFunctionMock import SingleFunctionMock
from utils.config.Config import AutograderConfigurationProvider
from TestingFramework.Assertions import Assertions
from StudentSubmissionImpl.Python.PythonFileImportFactory import PythonFileImportFactory
from test_public_validators import RecursionValidator, HelperModuleValidator


class TestCommon(Assertions):
    @classmethod
    def setUpClass(cls) -> None:
        cls.autograderConfig = AutograderConfigurationProvider.get()

        cls.studentSubmission = PythonSubmission() \
            .addValidator(HelperModuleValidator()) \
            .addValidator(RecursionValidator(["compress_image"])) \
            .setSubmissionRoot(cls.autograderConfig.config.student_submission_directory) \
            .enableRequirements() \
            .addPackage("pillow") \
            .addPackage("numpy") \
            .load() \
            .build() \
            .validate()

        for file in cls.studentSubmission.getDiscoveredFileMap()[FileTypeMap.PYTHON_FILES]:
            if os.path.basename(file) in cls.studentSubmission.ALLOWED_STRICT_MAIN_NAMES:
                continue

            modName = os.path.basename(file)[:-3]

            PythonFileImportFactory.registerFile(os.path.abspath(file), modName)

        cls.importHandler = PythonFileImportFactory.buildImport()

    def setUp(self):
        if self.importHandler is None:
            raise AssertionError("Invalid State: ImportLoader is NONE. Should never be none!")

        self.environmentBuilder = ExecutionEnvironmentBuilder[PythonEnvironment, PythonResults]() \
            .setTimeout(1000) \
            .setImplEnvironment(
            PythonEnvironmentBuilder, lambda x: x \
                .addImportHandler(self.importHandler) \
                .build()
        ) \
            .setDataRoot(self.autograderConfig.build.data_files_source)

        self.runnerBuilder = PythonRunnerBuilder(self.studentSubmission)


    def image_to_list(self, image_file):
        # delay loading of PIL til the autograder installs it
        from PIL import Image

        image = Image.open(image_file)

        # Check for RGB here
        if image.mode != 'RGB':
            image = image.convert('RGB')

        pixel_array = []
        pixels = image.load()

        # Dimensions
        width, height = image.size
    
        for j in range(height):
            row = []
            for i in range(width):
                row.append(pixels[i,j])
            pixel_array.append(row)
        return pixel_array
