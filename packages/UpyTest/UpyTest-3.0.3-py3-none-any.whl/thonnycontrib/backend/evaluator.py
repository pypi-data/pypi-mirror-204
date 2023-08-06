# Module Evaluator

from typing import Dict, List

from thonnycontrib.utils import send_current_state
from .ast_parser import L1DocTest
from thonnycontrib.properties import EXECUTED_STATE, FINISHED_STATE, PENDING_STATE
from thonnycontrib.exceptions import *
from thonnycontrib.utils import *
from .doctest_parser import *
from thonnycontrib.backend.verdicts.Test import Test
from thonnycontrib.backend.verdicts.EmptyTest import EmptyTest
from thonny import *
from types import ModuleType
from .test_finder import TestFinder
import sys 

class Evaluator:
    """
    Instantiate an `Evaluator` with a filename, a source and a test_finder. 
    The evaluator relies on the `TestFinder` to parse and extracts the tests from
    the docstrings. 
    
    Args:
        filename (str, optional): the filename to be executed by the `Evaluator`. Defaults to "".
        source (str, optional): the source code to be parsed by the `TestFinder`. Defaults to "".
        test_finder (TestFinder, optional): the finder of the tests declared in docstrings. 
                                        Defaults to TestFinder().
    """
    def __init__(self, filename:str="", source:str="", test_finder: TestFinder=TestFinder()):
        self._globals = dict()
        self._module: ModuleType = None
        self._test_finder = test_finder
        self._test_finder.set_filename(filename)
        self._test_finder.set_source(source)

    def evaluate(self) -> Dict[ast.AST, List[Test]]:
        """Imports the module from the filename, sets the global variables to
        imported module's dict and then evaluates the tests.

        Returns:
            Dict[ast.AST, list[Test]]: Returns for each node its list of verdicts (type of Test)
        """
        # si le `self._module` est null, alors `Evaluator` va s'occuper d'importer lui même
        # le module à partir du filename. 
        # Sinon, le module a été fournit, donc `Evaluator` utilisera le module fournit.
        if not self._module:
            # The `import_module()` function can raise an exception(see it's doc)
            self._module = import_module(self.get_filename()) 
        
        # set a globals dictionary that will contains all the functions and 
        # meta-informations decalared in the module
        self._globals = self._module.__dict__
        return self.__get_verdicts() 
    
    def __get_verdicts(self) -> Dict[ast.AST, List[Test]]:
        """
        Evaluate all the tests containing in the working editor. 
        Returns a list of passed, failed or empty tests. 
        The list can also contains the tests that raises other exceptions.
        
        Args:
            module (ModuleType): The module to be run.
        
        Returns:
            Dict[ast.AST, list[Test]]: Returns for each node its list of verdicts (type of Test)
        
        Raises:
            NoTestFoundException: When no test are found in the working editor.
            CompilationError: When the doctest parser raises an exception, it's catched 
                            and raised as a `CompilationError`, or when AST parser fails.
        """
        try:     
            # This line parses the source using the AST module and can raise a compilation error 
            l1_doctests = self._test_finder.extract_examples() 
            all_verdicts = self.__evaluate_each_method(l1_doctests)
            return group_by_node(all_verdicts)
        except (NoFunctionSelectedToTestException) as e:
            raise RuntimeException(str(e))
        except DoctestParserException as e:
            raise CompilationError(str(e)) 
        except InterruptedError as e:
            raise InterruptedError(str(e))
        except BaseException as e:
            # the compilation error is catched and raised as a CompilationError
            # and the evaluation is interrupted(because we cannot parse a content
            # with compilation errors).
            error_info = sys.exc_info()
            formatted_error = get_last_exception(error_info)
            raise CompilationError(formatted_error)     
    
    def __evaluate_each_method(self, l1_doctests: List[L1DocTest]) -> list[Test]:
        """
        Evaluates the doctest for each method containing in the source file.
        
        Args:
            l1_doctests ( List[L1DocTest): a list of L1DocTest.

        Returns:
            list[Test]: Returns a list of verdicts. Each verdict is a type of `Test`. 
        """
        all_verdicts = []
        for l1_doctest in l1_doctests:
            locals = {} # dictionnaire pour les variables locales
            copy_globals = self._globals.copy()    
            # si le noeud contient au moins un doctest
            if l1_doctest.has_examples():
                all_verdicts += self.__evaluate_each_test(l1_doctest.get_node(), 
                                                          l1_doctest.get_examples(), 
                                                          copy_globals, 
                                                          locals)
            else:
                all_verdicts += [EmptyTest(self._test_finder.get_filename(), node=l1_doctest.get_node(), 
                                           lineno=l1_doctest.get_node().lineno)]                           
        send_current_state(state=FINISHED_STATE)
        return all_verdicts
    
    def __evaluate_each_test(self, node: ast, examples: list[Example], globals:dict, locals):
        """Evaluate each test of an AST node.

        Args:
            node (ast): An ast node.
            examples (list[Example]): The list of tests of the given AST node.
            gloabls (dict): The dictionary of the global variables.
            locals (dict): The dictionary of the local variables used within the tests as setup.

        Returns:
            list[Test]: Returns a list of verdicts of each executed test in the given node.
        """
        node_verdicts = [] 
        for example in examples: 
            options_to_send = dict(source=example.source.strip(), invite=example.invite, lineno=example.lineno)
            send_current_state(state=PENDING_STATE, **options_to_send)
            
            verdict = example.exec_and_computes_verdict(node, globals, locals)
            if verdict:
                node_verdicts.append(verdict) 
             
            send_current_state(state=EXECUTED_STATE)
         
        # si une fonction contient que des setup alors y aura pas de verdicts -> verdict orange
        if (not node_verdicts):
            node_verdicts.append(EmptyTest(self._test_finder.get_filename(), node=node, lineno=node.lineno))
        return node_verdicts 
    
    def get_globals(self):
        return self._globals

    def get_module(self):
        return self._module

    def set_module(self, module: ModuleType):
        self._module = module
        
    def set_test_finder(self, test_finder):
        self._test_finder = test_finder
    
    def get_test_finder(self):
        return self._test_finder

    def set_filename(self, filename):
        self._test_finder.set_filename(filename)
    
    def get_filename(self):
        return self._test_finder.get_filename()
    
    def set_source(self, source:str):
        self._test_finder.set_source(source)
        
    def get_source(self):
        return self._test_finder.get_source()
    
    def set_finder_strategy(self, finder_strategy):
        self._test_finder.set_strategy(finder_strategy)


# ######################################
#  UTILITY FUNCTIONS 
# ######################################
def group_by_node(list_results: List[Test]) -> Dict[ast.AST, List[Test]]:
    """Group the tests containing in the ~list_results~ by their nodes.

    Args:  
        list_results (List[Test]): a list of Test objects.

    Returns:
        dict[ast.AST, List[Test]]: a dictionary containing for each node its list of tests.
    """ 
    groups = {}
    for res in list_results:
        ast_node = res.get_ast_node()
        if ast_node in groups:
            groups[ast_node].append(res)
        else:
            groups[ast_node] = [res]
    return groups