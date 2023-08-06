from typing import List
import re
from thonny import get_workbench
from functools import partial
from .properties import PLUGIN_NAME
import tkinter as tk

_OUTLINE_REGEX = r"\s*(?P<type>def|class)[ ]+(?P<name>[\w]+)"

# Ceci est une implémentation de création d'un singleton pour OutlineParser
_outliner = None

class OutlinedNode():
    def __init__(self, type:str, name:str, lineno:int) -> None:
        self.__type = type
        self.__name = name
        self.__lineno = lineno
    
    def get_type(self):
        return self.__type  
    
    def get_name(self):
        return self.__name  
    
    def get_lineno(self):
        return self.__lineno    

class Outliner():   
    def __init__(self, workbench=get_workbench()) -> None:
        super().__init__()
        global _outliner
        _outliner = self
        
        workbench._init_menu()
        self.menu = tk.Menu(workbench.get_menu(PLUGIN_NAME)) 
        self.menu.event_add("<<RunOneTest>>", "<Button-1>")
     
    def __parse(self, source:str) -> List[OutlinedNode]:
        """
        Parses a source and returns a list of the outlined nodes. 
        The outlined nodes are either a class or a function. For 
        each outlined node an object of type `OutlinedNode` is built 
        in which we store the type (class/function), the name and the lineno
        of the outlined node.
        """
        outlines = []
        lineno = 0
        for line in source.split("\n"):
            lineno += 1
            match = re.match(_OUTLINE_REGEX,line) 
            if match:
                outlined = OutlinedNode(match.group("type"), match.group("name"), lineno)
                outlines.append(outlined)
        return outlines
    
    def from_outlines_post_menu(self, source):
        self.menu.delete(0, tk.END)
        outlines = self.__parse(source)
        for outline in outlines: 
            label = "%s %s" % (outline.get_type(), outline.get_name())
            self.menu.add_command(label=label, 
                                  command=partial(run_outlined_test, outline.get_lineno()),
                                  activebackground="white",
                                  activeforeground="darkblue")
    
    def get_menu(self):
        return self.menu
    
    
def run_outlined_test(lineno:int):
    """
    Cette fonction est invoquée quand le button `Run test for selected function`
    suite à un clique droit sur une ligne du fichier.
    Cette fonction permet d'envoyer au l1test_backend la commande L1test avec en argument
    is_selected=True.
    
    """
    from .plugin_loader import _send_to_l1test_backend
    _send_to_l1test_backend(is_selected=True, selected_line=lineno)


def get_outliner() -> Outliner:
    """
    Retourne une instance de `OutlineParser` en tant que singleton.
    """
    return Outliner() if not _outliner else _outliner