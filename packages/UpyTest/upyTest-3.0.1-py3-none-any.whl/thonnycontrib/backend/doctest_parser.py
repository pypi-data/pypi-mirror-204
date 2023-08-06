# Module doctest.
# Released to the public domain 16-Jan-2001, by Tim Peters (tim@python.org).
# Major enhancements and refactoring by:
#     Jim Fulton
#     Edward Loper

# Provided as-is; use at your own risk; no warranty; no promises; enjoy!

# modified pour les besoins de L1test
# - modification de DoctestParser : expression régulière _EXAMPLE_RE changée
# pour supporter plusieurs invites différentes, et forcer à ce que les lignes
# source et want soient sur une seule ligne (ou absente pour want)
# - _check_prompt_blank : cette fonction lèvait une ValueError qd il manque
# un caractère espace après l'invite, ce qui déclenchait l'ouverture d'une
# pop-up "internal error" assez affreuse. Maintenant l'erreur levée est
# ManqueUnEspace et le message associé est affiché ds la fenêtre de test.
__docformat__ = 'reStructuredText en'

__all__ = [
    # 0, Option Flags
    'register_optionflag',
    'DONT_ACCEPT_TRUE_FOR_1',
    'DONT_ACCEPT_BLANKLINE',
    'NORMALIZE_WHITESPACE',
    'ELLIPSIS',
    'SKIP',
    'IGNORE_EXCEPTION_DETAIL',
    'COMPARISON_FLAGS',
    'REPORT_UDIFF',
    'REPORT_CDIFF',
    'REPORT_NDIFF',
    'REPORT_ONLY_FIRST_FAILURE',
    'REPORTING_FLAGS',
    'FAIL_FAST',
    # 1. Utility Functions
    # 2. Example & DocTest
    'Example',
    # 3. Doctest Parser
    'DocTestParser',
]
from abc import *
import __future__
import re
from collections import namedtuple
import sys

# ajout L1test
from thonnycontrib.properties import L1TEST_EXCEPTION_SYMBOL, L1TEST_SYMBOL1, L1TEST_SYMBOL2, L1TEST_SYMBOL3

from thonnycontrib.backend.verdicts.EmptyTest import *
from thonnycontrib.backend.verdicts.FailedTest import *
from thonnycontrib.backend.verdicts.FailedWhenExceptionExpectedTest import *
from thonnycontrib.backend.verdicts.PassedTest import *
from thonnycontrib.backend.verdicts.ExceptionTest import *

from thonnycontrib.exceptions import *
from thonnycontrib.utils import *

TestResults = namedtuple('TestResults', 'failed attempted')

# There are 2 basic classes:
#  - Example: a <source, want> pair, plus an intra-docstring line number.
#  - DocTest: a collection of examples, parsed from a docstring, plus
#    info about where the docstring came from (name, filename, lineno).
#  - DocTestFinder: extracts DocTests from a given object's docstring and
#    its contained objects' docstrings.
#  - DocTestRunner: runs DocTest cases, and accumulates statistics.
#
# So the basic picture is:
#
#                             list of:
# +------+                   +---------+                   +-------+
# |object| --DocTestFinder-> | DocTest | --DocTestRunner-> |results|
# +------+                   +---------+                   +-------+
#                            | Example |
#                            |   ...   |
#                            | Example |
#                            +---------+

# Option constants.

OPTIONFLAGS_BY_NAME = {}
def register_optionflag(name):
    # Create a new flag unless `name` is already known.
    return OPTIONFLAGS_BY_NAME.setdefault(name, 1 << len(OPTIONFLAGS_BY_NAME))

DONT_ACCEPT_TRUE_FOR_1 = register_optionflag('DONT_ACCEPT_TRUE_FOR_1')
DONT_ACCEPT_BLANKLINE = register_optionflag('DONT_ACCEPT_BLANKLINE')
NORMALIZE_WHITESPACE = register_optionflag('NORMALIZE_WHITESPACE')
ELLIPSIS = register_optionflag('ELLIPSIS')
SKIP = register_optionflag('SKIP')
IGNORE_EXCEPTION_DETAIL = register_optionflag('IGNORE_EXCEPTION_DETAIL')

