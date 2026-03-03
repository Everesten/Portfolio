import os
from StudentSubmission.common import ValidationHook
from StudentSubmissionImpl.Python.common import FileTypeMap
from StudentSubmissionImpl.Python.PythonSubmission import PythonSubmission
from StudentSubmission.AbstractValidator import AbstractValidator
from utils.config.Config import AutograderConfigurationProvider
from TestingFramework.Assertions import Assertions
from StudentSubmissionImpl.Python.PythonFileImportFactory import PythonFileImportFactory

class HelperModuleValidator(AbstractValidator):
    @staticmethod
    def getValidationHook() -> ValidationHook:
        return ValidationHook.POST_LOAD

    def __init__(self):
        super().__init__()
        self.files = []

    def setup(self, studentSubmission):
        self.files = studentSubmission.getDiscoveredFileMap()[FileTypeMap.PYTHON_FILES]

    def run(self):
        return

class TestCommon(Assertions):
    @classmethod
    def setUpClass(cls) -> None:
        cls.autograderConfig = AutograderConfigurationProvider.get()

        cls.studentSubmission = PythonSubmission() \
            .addValidator(HelperModuleValidator()) \
            .setSubmissionRoot(cls.autograderConfig.config.student_submission_directory) \
            .enableRequirements() \
            .addPackage("matplotlib") \
            .load() \
            .build() \
            .validate()
        
        for file in cls.studentSubmission.getDiscoveredFileMap()[FileTypeMap.PYTHON_FILES]:
            modName = os.path.basename(file)[:-3]

            PythonFileImportFactory.registerFile(os.path.abspath(file), modName)

        cls.importHandler = PythonFileImportFactory.buildImport()