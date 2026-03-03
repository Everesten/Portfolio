import ast
import os
from typing import List, Dict

from StudentSubmission.AbstractValidator import AbstractValidator, ValidationHook
from StudentSubmissionImpl.Python.common import FileTypeMap


class RecursionValidator(AbstractValidator):
    @staticmethod
    def getValidationHook() -> ValidationHook:
        return ValidationHook.VALIDATION

    def __init__(self, recursiveFunctions: List[str]):
        super().__init__()
        self.recursiveFunctions = recursiveFunctions

        self.pythonFiles: Dict[FileTypeMap, List[str]] = {}

    def setup(self, studentSubmission):
        self.pythonFiles = studentSubmission.getDiscoveredFileMap()

    def _processAst(self, tree: ast.AST) -> Dict[str, ast.AST]:
        functions: Dict[str, ast.AST] = {}
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef):
                continue
            if str(node.name) not in self.recursiveFunctions:
                continue

            functions[str(node.name)] = node

        return functions

    @staticmethod
    def _isRecursive(name: str, body: ast.AST, level: int = 0) -> bool:
        nestedRecusion = False
        for expr in ast.walk(body):
            # if they do a nested function... Why ben?!?
            if level == 0 and isinstance(expr, ast.FunctionDef):
                # only allowing one level of nested functions. dear jesus, why????
                nestedRecusion = RecursionValidator._isRecursive(expr.name, expr, (level + 1))

                if nestedRecusion:
                    return True

                continue

            if not isinstance(expr, ast.Call):
                continue
            if not isinstance(expr.func, ast.Name):
                continue

            if expr.func.id != name:
                continue

            return True

        return nestedRecusion

    def run(self):
        functionStats: Dict[str, Dict[str, bool]] = {functionName: {"occured": False, "recursive": False} for functionName in self.recursiveFunctions}
        functionAsts: Dict[str, ast.AST] = {}
        for file in self.pythonFiles[FileTypeMap.PYTHON_FILES]:
            with open(file, 'r') as r:
                try:
                    functionAsts.update(self._processAst(ast.parse(r.read())))
                except SyntaxError as ex:
                    self.addError(ex)

        for name, functionAst in functionAsts.items():
            functionStats[name]["occured"] = True
            functionStats[name]["recursive"] = self._isRecursive(name, functionAst)

        for name, stats in functionStats.items():
            if not stats["occured"]:
                continue
            if stats["occured"] and not stats["recursive"]:
                self.addError(AttributeError(f"Function: '{name}' occured and was missing recursive call!\nExpected to have recursive call."))

        # print(functionStats)

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

        self.addError(EnvironmentError("`helper_library.py` not found in student submission!\n" \
                                       "Please ensure that it is in the `student_work` folder (if running locally) or was included in your Gradescope upload (if running on gradescope)!"))