COMPARISON_FLAGS = (DONT_ACCEPT_TRUE_FOR_1 |
                    DONT_ACCEPT_BLANKLINE |
                    NORMALIZE_WHITESPACE |
                    ELLIPSIS |
                    SKIP |
                    IGNORE_EXCEPTION_DETAIL)

REPORT_UDIFF = register_optionflag('REPORT_UDIFF')
REPORT_CDIFF = register_optionflag('REPORT_CDIFF')
REPORT_NDIFF = register_optionflag('REPORT_NDIFF')
REPORT_ONLY_FIRST_FAILURE = register_optionflag('REPORT_ONLY_FIRST_FAILURE')
FAIL_FAST = register_optionflag('FAIL_FAST')

REPORTING_FLAGS = (REPORT_UDIFF |
                   REPORT_CDIFF |
                   REPORT_NDIFF |
                   REPORT_ONLY_FIRST_FAILURE |
                   FAIL_FAST)

# Special string markers for use in `want` strings:
BLANKLINE_MARKER = '<BLANKLINE>'
ELLIPSIS_MARKER = '...'


######################################################################
## 2. Example 
######################################################################
## - An "example" is a <source, want> pair, where "source" is a
##   fragment of source code, and "want" is the expected output for
##   "source."  The Example class also includes information about
##   where the example was extracted from.

