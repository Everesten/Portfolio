from StudentSubmissionImpl.Python.PythonSubmission import PythonSubmission
from utils.config.Config import AutograderConfigurationProvider
from TestingFramework.Assertions import Assertions


class TestCommon(Assertions):
    @classmethod
    def setUpClass(cls) -> None:
        cls.autograderConfig = AutograderConfigurationProvider.get()

        cls.studentSubmission = PythonSubmission()\
            .setSubmissionRoot(cls.autograderConfig.config.student_submission_directory)\
            .load()\
            .build()\
            .validate()
