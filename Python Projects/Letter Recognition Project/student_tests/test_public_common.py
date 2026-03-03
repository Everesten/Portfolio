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
        for file in self.files:
            if os.path.basename(file) == "helper_library.py":
                return

        self.addError(EnvironmentError("`helper_library.py` not found in student submission!\n"\
                                       "Please ensure that it is in the `student_work` folder (if running locally) or was included in your Gradescope upload (if running on gradescope)!"))

class TestCommon(Assertions):
    @classmethod
    def setUpClass(cls) -> None:
        cls.autograderConfig = AutograderConfigurationProvider.get()

        cls.studentSubmission = PythonSubmission()\
            .addValidator(HelperModuleValidator())\
            .setSubmissionRoot(cls.autograderConfig.config.student_submission_directory)\
            .load()\
            .build()\
            .validate()

        for file in cls.studentSubmission.getDiscoveredFileMap()[FileTypeMap.PYTHON_FILES]:
            modName = os.path.basename(file)[:-3]
            
            PythonFileImportFactory.registerFile(os.path.abspath(file), modName)

        cls.importHandler = PythonFileImportFactory.buildImport()

        cls.letterGrids = [
            [[1, 1, 0, 1, 1], [1, 0, 1, 0, 1], [1, 0, 0, 0, 1], [1, 0, 1, 0, 1], [1, 0, 1, 0, 1]],
            [[1, 0, 0, 0, 1], [1, 0, 1, 1, 0], [1, 0, 0, 0, 1], [1, 0, 1, 1, 0], [1, 0, 0, 0, 1]],
            [[1, 0, 0, 0, 1], [0, 1, 1, 1, 1], [0, 1, 1, 1, 1], [0, 1, 1, 1, 1], [1, 0, 0, 0, 1]],
            [[1, 0, 0, 0, 1], [1, 0, 1, 1, 0], [1, 0, 1, 1, 0], [1, 0, 1, 1, 0], [1, 0, 0, 0, 1]],
            [[1, 0, 0, 0, 0], [1, 0, 1, 1, 1], [1, 0, 0, 0, 0], [1, 0, 1, 1, 1], [1, 0, 0, 0, 0]],
            [[1, 0, 0, 0, 0], [1, 0, 1, 1, 1], [1, 0, 0, 1, 1], [1, 0, 1, 1, 1], [1, 0, 1, 1, 1]],
            [[1, 0, 0, 0, 1], [0, 1, 1, 1, 1], [0, 1, 1, 0, 0], [0, 1, 1, 1, 0], [1, 0, 0, 0, 1]],
            [[1, 0, 1, 0, 1], [1, 0, 1, 0, 1], [1, 0, 0, 0, 1], [1, 0, 1, 0, 1], [1, 0, 1, 0, 1]],
            [[1, 0, 0, 0, 1], [1, 1, 0, 1, 1], [1, 1, 0, 1, 1], [1, 1, 0, 1, 1], [1, 0, 0, 0, 1]],
            [[1, 0, 0, 0, 1], [1, 1, 1, 0, 1], [1, 1, 1, 0, 1], [1, 0, 1, 0, 1], [1, 1, 0, 1, 1]],
            [[1, 0, 1, 1, 0], [1, 0, 1, 0, 1], [1, 0, 0, 1, 1], [1, 0, 1, 0, 1], [1, 0, 1, 1, 0]],
            [[1, 0, 1, 1, 1], [1, 0, 1, 1, 1], [1, 0, 1, 1, 1], [1, 0, 1, 1, 1], [1, 0, 0, 0, 1]],
            [[1, 0, 1, 0, 1], [0, 1, 0, 1, 0], [0, 1, 1, 1, 0], [0, 1, 1, 1, 0], [0, 1, 1, 1, 0]],
            [[0, 1, 1, 1, 0], [0, 0, 1, 1, 0], [0, 1, 0, 1, 0], [0, 1, 1, 0, 0], [0, 1, 1, 1, 0]],
            [[1, 0, 0, 0, 1], [0, 1, 1, 1, 0], [0, 1, 1, 1, 0], [0, 1, 1, 1, 0], [1, 0, 0, 0, 1]],
            [[1, 0, 0, 0, 1], [1, 0, 1, 1, 0], [1, 0, 0, 0, 1], [1, 0, 1, 1, 1], [1, 0, 1, 1, 1]],
            [[1, 0, 0, 0, 1], [0, 1, 1, 1, 0], [0, 1, 1, 1, 0], [1, 0, 0, 0, 1], [1, 1, 1, 1, 0]],
            [[0, 0, 0, 1, 1], [0, 1, 1, 0, 1], [0, 0, 0, 1, 1], [0, 1, 0, 1, 1], [0, 1, 1, 0, 1]],
            [[1, 0, 0, 0, 0], [0, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 1, 1, 1, 0], [0, 0, 0, 0, 1]],
            [[0, 0, 0, 0, 0], [1, 1, 0, 1, 1], [1, 1, 0, 1, 1], [1, 1, 0, 1, 1], [1, 1, 0, 1, 1]],
            [[0, 1, 1, 1, 0], [0, 1, 1, 1, 0], [0, 1, 1, 1, 0], [0, 1, 1, 1, 0], [1, 0, 0, 0, 1]],
            [[0, 1, 1, 1, 0], [0, 1, 1, 1, 0], [1, 0, 1, 0, 1], [1, 0, 1, 0, 1], [1, 1, 0, 1, 1]],
            [[0, 1, 1, 1, 0], [0, 1, 1, 1, 0], [0, 1, 1, 1, 0], [0, 1, 0, 1, 0], [1, 0, 1, 0, 1]],
            [[0, 1, 1, 1, 0], [1, 0, 1, 0, 1], [1, 1, 0, 1, 1], [1, 0, 1, 0, 1], [0, 1, 1, 1, 0]],
            [[0, 1, 1, 1, 0], [1, 0, 1, 0, 1], [1, 1, 0, 1, 1], [1, 1, 0, 1, 1], [1, 1, 0, 1, 1]],
            [[0, 0, 0, 0, 0], [1, 1, 1, 0, 1], [1, 1, 0, 1, 1], [1, 0, 1, 1, 1], [0, 0, 0, 0, 0]]
        ]
        cls.letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