class Example(ABC):
    """
    A single doctest example, consisting of source code and expected
    output.  `Example` defines the following attributes:

      - source: A single Python statement, always ending with a newline.
        The constructor adds a newline if needed.

      - want: The expected output from running the source code (either
        from stdout, or a traceback in case of exception).  `want` ends
        with a newline unless it's empty, in which case it's an empty
        string.  The constructor adds a newline if needed.

      - exc_msg: The exception message generated by the example, if
        the example is expected to generate an exception; or `None` if
        it is not expected to generate an exception.  This exception
        message is compared against the return value of
        `traceback.format_exception_only()`.  `exc_msg` ends with a
        newline unless it's `None`.  The constructor adds a newline
        if needed.

      - lineno: The line number within the DocTest string containing
        this Example where the Example begins.  This line number is
        zero-based, with respect to the beginning of the DocTest.

      - indent: The example's indentation in the DocTest string.
        I.e., the number of space characters that precede the
        example's first prompt.

      - options: A dictionary mapping from option flags to True or
        False, which is used to override default options for this
        example.  Any option flags not contained in this dictionary
        are left at their default value (as specified by the
        DocTestRunner's optionflags).  By default, no options are set.
    """
    def __init__(self, filename:str, source:str, want:str, invite:str, exc_msg:str=None, lineno:int=0, indent:int=0, 
                 options:dict=None):
        # Normalize inputs.
        if not source.endswith('\n'):
            source += '\n'
        if want and not want.endswith('\n'):
            want += '\n'
        if exc_msg is not None and not exc_msg.endswith('\n'):
            exc_msg += '\n'
        # Store properties.
        self.filename = filename
        self.source = source
        self.want = want
        self.lineno = lineno
        self.indent = indent
        self.invite = invite
        if options is None: options = {}
        self.options = options
        self.exc_msg = exc_msg

    @abstractmethod
    def exec_and_computes_verdict(self, node:ast, globals:dict={}, locals:dict={}):
        pass
    
    def _execute_statement(self, source:str, globals:dict, locals:dict, lineno:int):
        """
        Execute a source code using the given globals. 
        
        This function should be invoked after a `compile()`. The compile() function is removed from 
        this function because it's hard to know if an exception is raised by a compilation error
        or by an executed statement(using exec()). 
        
        Args:
            source (str): A string representing a source code. 
            globals (dict): The dictionary of the global variables.
            locals (dict): The dictionary of the local variables. 
            lineno (int): The line of the test to execute.
        Raises:
            RuntimeException: When the source code raises a runtime error(ex. NameError...)
        """
        try:
            exec(source, globals, locals)
        except BaseException as e:
            error_info = sys.exc_info()
            formatted_error = replace_filename(self.filename, get_last_exception(error_info))
            # For runtime errors the line mentionned in the error raised by `exec()` is always equal to 1.
            # To learn about runtime errors in python: https://www.geeksforgeeks.org/runtime-errors/
            has_error_lineno = re.search(r'line (\d+)', formatted_error)
            if has_error_lineno:
                error_line = int(has_error_lineno.group(1))
                # comme cette fonction est toujours appelée pour executer un test ou sa valeur attendu
                # alors on aura jamais la ligne d'erreur est égal à 1. Donc, on remplace la ligne d'erreur
                # par le numéro de ligne du test.
                if error_line == 1: 
                    formatted_error = replace_error_line(formatted_error, lineno)
            raise RuntimeException(formatted_error)
    
    def _check_source_syntax(self, source:str, lineno:int, mode="single"):
        """
        Compile the `source` of a test statement and raise an exception when a 
        compilation error occurs.

        Args:
            source (str): The statement to be compiled
            mode (str): Defaults to "single".
        Raises:
            CompilationError: when a compilation error occurs.
        """
        try:
            compile(source, filename=self.filename, mode=mode)
        except Exception:
            formatted_error = get_last_exception(sys.exc_info())
            raise CompilationError(replace_error_line(formatted_error, lineno))

    def _check_want_syntax(self, got:str, lineno:int, mode="single"):
        """
        Compile the `want` statement of a test and raise an exception when 
        a compilation error occurs.

        Args:
            source (str): The statement to be compiled
            mode (str): Defaults to "single".
        Raises:
            CompilationError: when a compilation error occurs.
        """
        try:
            compile(got, filename=self.filename, mode=mode)
        except Exception:
            formatted_error = get_last_exception(sys.exc_info())
            raise CompilationError(replace_error_line(formatted_error, lineno))
    
    def _create_affectation_statement(self, statement1, statement2):
        """
        Creates an affectation expression by affecting the statement2 to statement1.

        The result will be : "%s = %s" % (statement1, statement2)
        
        Args:
            statement1 (str): the left side of the affectation expression
            statement2 (str): the right side of the affectation expression

        Returns:
            (str): the affectation expression using `statement1` and `statement1`. 
        """
        return "%s = (%s)" % (statement1, statement2)
        
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented

        return self.filename == other.filename and \
               self.source == other.source and \
               self.want == other.want and \
               self.lineno == other.lineno and \
               self.indent == other.indent and \
               self.options == other.options and \
               self.exc_msg == other.exc_msg

    def __hash__(self):
        return hash((self.filename, self.source, self.want, self.lineno, 
                     self.indent, self.exc_msg))

        
class ExampleWithExpected(Example):
    """
    An `ExampleWithExpected` is a test example that expects a value to be returned.
    """
    def exec_and_computes_verdict(self, node:ast, globals:dict={}, locals:dict={}):
        executed, wanted = add_random_suffix("executed"), add_random_suffix("wanted")
        want = self.want.strip("\n")   
        try:             
            # we should check the syntax of the `source` before executing it   
            self._check_source_syntax(self.source, self.lineno)
            # we should check the syntax of the `want` before executing it 
            self._check_want_syntax(self.want, self.lineno)
            
            # si on est là alors la syntaxe de la source et du want est valide
            # et on doit pouvoir les executer sans problème
            self._execute_statement(self._create_affectation_statement(executed, self.source), 
                                    globals, locals, self.lineno)
            self._execute_statement(self._create_affectation_statement(wanted, self.want), 
                                    globals, locals, self.lineno)
            
            self._check_source_syntax(self.str_comparaison(self.source, self.want), self.filename, "single")
            
            if locals[executed] == locals[wanted]:
                verdict = PassedTest(self.filename, node=node, tested_line=self.source.strip(), 
                                      expected_result=want, lineno=self.lineno)
            else:
                verdict = FailedTest(self.filename, node=node, tested_line=self.source.strip(), 
                                      expected_result=want, obtained_result=locals[executed], 
                                      lineno=self.lineno)
        except (CompilationError, RuntimeException) as e:
            verdict = ExceptionTest(self.filename, node=node, tested_line=self.source.strip(), 
                                    expected_result=want, lineno=self.lineno, message=str(e))
        return verdict

    def str_comparaison(self, expected, got):
        return  "(%s) == (%s)" % (expected, got) 
    
