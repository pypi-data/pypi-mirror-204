import ast
from .doctest_parser import DocTestParser, Example
from typing import List

# Only these types can have a docstring 
# according to ast's module documentation
SUPPORTED_TYPES = (ast.FunctionDef, 
                   ast.AsyncFunctionDef, 
                   ast.ClassDef, 
                   ast.Module)

class L1DocTest():
    """
    An `L1DocTest` is associated to an ast node and that groups its tests containing in the docstring of that node.
    The `L1DocTest` is identified by its node, its docstring, its starting lineno and its ending lineno. The 
    starting/ending lineno is the starting/ending line of the docstring. 
    
    An `L1DocTest` handles a list of the example of type `Example`.
    
    Args:
        ast_node (ast.AST): The ast node to be associated to the L1Doctest.
        docstring (str): The docstring of the associated ast node. 
        start_lineno (int): the starting lineno of the docstring.
        Defaults to -1 If no docstring was found.
        end_lineno (int): the ending lineno of the docstring.
        Defaults to -1 If no docstring was found.
    """
    def __init__(self, ast_node:ast.AST, docstring:str, start_lineno=-1, end_lineno=-1) -> None:
        self.__node = ast_node
        self.__start_lineno = start_lineno
        self.__end_lineno = end_lineno
        self.__docstring = docstring
        self.__examples:List[Example] = []
        
    def add_example(self, example:Example):
        self.__examples.append(example)
        
    def remove_example(self, example:Example):
        self.__examples.remove(example)
    
    def has_examples(self) -> bool:
        """
        Returns:
            bool: Returns True if this `L1Doctest` contains at least one `Example`. 
            Otherwise, returns False.
        """
        return len(self.__examples) > 0
    
    def has_docstring(self) -> bool:
        """
        Returns:
            bool: Returns True if this `L1Doctest` contains a docstring. 
            Otherwise, returns False.
        """
        return bool(self.__docstring)
    
    def get_examples(self):
        return self.__examples
    
    def set_examples(self, examples:List[Example]):
        self.__examples = examples
    
    def get_docstring(self):
        return self.__docstring
    
    def get_node(self):
        return self.__node
    
    def get_start_end_lineno(self):
        return (self.__start_lineno, self.__end_lineno)

    def get_start_lineno(self):
        return self.__start_lineno
    
    def set_start_lineno(self, start_lineno):
        self.__start_lineno = start_lineno
    
    def get_end_lineno(self):
        return self.__end_lineno
    
    def set_end_lineno(self, end_lineno):
        self.__end_lineno = end_lineno
    
    def __str__(self) -> str:
        return "L1Doctest {\n examples = %s,\n start_lineno = %s,\n end_lineno = %s,\n docstring = %s}" \
                % (self.__examples, self.__start_lineno, self.__end_lineno, self.__docstring)
    
    
class L1TestAstParser():
    def __init__(self, filename:str="", source:str="", mode="exec") -> None:
        self._source = source
        self._filename = filename
        self._mode = mode

    def get_l1_doctests(self, list_nodes: list) -> List[L1DocTest]:
        """
        Takes a list of supported nodes and returns list of L1DocTest. 
        Each L1DocTest represents an AST node. 
        """
        l1doctests: List[L1DocTest] = []
        for node in list_nodes:
            if isinstance(node, SUPPORTED_TYPES):
                docstring = ast.get_docstring(node, False) or ""
                l1doctest = L1DocTest(node, docstring)
                if node.body:
                    first_stmt = node.body[0]
                    if isinstance(first_stmt, ast.Expr) and isinstance(first_stmt.value, ast.Str):
                        l1doctest.set_start_lineno(first_stmt.lineno)
                        l1doctest.set_end_lineno(first_stmt.end_lineno)
                
                parsed_doc = DocTestParser().parse(l1doctest.get_docstring(), name=self._filename)
                l1doctest.set_examples(self.__filter_example_instances(l1doctest, parsed_doc))
                l1doctests.append(l1doctest)
        return l1doctests

    def get_l1_doctest(self, node:ast):
        """
        Returns the corresponding L1DocTest for the given node.
        
        Args: 
            node (ast) : the ast node.  
            This parameter cannot be None and should be a supported type. See `SUPPORTED_TYPES`.
        """
        assert node != None and isinstance(node, SUPPORTED_TYPES)
        return self.get_l1_doctests([node])

    def _get_supported_nodes(self):
        """
        Get only the nodes that can have a docstring. 
        The supported nodes are repported to ~SUPPORTED_TYPES~ constant.
        
        Returns:
            list[ast.AST]: returns only the nodes that can have a docstring. 
        
        Raises: 
            Error: A compilation error raised by the AST module.
        """
        source_nodes = [node for node in self.__get_ast_body() if isinstance(node, SUPPORTED_TYPES)]
        all_nodes = []
        # get all the supported nodes from a source content
        self.__recursive_walking(source_nodes, all_nodes)
        return all_nodes      
    
    def __filter_example_instances(self, l1_doctest:L1DocTest, parsed_doc:list) -> List[Example]:
        """
        The filter can return an empty list if there's no example 
        in the parsed docstring. Otherwise, it will return a list of the `Example` instances 
        matching the given l1doctest.
        """
        examples = []
        for test in parsed_doc:
            if isinstance(test, Example):
                test.lineno = test.lineno + l1_doctest.get_start_lineno() - 1
                examples.append(test)
        return examples
    
    def __get_ast_body(self):
        """
        Returns the body(list of nodes) of the root node of the AST tree.
        
        Raises: 
            Error: A compilation error raised by the AST module.
        """
        return ast.parse(self._source, self._filename, mode=self._mode).body
    
    def __recursive_walking(self, list_nodes:list, all_nodes:list):
        """
        Search all the supported nodes in the AST tree. Even sub-nodes are visited.
        This is a recursive function, so all the visited nodes are added in the ~all_nodes~
        parameter.
        """
        for node in list_nodes:
            if isinstance(node, SUPPORTED_TYPES):
                all_nodes.append(node)
                self.__recursive_walking(node.body, all_nodes)
            
    def get_filename(self):
        return self._filename
    
    def set_filename(self, filename: str):
        self._filename = filename
    
    def get_source(self):
        return self._source
    
    def set_source(self, source: str):
        self._source = source
        
    def get_mode(self):
        return self._mode
    
    def set_mode(self, mode):
        self._mode = mode
