from autograder_utils.Decorators import Weight, Number

from test_public_common import TestCommon
from Executors.Executor import Executor
from Executors.Environment import ExecutionEnvironmentBuilder, getResults
from StudentSubmissionImpl.Python.Runners import PythonRunnerBuilder
from StudentSubmissionImpl.Python.PythonEnvironment import PythonEnvironmentBuilder
from TestingFramework.SingleFunctionMock import SingleFunctionMock
from StudentSubmissionImpl.Python.PythonEnvironment import PythonEnvironment
from StudentSubmissionImpl.Python.PythonSubmissionProcess import PythonResults

class DNAInformationPlottingPublicTests(TestCommon):
    def setUp(self) -> None:
        self.mockStrs = ["title", "xlabel", "ylabel", "savefig", "hist", "scatter", "plot", "legend"]
        mocks = [SingleFunctionMock(str, spy=True) for str in self.mockStrs]
        self.mockDict = dict(zip(self.mockStrs, mocks))
        
        self.environmentBuilder = ExecutionEnvironmentBuilder[PythonEnvironment, PythonResults]() \
            .setTimeout(10) \
            .setImplEnvironment(
                PythonEnvironmentBuilder, lambda x: x \
                .addImportHandler(self.importHandler) \
                .addModuleMock("matplotlib.pyplot", {"matplotlib.pyplot.title": self.mockDict["title"]}) \
                .addModuleMock("matplotlib.pyplot", {"matplotlib.pyplot.xlabel": self.mockDict["xlabel"]}) \
                .addModuleMock("matplotlib.pyplot", {"matplotlib.pyplot.ylabel": self.mockDict["ylabel"]}) \
                .addModuleMock("matplotlib.pyplot", {"matplotlib.pyplot.savefig": self.mockDict["savefig"]}) \
                .addModuleMock("matplotlib.pyplot", {"matplotlib.pyplot.hist": self.mockDict["hist"]}) \
                .addModuleMock("matplotlib.pyplot", {"matplotlib.pyplot.scatter": self.mockDict["scatter"]}) \
                .addModuleMock("matplotlib.pyplot", {"matplotlib.pyplot.plot": self.mockDict["plot"]}) \
                .addModuleMock("matplotlib.pyplot", {"matplotlib.pyplot.legend": self.mockDict["legend"]}) \
                .build()
            ) \
            .setDataRoot(self.autograderConfig.build.data_files_source)
        
        self.runnerBuilder = PythonRunnerBuilder(self.studentSubmission)
        [self.runnerBuilder.subscribeToMock(f"matplotlib.pyplot.{str}") for str in self.mockStrs]

    def assertAminoHistogramFunc(self, parameters):
        environment = self.environmentBuilder.build()
    
        if environment.impl_environment is None:
            print("Failed impl_environment")

        self.runnerBuilder.setEntrypoint(function="create_amino_histogram")
        [self.runnerBuilder.addParameter(param) for param in parameters]
        runner = self.runnerBuilder.build()
        
        Executor.execute(environment, runner)
        expectedParameters = [parameters[1], "Histogram of Amino Acids", "Amino Acid Abbreviations", "Counts", parameters[0]]

        mockStrsIdxs = [4, 0, 1, 2, 3]
        mockResults = [getResults(environment).impl_results.mocks[f"matplotlib.pyplot.{self.mockStrs[idx]}"] for idx in mockStrsIdxs]

        for idx, mockResult in enumerate(mockResults):
            mockResult.assertCalledAtLeastTimes(1)
            mockResult.assertCalledWith(expectedParameters[idx])

    def assertGCScatterFunc(self, parameters):
        environment = self.environmentBuilder.build()

        if environment.impl_environment is None:
            print("Failed impl_environment")

        self.runnerBuilder.setEntrypoint(function="create_GC_scatter")
        [self.runnerBuilder.addParameter(param) for param in parameters]
        runner = self.runnerBuilder.build()
        
        Executor.execute(environment, runner)
        expectedParameters = [[parameters[1], parameters[2]], "Scatterplot of Sequence Length vs GC Content", "GC Content Ratio", "Sequence Length", parameters[0]]

        mockStrsIdxs = [5, 0, 1, 2, 3]
        mockResults = [getResults(environment).impl_results.mocks[f"matplotlib.pyplot.{self.mockStrs[idx]}"] for idx in mockStrsIdxs]

        for idx, mockResult in enumerate(mockResults):
            mockResult.assertCalledAtLeastTimes(1)
            if (idx == 0):
                mockResult.assertCalledWith(expectedParameters[idx][0], expectedParameters[idx][1])
            else:
                mockResult.assertCalledWith(expectedParameters[idx])

    def assertCreateBaseLineplotFunc(self, parameters):
        environment = self.environmentBuilder.build()

        if environment.impl_environment is None:
            print("Failed impl_environment")

        self.runnerBuilder.setEntrypoint(function="create_base_lineplot")
        [self.runnerBuilder.addParameter(param) for param in parameters]
        runner = self.runnerBuilder.build()
        
        Executor.execute(environment, runner)
        
        sequence = parameters[1]
        seqRange = range(1, len(sequence) + 1)

        ratios = {'A': [], 'T': [], 'G': [], 'C': []}
        [{ratios[let].append(sequence[:(idx + 1)].count(let) / (idx + 1)) for let in ratios.keys()} for idx in range(len(sequence))]

        expectedParameters = [
            [
                [seqRange, ratios['A'], 'A'], [seqRange, ratios['T'], 'T'], [seqRange, ratios['G'], 'G'], [seqRange, ratios['C'], 'C'],
            ], 
            "best", "Line Plot of Base Ratios", "Location in Sequence", "Ratio Per Base", parameters[0]]

        mockStrsIdxs = [6, 7, 0, 1, 2, 3]
        mockResults = [getResults(environment).impl_results.mocks[f"matplotlib.pyplot.{self.mockStrs[idx]}"] for idx in mockStrsIdxs]

        for idx, mockResult in enumerate(mockResults):
            if (idx == 0):
                mockResult.assertCalledAtLeastTimes(4)
                [mockResult.assertCalledWith(expectedParameters[0][i][0], expectedParameters[0][i][1], label=expectedParameters[0][i][2]) for i in range(4)]
            else:
                mockResult.assertCalledAtLeastTimes(1)
                if (idx == 1):
                    mockResult.assertCalledWith(loc=expectedParameters[1])
                else:
                    mockResult.assertCalledWith(expectedParameters[idx])

    def assertProgramExecution(self, inputs):
        environment = self.environmentBuilder \
            .addFile(f"{inputs[0]}", f"./{inputs[0]}") \
            .addFile(f"public/{inputs[1]}", f"./{inputs[1]}") \
            .setStdin(inputs) \
            .build()

        if environment.impl_environment is None:
            print("Failed impl_environment")
            return -1
        
        parseFileIntoAcidsRunner = PythonRunnerBuilder(self.studentSubmission) \
            .setEntrypoint(function="parse_file_into_acids") \
            .addParameter(inputs[0]) \
            .build()
        Executor.execute(environment, parseFileIntoAcidsRunner)
        acids = getResults(environment).return_val
        
        with open(f"student_tests/data/public/{inputs[1]}", 'r') as seqFile:
            sequences = [seq.strip() for seq in seqFile if (seq != "DONE")]

        if (inputs[2] == '1'):
            codons = []
            stops = ["UAA", "UGA", "UAG"]
            for dnaSeq in sequences:
                dnaToRnaRunner = PythonRunnerBuilder(self.studentSubmission) \
                    .setEntrypoint(function="dna_to_rna") \
                    .addParameter(dnaSeq) \
                    .build()
                Executor.execute(environment, dnaToRnaRunner)
                rnaSeq = getResults(environment).return_val

                out = ""
                start = rnaSeq.find("AUG")
                while rnaSeq[start:start+3] not in stops:
                    out += ''.join([row[2] for row in acids if (row[0] == rnaSeq)])
                    start += 3
                codons += list(out)
            
            self.assertAminoHistogramFunc([inputs[3], codons])
        elif (inputs[2] == '2'):
            lengths = [len(seq) for seq in sequences]
            gcRatios = [(seq.count('G') + seq.count('C') / len(seq)) for seq in sequences]

            self.assertGCScatterFunc([inputs[3], lengths, gcRatios])
        elif (inputs[2] == '3'):
            self.assertCreateBaseLineplotFunc([inputs[3], sequences[int(inputs[4])]])


    @Number(1.1)
    @Weight(.33)
    def test_example_execution_one(self):
        """Example Execution #1"""

        codonsFile = "codons.dat"
        sequencesFile = "sequences.dat"
        plotNum = "1"
        plotName = "plot.png"

        self.assertProgramExecution([codonsFile, sequencesFile, plotNum, plotName])

    @Number(1.2)
    @Weight(.33)
    def test_example_execution_two(self):
        """Example Execution #2"""

        codonsFile = "codons.dat"
        sequencesFile = "sequences.dat"
        plotNum = "2"
        plotName = "plot.png"

        self.assertProgramExecution([codonsFile, sequencesFile, plotNum, plotName])
 
    @Number(1.3)
    @Weight(.34)
    def test_example_execution_three(self):
        """Example Execution #3"""

        codonsFile = "codons.dat"
        sequencesFile = "sequences.dat"
        plotNum = "3"
        plotName = "plot.png"
        seqNum = "1"

        self.assertProgramExecution([codonsFile, sequencesFile, plotNum, plotName, seqNum])

    @Number(2.1)
    @Weight(.33)
    def test_createAminoHist_example(self):
        """`create_amino_hist` - Given Example"""

        fileName = "plot.png"
        acids = ['M', 'A', 'G', 'Y', 'M', 'G', 'Y', 'K']

        self.assertAminoHistogramFunc([fileName, acids])

    @Number(2.2)
    @Weight(.33)
    def test_createGCScatter_example(self):
        """`create_gc_scatter` - Given Example"""

        fileName = "plot.png"
        gcRatios = [0.48, 0.44, 0.52]
        seqLengths = [50, 45, 42]

        self.assertGCScatterFunc([fileName, gcRatios, seqLengths])

    @Number(2.3)
    @Weight(.34)
    def test_createBaseLineplot_example(self):
        """`create_base_lineplot` - Given Example"""

        fileName = "plot.png"
        sequence = "TTAAACCGGGCCCGGCTACCGACCCATGATTAAACCCTACTCAAATCATT"

        self.assertCreateBaseLineplotFunc([fileName, sequence])

    @Number(3.1)
    @Weight(1)
    def test_oneLongSequence_functionOne(self):
        """One Long Sequence - Function #1"""

        codonsFile = "codons.dat"
        sequencesFile = "one_long_sequence.dat"
        plotNum = "1"
        plotName = "result.png"

        self.assertProgramExecution([codonsFile, sequencesFile, plotNum, plotName])

    @Number(3.2)
    @Weight(1)
    def test_oneLongSequence_functionTwo(self):
        """One Long Sequence - Function #2"""

        codonsFile = "codons.dat"
        sequencesFile = "one_long_sequence.dat"
        plotNum = "2"
        plotName = "result.png"

        self.assertProgramExecution([codonsFile, sequencesFile, plotNum, plotName])

    @Number(3.3)
    @Weight(1)
    def test_oneLongSequence_functionThree(self):
        """One Long Sequence - Function #3"""

        codonsFile = "codons.dat"
        sequencesFile = "one_long_sequence.dat"
        plotNum = "3"
        plotName = "output.png"
        seqNum = "0"

        self.assertProgramExecution([codonsFile, sequencesFile, plotNum, plotName, seqNum])

    @Number(3.4)
    @Weight(1)
    def test_oneShortSequence_functionOne(self):
        """One Short Sequence - Function #1"""

        codonsFile = "codons.dat"
        sequencesFile = "one_short_sequences.dat"
        plotNum = "1"
        plotName = "graph.png"

        self.assertProgramExecution([codonsFile, sequencesFile, plotNum, plotName])

    @Number(3.5)
    @Weight(1)
    def test_oneShortSequence_functionTwo(self):
        """One Short Sequence - Function #2"""

        codonsFile = "codons.dat"
        sequencesFile = "one_short_sequences.dat"
        plotNum = "2"
        plotName = "plot.png"

        self.assertProgramExecution([codonsFile, sequencesFile, plotNum, plotName])

    @Number(3.6)
    @Weight(1)
    def test_oneShortSequence_functionThree(self):
        """One Short Sequence - Function #3"""

        codonsFile = "codons.dat"
        sequencesFile = "one_short_sequences.dat"
        plotNum = "3"
        plotName = "result.png"
        seqNum = "0"

        self.assertProgramExecution([codonsFile, sequencesFile, plotNum, plotName, seqNum])

    @Number(3.7)
    @Weight(1)
    def test_manyLongSequences_functionOne(self):
        """Many Long Sequences - Function #1"""

        codonsFile = "codons.dat"
        sequencesFile = "many_long_sequences.dat"
        plotNum = "1"
        plotName = "plot.png"

        self.assertProgramExecution([codonsFile, sequencesFile, plotNum, plotName])

    @Number(3.8)
    @Weight(1)
    def test_manyLongSequences_functionTwo(self):
        """Many Long Sequences - Function #2"""

        codonsFile = "codons.dat"
        sequencesFile = "many_long_sequences.dat"
        plotNum = "2"
        plotName = "graph.png"

        self.assertProgramExecution([codonsFile, sequencesFile, plotNum, plotName])

    @Number(3.9)
    @Weight(1)
    def test_manyLongSequences_functionThree(self):
        """Many Long Sequences - Function #3"""

        codonsFile = "codons.dat"
        sequencesFile = "many_long_sequences.dat"
        plotNum = "3"
        plotName = "output_graph.png"
        seqNum = "38"

        self.assertProgramExecution([codonsFile, sequencesFile, plotNum, plotName, seqNum])