class ExampleWithoutExpected(Example):
    """
    An `ExampleWithNoExpected` is an example without a `want` and cannot be considered as a test.
    """
    def exec_and_computes_verdict(self, node:ast, globals:dict={}, locals:dict={}):
        try:  
            # we check the syntax of the test before its execution
            self._check_source_syntax(self.source, self.lineno) 
            self._execute_statement(self.source, globals, locals, self.lineno)
            return None
        except (RuntimeException, CompilationError) as error:
            return ExceptionTest(self.filename, node=node, tested_line=self.source.strip(), 
                                 expected_result=self.want.strip("\n"), lineno=self.lineno, 
                                 message=str(error))

class ExampleExceptionExpected(Example):
    """
    An `ExampleExceptionExpected` is a test example that expects an exception to be raised.
    """
    def exec_and_computes_verdict(self, node:ast, globals:dict={}, locals:dict={}):
        want = self.want.strip("\n").strip()
        try:
            self.__check_want_validity(want, globals)
            return self.__execute_and_get_verdict_(node, globals, locals, want) 
        except (ValueError, TypeError, NameError) as e:
            return self.__build_exception_verdict(e, node, want)      
    
    def __execute_and_get_verdict_(self, node:ast.AST, globals, locals, want:str):
        try:
            # il faudrait quand même compiler la source avant de l'executer
            self._check_source_syntax(self.source, self.lineno)
            
            exec(self.source, globals, locals)
            
            # si on est ici alors aucune exc levée -> FailedTest
            # <nom_exc> was not raised by <source>
            failure_msg = "%s was not raised by %s" % (want, self.source.strip()) 
            return FailedWhenExceptionExpectedTest(self.filename, node=node, tested_line=self.source.strip(), 
                                expected_result=want,lineno=self.lineno, failure_message=failure_msg)        
        except BaseException as e: # ici on a forcément une exception levée par le code source
                # mais a priori rien de syntaxique car on est sur un seul nom
            error_type, _, _ = sys.exc_info()    
            exc_name_effective = str(error_type.__name__)
            if want == exc_name_effective: 
                return PassedTest(self.filename, node=node, tested_line=self.source.strip(), 
                                    expected_result=want, lineno=self.lineno)   
            else: # forcément une erreur de compilation ou encore une erreur de runtime
                # si c'est une erreur `CompilationError` alors on récupère seulement sa représentation      
                if isinstance(e, CompilationError):   # if CompilationError -> ExceptionTest verdict
                    return ExceptionTest(self.filename, node=node, tested_line=self.source.strip(), 
                                            expected_result=want, lineno=self.lineno, message=str(e))
                else: # sinon on doit chercher la dernière exception. 
                    formatted_error = get_last_exception(sys.exc_info())                  
                    failure_msg = "%s was not raised by %s\nInstead, it raises :\n%s" % (want, self.source.strip(), formatted_error) 
                    return FailedWhenExceptionExpectedTest(self.filename, node=node, tested_line=self.source.strip(), 
                                expected_result=want,lineno=self.lineno, failure_message=failure_msg) 
    
    def __build_exception_verdict(self, exception, node, want):
        """
        Returns an exception verdict with the given exception message. 

        Args:
            exception_msg (str): The exception message
            node (ast.AST): The node ast associated to that Example.
            want (str): The want of the Example.

        Returns:
            ExceptionTest: an exception verdict with the given exception message. 
        """
        common_msg = 'File "%s", line %s\n' % (self.filename, self.lineno) 
        error_msg = common_msg + "%s:\n  %s" % (exception.__class__.__name__, str(exception))
        return ExceptionTest(self.filename, node=node, tested_line=self.source.strip(), 
                             expected_result=want, lineno=self.lineno, 
                             message=error_msg)  
    
    def __check_want_validity(self, want:str, globals:dict):
        """_summary_
        Checks if the <want> syntax is an exception and if it inherits 
        from the BaseException class.
        Args:
            want (str): The value of the <want> to check.
            globals (dict): The global is needed to look for the associated 
            given exception.
        
        Raises: 
            - ValueError: when the want doesn't respect the syntaxe.
            - TypeError: if the retrieved exception from the given exception name is not an exception that
                        inherits from `BaseException`. 
            - NameError: if cannot retrieve the exception from the given exception name.
        """
        # On vérifie si la syntaxe du <want> est une exception -> lève exception sinon
        self.__is_an_exception(want)
        # On vérifie si l'exception hérite de la BaseException -> lève exception sinon
        self.__is_exception_inherits_from_BaseException(globals, want)
        
    def __is_an_exception(self, want):
        """Check if the want is a valid exception name that contains letters, 
        numbers and/or underscore.

        Args:
            want (str): a string.

        Raises:
            ValueError: when the want doesn't respect the syntaxe.
        """
        match = re.match("^[a-zA-Z][a-zA-Z0-9_]*", want)
        if not match:
            if not want:
                error_msg = "The expected exception cannot be empty or blank."
            else: 
                error_msg = '%s\nIndentationError: unexpected indent' % self.want.strip("\n") \
                                if self.want.strip("\n").startswith(" ") \
                                else 'The expected exception `%s` is not a valid exception name.' % want
            raise ValueError(error_msg)
    
    def __get_exception_from_name(self, globals:dict, exception_name:str):
        """Returns the exception class from its name.

        Args:
            globals (dict): the globals contains all the declared meta informations on the module.
            exception_name (str): the name of the exception.

        Returns:
            (object|None): an object(maybe an exception or not) or None if the exception is not
                        a known exception.
        """
        builtins = globals['__builtins__'].__dict__ if isinstance(globals['__builtins__'], ModuleType) \
                                                    else globals['__builtins__']
        if exception_name in builtins:
            return builtins[exception_name]
        else:  
            # si on est là alors le nom de l'exception n'est pas trouvée dans le __builtins__
            # on doit chercher si l'exception est déclarée dans le fichier executé
            return globals[exception_name] if exception_name in globals else None 
                
    def __is_exception_inherits_from_BaseException(self, globals: dict, exception_name: str) -> None:
        """Checks the superclass of the given exception name. 
        This function first gets the corresponding exception class from its name.
        Then, it verifies if the exception class is really an exception (inherits from `BaseException`).
        
        Args:
            globals (dict): the globals contains all the declared meta informations on the module.
            exception_name (str): the name of the exception.

        Returns:
            None: Return None if the given exception name is an exception that inherits form `BaseException`.
                Otherwise, raises exceptions.
        Raises:
            - TypeError: if the retrieved exception from the given exception name is not an exception that
                        inherits from `BaseException`. 
            - NameError: if cannot retrieve the exception from the given exception name.
        """
        exception: object = self.__get_exception_from_name(globals, exception_name)
        import inspect
        if exception:
            try:
                super_cls = inspect.getmro(exception)[1:] # le premier élément est la classe elle même
                if BaseException in super_cls:
                    return None
                else:
                    raise TypeError("The expected exception `%s` is not a class of type exception." % exception_name) 
            except:
                raise TypeError("The expected exception `%s` is not a class of type exception." % exception_name) 
        raise NameError("The expected exception `%s` cannot be found." % exception_name)

    
    
