import shutil
import os

from Executors.Environment import ExecutionEnvironment

from StudentSubmission.SubmissionProcessFactory import SubmissionProcessFactory
from Tasks.TaskRunner import TaskRunner
from utils.config.Config import AutograderConfigurationProvider, AutograderConfiguration

# For typing only
from StudentSubmission.ISubmissionProcess import ISubmissionProcess


class Executor:
    @classmethod
    def setup(cls, environment: ExecutionEnvironment, runner: TaskRunner, autograderConfig: AutograderConfiguration) -> ISubmissionProcess:
        if not os.path.exists(f"{environment.SANDBOX_LOCATION}"):
            raise EnvironmentError(f"Failed to locate sandbox at '{environment.SANDBOX_LOCATION}'")

        process = SubmissionProcessFactory.createProcess(environment, runner, autograderConfig)

        if environment.files:
            for src, dest in environment.files.items():
                if os.path.basename(src) not in os.listdir(environment.SANDBOX_LOCATION):
                    raise EnvironmentError(f"Required file not located in '{environment.SANDBOX_LOCATION}'. Expected {os.path.basename(src)}.")

        return process
        
    @classmethod
    def execute(cls, environment: ExecutionEnvironment, runner: TaskRunner, raiseExceptions: bool = True) -> None:
        submissionProcess: ISubmissionProcess = cls.setup(environment, runner, AutograderConfigurationProvider.get())

        submissionProcess.run()

        cls.postRun(environment, submissionProcess, raiseExceptions)

    @classmethod
    def postRun(cls, environment: ExecutionEnvironment, 
                submissionProcess: ISubmissionProcess, raiseExceptions: bool) -> None:

        submissionProcess.cleanup()

        submissionProcess.populateResults(environment)

        if raiseExceptions:
            # Moving this into the actual submission process allows for each process type to
            # handle their exceptions differently
            submissionProcess.processAndRaiseExceptions(environment)


    @classmethod
    def cleanup(cls, environment: ExecutionEnvironment):
        raise Exception("Clean up has been disabled")
        # if os.path.exists(environment.SANDBOX_LOCATION):
        #     shutil.rmtree(environment.SANDBOX_LOCATION)
