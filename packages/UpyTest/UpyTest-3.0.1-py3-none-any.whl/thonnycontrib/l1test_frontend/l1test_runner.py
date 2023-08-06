from collections import namedtuple
from thonny.workbench import WorkbenchEvent
from ..backend.verdicts.Test import Test
from ..environement_vars import IS_SELECTED_VAR
from ..exceptions import *
from .l1test_reporter import *
from ..properties import *
from thonny.common import ToplevelResponse, InlineResponse
from thonnycontrib import l1test_frontend 
from ..ThonnyLogsGenerator import log_in_thonny
import pickle, inspect, thonny, ast

# ErrorMsg déclare deux champs : le préfixe et le message d'erreur
# le préfix est juste le titre qui précède le message d'erreur sur la Error view
ErrorMsg = namedtuple("ErrorMsg", "title msg")

# Le nom de l'event qui lance le redémarrage du backend thonny
BACKEND_RESTART_EVENT = "BackendRestart"

class L1TestRunner:
    """
        The L1TestRunner is responsible for receiving the test results returned 
        by the l1test_backend and displaying them on the treeview. The L1TestRunner 
        is also responsible for displaying errors if the l1test_backend returns 
        a response that carries an exception.
        
        Finally, the L1TestRunner decides which view (the Treeview or the ErrorView)
        to display depending on the state of program execution.
        
        Note: L1TestRunner does not deal with the construction of the views but 
        it allows to invoke the correct one.
    """
    def __init__(self, reporter=None):
        l1test_frontend._l1test_runner = self
        
        self._reporter = L1TestReporter() if not reporter else reporter
        self._has_exception = False
        self._is_l1test_running = False
        self._is_pending = False
        
        # Quand le backend envoie une réponse de type `ToplevelResponse``,
        # alors le TestRunner va invoquer la fonction `show_verdicts`
        thonny.get_workbench().bind("ToplevelResponse", self.report_verdicts, True)
        
        # Quand le backend envoie une réponse de type `InlineResponse``,
        # alors le TestRunner va invoquer la fonction `show_execution_state`
        thonny.get_workbench().bind("InlineResponse", self.show_execution_state, True)
        
        thonny.get_workbench().bind(L1TREE_VIEW_EVENT, self.show_right_view, True)
        
        # Quand le backend est redémarré en thonny nous invoquons la méthode 
        # `self._on_restart_backend()`
        thonny.get_workbench().bind(BACKEND_RESTART_EVENT, self._on_restart_backend, True)
    
    def show_execution_state(self, msg: InlineResponse):
        """
        This function is called when an event of type InlineResponse is received. 
        This function verfies the source of the event. If the source is L1Test so it will access to the 
        received response and then it will show the state of the execution.
        """
        if msg.get("command_name") == BACKEND_COMMAND:
            self.clean_error_view()

            state:str = msg.get("state")

            l1test_treeview:L1TestTreeView = self._reporter.get_l1test_treeview()
            l1test_treeview.disable_menu()
             
            l1test_treeview.insert_in_header(L1TEST_IN_PROGRESS, clear=True, tags="blue", image=l1test_treeview.pending_img)
            
            if state == PENDING_STATE:
                self.set_pending(True)
                self.clean_treeview(all=False)
                source, invite, lineno = msg.get("source"), msg.get("invite"), msg.get("lineno") 

                row_content = "%s for line %s, %s %s" % (state, lineno, invite, source)
                self.row = l1test_treeview.insert_row(text=row_content, open=True, tags=("clickable",), values=lineno)
                l1test_treeview.insert_row(parent=self.row, 
                                           text="Interrompez avec 'ctrl+c', si ce test prend plus de temps.", 
                                           tags=("nonClickable", "orange"))
            elif state == EXECUTED_STATE: 
                l1test_treeview.insert_row(parent=self.row, text=state, tags=("nonClickable", "green"))  
            elif state == INTERRUPTED_STATE:
                # print("here")
                # breakpoint()
                self.set_pending(True) 
                # l1test_treeview.insert_row(parent=self.row, text=state, tags=("nonClickable", "red")) 
                # l1test_treeview.get_treeview().item(self.row, open=True)
            else: # si le state == FINISHED_STATE
                self.set_pending(False)     
    
    def report_verdicts(self, msg: ToplevelResponse):     
        """
            This method is binded to the `TopLevelResponse` event sent by the backend.
            
            If this method is triggered so the `msg` parameter will contain the response received 
            from the backend. Please note that the `TopLevelResponse` event is not necessary sent 
            by the l1test_backend, but it can be also sent by the Shell. The shell contains an 
            internal infinite loop that waits for commands and sends the responses periodically.
            
            This method verify the source of the `TopLevelResponse` event. If the source is 
            l1test_backend so it checks the recieved response if it contains exception or not. 
            If the response contains an exception so the according error will be displayed in 
            error view. Otherwise the response contains the verdicts of the tests and will be shown 
            on the treeview.
            
            Note: The data is deserialized before displaying it on the view.
        """   
       
        # On vérifie si le TopLevelRespone reçu est envoyé par le l1test_backend 
        if msg.get("command_name") == BACKEND_COMMAND:
            verdicts, error_msg = None, ErrorMsg(title=None, msg=None)
           
            self.clean_error_view()         
            # We check if the backend encountered an exception
            if msg.get(L1TEST_EXCEPTION):
                error_msg = self.__handle_raised_exception(msg.get(L1TEST_EXCEPTION))
            
            if not self.is_pending() and self.is_running():
                self.clean_treeview()
                
                l1test_treeview:L1TestTreeView = self._reporter.get_l1test_treeview()
                l1test_treeview.enable_menu()    
                
                if msg.get(VERDICTS): # We check if the response contains the "verdicts" attribute 
                    self.set_has_exception(False)
                    received_verdicts = msg.get(VERDICTS)

                    # deserialization of the data
                    verdicts:dict[str, list[Test]] = pickle.loads(received_verdicts)                    
                    log_in_thonny(verdicts, eval(os.environ.get(IS_SELECTED_VAR)))
            self.show_right_view(verdicts=verdicts, error_msg=error_msg.msg, error_title=error_msg.title)
        else:
            # Le TopLevelReponse reçu ne nous intéresse pas.
            return 
        # On indique l'état de l'execution du la commande comme terminée
        self.terminate_running()
    
    def show_verdicts(self, test_results:dict[ast.AST, list[Test]]):
        """
        Report the verdicts on the view.

        Args:
            test_results (dict): The recieved verdicts from the backend.
        """
        self._reporter.display_tests_results(test_results) 
    
    def __handle_raised_exception(self, exception: dict) -> ErrorMsg:
        """
        This function handles the raised exception by returning a tuple containing
        a prefix message and the exception message.

        The prefix refers to the title shown on the ErrorView. If you want to remove 
        the title, you should specify the prefix as an empty string. If you don't 
        want to change the title, you should specify the prefix as `None`.
         
        Args:
            exception (dict): The exception to handle.

        Returns:
            ErrorMsg: a couple that indicates a prefix message and the exception message.
        """
        if exception.get("type_name") == InterruptedError.__name__:
            self.set_has_exception(False)  # ce n'est pas une erreur
            self.clean_treeview()
            
            return ErrorMsg(title=None, msg=None)    # On fait rien.
        
        self.set_has_exception(True)   # on indique l'état de l'execution
        
        # The backend exceptions inherit from the BackendException class
        backend_exceptions = self.__get_all_backend_exceptions()
        
        for backend_exception in backend_exceptions:                
            if (exception.get("type_name") == backend_exception.__name__) :
                return ErrorMsg(exception.get("prefix"), exception.get("message")) 
        
        # si on est là alors l'exception levée n'est pas une exception backend est
        # c'est probablement une exception levée par python.
        return ErrorMsg(title=exception.get("prefix"), 
                        msg="%s:\n%s" % (exception.get("type_name"), exception.get("message")))
    
    def __get_all_backend_exceptions(self) -> list[BackendException]:
        """
        All the exceptions (specifc to l1test) raised on the backend 
        inherit from the `BackendException` class.
        
        Gets dynamically the exceptions inherit from the `BackendException` class that
        are declared in the `exceptions.py` module.

        Returns:
            list[BackendException]: Returns a list of the backend exception classes.
        """
        import thonnycontrib.exceptions as exceptions
        backend_exceptions = []
        for name, obj in inspect.getmembers(exceptions):
            if inspect.isclass(obj) and issubclass(obj, exceptions.BackendException):
                backend_exceptions.append(obj)
        return backend_exceptions
    
    def show_errors(self, exception_msg, title=None):
        title = CANNOT_RUN_TESTS_MSG if title is None else title
        self._reporter.display_error_msg(exception_msg, title=title)    
    
    def _on_restart_backend(self, event: WorkbenchEvent):
        """
        This function is called when the backend of thonny is restared. The restarting
        of the backend generates a `BackendRestart` event and this event can 
        be generated either by  the red `Stop/Restart backend` button in Thonny's 
        toolbar or by invoking a new command. 
        
        When a new command is called in Thonny it triggers a partial restart
        of the backend before processing the command. Thonny does this to stop
        the current process and start a new process for the new command.

        This function tries to verify if the backend is restarted by clicking the red button
        or by invoking the `l1test_command`. 
            - if the backend is restarted by clicking the red button, so the treeview is cleaned.
            - if the backend is restarted by invoking the `l1test_command`, so we show in the
            treeview that the l1test is being executed.
            - if the backend is restarted by invoking an other command, so nothing is done.
        
        The problem is that we cannot know who generates the `BackendRestart` event. So to know 
        if the `BackendRestart` event is generated by the `l1test_command` we use the attribute 
        `self._is_l1test_running`. This attribute was setted to True before sending the 
        `l1test_command` to the backend.
        
        Args:
            event (WorkbenchEvent): The event generated from backend restart.
        """
        if (event.get("sequence") == BACKEND_RESTART_EVENT):   
            # Quand le backend est redémarré on efface les exceptions récemment affichée par l1test 
            self.set_has_exception(False)
            self.clean_error_view() 

            # L'attribut "full" est un boolean, si c'est "True" alors le backend procède a un
            # redémarrage complet (c'est le cas quand on appuit sur le bouton rouge Stop/Restart).
            # Si c'est False alors c'est un redémarrage partiel du backend (c'est le cas d'un appel 
            # d'une nouvelle commande).
            if event.get("full"):
                self.terminate_running()
                self.clean_treeview()          
            else:       
                # on vérifie si le l1test a été invoqué
                if self.is_running(): 
                    self.clean_treeview()
                else: # probablement une autre commande a déclenché le Restart du backend -> on fait rien
                    pass
        self.show_right_view()
      
    def show_right_view(self, event:WorkbenchEvent=None, verdicts=None, error_msg:str=None, error_title:str=None, both=False):
        """
            Displays either the L1TestTreeView or the L1TestErrorView. 
            It depends on the execution state of the l1test plugin. 
            
            If an error was raised by the plugin then only the Error view will be displayed.
        """
        if event and event.get("sequence") == L1TREE_VIEW_EVENT:
            possible_keys = ["sequence", "has_exception", "both", "verdicts", "error_msg", "error_title"]
            assert any(key in possible_keys for key in event.__dict__.keys())
            if event.get("has_exception") != None:
                has_exception = event.has_exception
                self._has_exception = has_exception
            if event.get("verdicts") != None:
                verdicts = event.verdicts
            if event.get("error_msg") != None:
                error_msg = event.error_msg 
            if event.get("error_title") != None: 
                error_title = event.error_title
            if event.get("both") != None: 
                both = event.both
        if (self._has_exception):
            if error_msg:
                self.show_errors(exception_msg=error_msg, title=error_title)
            if not both:
                self._reporter.get_l1test_treeview().hide_view()
            else:
                self._reporter.get_l1test_treeview().show_view()
            self._reporter.get_l1test_error_view().show_view()
        else:
            self.clean_error_view()
            if verdicts:
                self.show_verdicts(verdicts)
            if not both:
                self._reporter.get_l1test_error_view().hide_view()
            else:
                self._reporter.get_l1test_error_view().show_view()
            self._reporter.get_l1test_treeview().show_view()
       
    def clean_error_view(self):
        self._reporter.get_l1test_error_view().clear()
               
    def clean_treeview(self, all=True): 
        self._reporter.get_l1test_treeview().clear_tree(clear_all=all)
         
    def set_is_running(self, value=True):
        self._is_l1test_running = value
    
    def is_running(self):
        return self._is_l1test_running
    
    def is_pending(self):
        return self._is_pending
    
    def set_pending(self, is_pending:bool):
        self._is_pending = is_pending
    
    def set_has_exception(self, has_exception:bool):
        self._has_exception = has_exception
    
    def has_exception(self):
        return self._has_exception
    
    def terminate_running(self):
        """
        Set the state of `L1TestRunner` as terminated.
        This function sets the `_is_l1test_running` attribute to False
        """
        self.set_pending(False)
        self.set_is_running(False)
        
    def get_reporter(self) -> L1TestReporter:
        return self._reporter
    
    def set_reporter(self, reporter):
        self._reporter = reporter