######################################################################
## 3. DocTestParser
######################################################################

class DocTestParser:
    """
    A class used to parse strings containing doctest examples.
    """
    # This regular expression is used to find doctest examples in a
    # string.  It defines three groups: `source` is the source code
    # (including leading indentation and prompts); `indent` is the
    # indentation of the first (PS1) line of the source code; and
    # `want` is the expected output (including leading indentation).
    _EXAMPLE_RE = re.compile(r'''
        # Source consists of a PS1 line 
        (?P<source>
            (?:^(?P<indent> [ ]*) (?P<invite> %s|%s|%s|%s)    .*))    # PS1 line
        \n?
        # Want consists of zero or one non-blank lines that do not start with PS1.
        (?P<want> (?:(?![ ]*$)    # Not a blank line
                     (?![ ]*(%s|%s|%s|%s))  # Not a line starting with PS1
                     .+$\n?       # But any other line
                  )?) # 0 ou 1 é
        '''%(L1TEST_SYMBOL1, L1TEST_SYMBOL2, L1TEST_SYMBOL3, L1TEST_EXCEPTION_SYMBOL,   # source
             L1TEST_SYMBOL1, L1TEST_SYMBOL2, L1TEST_SYMBOL3, L1TEST_EXCEPTION_SYMBOL),  # want
             re.MULTILINE | re.VERBOSE)

    # version d'origine doctest avec nouvelle invite
    # _EXAMPLE_RE = re.compile(r'''
    #     # Source consists of a PS1 line followed by zero or more PS2 lines.
    #     (?P<source>
    #         (?:^(?P<indent> [ ]*) (%s|%s|%s)    .*)    # PS1 line
    #         (?:\n           [ ]*  \.\.\. .*)*)  # PS2 lines
    #     \n?
    #     # Want consists of any non-blank lines that do not start with PS1.
    #     (?P<want> (?:(?![ ]*$)    # Not a blank line
    #                  (?![ ]*(%s|%s|%s))  # Not a line starting with PS1
    #                  .+$\n?       # But any other line
    #               )*)
    #     '''%(L1TEST_SYMBOL1, L1TEST_SYMBOL2, L1TEST_SYMBOL3, L1TEST_SYMBOL1, L1TEST_SYMBOL2, L1TEST_SYMBOL3), re.MULTILINE | re.VERBOSE)

    
    # A regular expression for handling `want` strings that contain
    # expected exceptions.  It divides `want` into three pieces:
    #    - the traceback header line (`hdr`)
    #    - the traceback stack (`stack`)
    #    - the exception message (`msg`), as generated by
    #      traceback.format_exception_only()
    # `msg` may have multiple lines.  We assume/require that the
    # exception message is the first non-indented line starting with a word
    # character following the traceback header line.
    _EXCEPTION_RE = re.compile(r"""
        # Grab the traceback header.  Different versions of Python have
        # said different things on the first traceback line.
        ^(?P<hdr> Traceback\ \(
            (?: most\ recent\ call\ last
            |   innermost\ last
            ) \) :
        )
        \s* $                # toss trailing whitespace on the header.
        (?P<stack> .*?)      # don't blink: absorb stuff until...
        ^ (?P<msg> \w+ .*)   #     a line *starts* with alphanum.
        """, re.VERBOSE | re.MULTILINE | re.DOTALL)

    # A callable returning a true value iff its argument is a blank line
    # or contains a single comment.
    _IS_BLANK_OR_COMMENT = re.compile(r'^[ ]*(#.*)?$').match

    def parse(self, string, name='<string>'):
        """
        Divide the given string into examples and intervening text,
        and return them as a list of alternating Examples and strings.
        Line numbers for the Examples are 0-based.  The optional
        argument `name` is a name identifying this string, and is only
        used for error messages.
        
        Raises:
            SpaceMissingAfterPromptException: when a space is missing after the prompt.
        """
        string = string.expandtabs()
        # If all lines begin with the same indentation, then strip it.
        min_indent = self._min_indent(string)
        if min_indent > 0:
            string = '\n'.join([l[min_indent:] for l in string.split('\n')])

        output = []
        charno, lineno = 0, 0
        # Find all doctest examples in the string:
        for m in self._EXAMPLE_RE.finditer(string):            
            invite = m.group("invite")

            # Add the pre-example text to `output`.
            output.append(string[charno:m.start()])
            # Update lineno (lines before this example)
            lineno += string.count('\n', charno, m.start())
            # Extract info from the regexp match.
            (source, options, want, exc_msg) = \
                self._parse_example(m, name, invite, lineno)
            
            # Create an Example, and add it to the list.
            if not self._IS_BLANK_OR_COMMENT(source):
                example = ExampleFactory(invite, name, source, want, exc_msg,
                                         lineno=lineno, indent=min_indent+len(m.group('indent')),
                                         options=options)
                       
                output.append(example)
            # Update lineno (lines inside this example)
            lineno += string.count('\n', m.start(), m.end())
            # Update charno.
            charno = m.end()
        # Add any remaining post-example text to `output`.
        output.append(string[charno:])
        return output

    def get_examples(self, string, name='<string>'):
        """
        Extract all doctest examples from the given string, and return
        them as a list of `Example` objects.  Line numbers are
        0-based, because it's most common in doctests that nothing
        interesting appears on the same line as opening triple-quote,
        and so the first interesting line is called \"line 1\" then.

        The optional argument `name` is a name identifying this
        string, and is only used for error messages.
        """
        return [x for x in self.parse(string, name)
                if isinstance(x, Example)]

    def _parse_example(self, m, name, invite, lineno):
        """
        Given a regular expression match from `_EXAMPLE_RE` (`m`),
        return a pair `(source, want)`, where `source` is the matched
        example's source code (with prompts and indentation stripped);
        and `want` is the example's expected output (with indentation
        stripped).

        `name` is the string's name, and `lineno` is the line number
        where the example starts; both are used for error messages.
        """
        # Get the example's indentation level.
        indent = len(m.group('indent'))

        # Divide source into lines; check that they're properly
        # indented; and then strip their indentation & prompts.
        source_lines = m.group('source').split('\n')
        self._check_prompt_blank(source_lines, indent, invite, name, lineno)
        self._check_prefix(source_lines[1:], ' '*indent + '.', name, lineno)
        source = '\n'.join([sl[indent+4:] for sl in source_lines])

        # Divide want into lines; check that it's properly indented; and
        # then strip the indentation.  Spaces before the last newline should
        # be preserved, so plain rstrip() isn't good enough.
        want = m.group('want')
        want_lines = want.split('\n')
        if len(want_lines) > 1 and re.match(r' *$', want_lines[-1]):
            del want_lines[-1]  # forget final newline & spaces after it
        self._check_prefix(want_lines, ' '*indent, name,
                           lineno + len(source_lines))
        want = '\n'.join([wl[indent:] for wl in want_lines])

        # If `want` contains a traceback message, then extract it.
        m = self._EXCEPTION_RE.match(want)
        if m:
            exc_msg = m.group('msg')
        else:
            exc_msg = None

        # Extract options from the source.
        options = self._find_options(source, name, lineno)

        return source, options, want, exc_msg

    # This regular expression looks for option directives in the
    # source code of an example.  Option directives are comments
    # starting with "doctest:".  Warning: this may give false
    # positives for string-literals that contain the string
    # "#doctest:".  Eliminating these false positives would require
    # actually parsing the string; but we limit them by ignoring any
    # line containing "#doctest:" that is *followed* by a quote mark.
    _OPTION_DIRECTIVE_RE = re.compile(r'#\s*doctest:\s*([^\n\'"]*)$',
                                      re.MULTILINE)

    def _find_options(self, source, name, lineno):
        """
        Return a dictionary containing option overrides extracted from
        option directives in the given source string.

        `name` is the string's name, and `lineno` is the line number
        where the example starts; both are used for error messages.
        """
        options = {}
        # (note: with the current regexp, this will match at most once:)
        for m in self._OPTION_DIRECTIVE_RE.finditer(source):
            option_strings = m.group(1).replace(',', ' ').split()
            for option in option_strings:
                if (option[0] not in '+-' or
                        option[1:] not in OPTIONFLAGS_BY_NAME):
                    raise ValueError('line %r of the doctest for %s '
                                     'has an invalid option: %r' %
                                     (lineno+1, name, option))
                flag = OPTIONFLAGS_BY_NAME[option[1:]]
                options[flag] = (option[0] == '+')
        if options and self._IS_BLANK_OR_COMMENT(source):
            raise ValueError('line %r of the doctest for %s has an option '
                             'directive on a line with no example: %r' %
                             (lineno, name, source))
        return options

    # This regular expression finds the indentation of every non-blank
    # line in a string.
    _INDENT_RE = re.compile(r'^([ ]*)(?=\S)', re.MULTILINE)

    def _min_indent(self, s):
        "Return the minimum indentation of any non-blank line in `s`"
        indents = [len(indent) for indent in self._INDENT_RE.findall(s)]
        if len(indents) > 0:
            return min(indents)
        else:
            return 0

    def _check_prompt_blank(self, lines, indent, invite, name, lineno):
        """
        Given the lines of a source string (including prompts and
        leading indentation), check to make sure that every prompt is
        followed by a space character.  If any line is not followed by
        a space character, then raise ValueError.
        """
        for i, line in enumerate(lines):
            invite_length = len(invite)
            if len(line) >= indent+invite_length+1 and line[indent+invite_length] != ' ':
                # old doctest version
                # raise ValueError('line %r of the docstring for %s '
                #                  'lacks blank after %s: %r' %
                #                  (lineno+i+1, name,
                #                    line[indent:indent+3], line))
                raise SpaceMissingAfterPromptException(name, lineno+i+1, line[indent:])
            
    def _check_prefix(self, lines, prefix, name, lineno):
        """
        Check that every line in the given list starts with the given
        prefix; if any line does not, then raise a ValueError.
        """
        for i, line in enumerate(lines):
            if line and not line.startswith(prefix):
                raise ValueError('line %r of the docstring for %s has '
                                 'inconsistent leading whitespace: %r' %
                                 (lineno+i+1, name, line))
     
def ExampleFactory(invite:str, filename:str, source:str, want:str, exc_msg:str, lineno:int, indent, options) -> Example:
    """
    Creates the appropriate `Example` type depending on the invite command and
    depending on the want value.
    
    - If the invite command is an exception invite so an `ExceptionExample` will be returned.
    - If the want value is empty so a `ExampleWithNoExpected` will be returned.
    - Otherwise, an `ExpectedExample` is returned.
    
    To know more about each `Example` type, please see thier documentations.
    
    Returns:
        Example: an `Example` type depending on the invite command and the want value.
    """
    exception_invite = re.search(L1TEST_EXCEPTION_SYMBOL, invite)

    if exception_invite: 
        example = ExampleExceptionExpected(filename, source, want, invite, exc_msg,
                                            lineno=lineno,
                                            indent=indent,
                                            options=options)
    else:
        if not want:
            example = ExampleWithoutExpected(filename, source, want, invite, exc_msg,
                                            lineno=lineno,
                                            indent=indent,
                                            options=options)
        else:
            example = ExampleWithExpected(filename, source, want, invite, exc_msg,
                                            lineno=lineno,
                                            indent=indent,
                                            options=options) 
    return example      
