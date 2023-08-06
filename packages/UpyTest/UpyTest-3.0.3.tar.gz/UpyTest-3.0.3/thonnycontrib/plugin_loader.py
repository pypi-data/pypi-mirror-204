import os, os.path
from thonny import get_workbench
from thonny.editors import  EditorNotebook
from thonny import editors
from thonny.ui_utils import select_sequence
from thonnycontrib.outlines import get_outliner, run_outlined_test
from .docstring_generator.doc_generator import DocGenerator
from .l1test_frontend.l1test_reporter import L1TestErrorView, L1TestTreeView
from .exceptions import *
from .properties import  ERROR_VIEW_LABEL, PLUGIN_NAME, CANNOT_GENERATE_THE_DOCSTRING
from .utils import (
    get_focused_writable_text,
    get_selected_line, 
    send_to_backend, 
    assert_one_line_is_selected
)
from .l1test_configuration import l1test_options
from .l1test_frontend import get_l1test_runner
from .environement_vars import *
from thonny.editors import EditorCodeViewText

def run_all_tests():
    """
    Cette fonction est invoquée quand le button `l1test` est cliqué.
    Cette fonction permet d'envoyer au l1test_backend la commande L1test.
    """
    _send_to_l1test_backend()

def update_test_for_one_menu(event):
    editor = get_workbench().get_editor_notebook().get_current_editor()
    if editor is None:
        return
    source = editor.get_code_view().get_content()
    
    outliner = get_outliner()
    outliner.from_outlines_post_menu(source)

def run_selected_test():
    """
    Cette fonction est invoquée quand le button `Run test for selected function`
    suite à un clique droit sur une ligne du fichier.
    Cette fonction permet d'envoyer au l1test_backend la commande L1test avec en argument
    is_selected=True.
    
    Raises:
        CannotSelectSeveralLines: si plusieurs lignes sont séléctionnées.
    """
    try:
        assert_one_line_is_selected()
        lineno = get_selected_line(get_focused_writable_text())
        _send_to_l1test_backend(is_selected=True, selected_line=lineno)
    except CannotSelectSeveralLines as e:
        l1test_runner = get_l1test_runner()
        l1test_runner.set_has_exception(True) 
        l1test_runner.clean_error_view()
        l1test_runner.show_right_view(error_msg=str(e))

def _send_to_l1test_backend(is_selected: bool=False, selected_line: int=0):
    """
        Send a command to the l1test_backend.
        Args:
            is_selected (bool): Set as True if only one method is selected to run
                            it's tests.
            test_only (bool): Set as True to run only the decorated(with @test_only) methods.
    """
    l1test_runner = get_l1test_runner()
    try:
        editor: EditorNotebook = get_workbench().get_editor_notebook()
        # si aucun editeur n'est ouvert sur le workbench
        if not editor.get_current_editor():
            raise NoEditorFoundException("No editor found !\n\nPlease open an editor before running the tests.")
        
        # cette ligne demande de sauver le fichier s'il n'a pas encore été sauvé sur
        # la machine. Si le fichier est déjà sauvé, il va permettre d'enregistrer la nouvelle
        # version du fichier.
        filename = editors.get_saved_current_script_filename(force=True)
        
        # si le filename est null alors le fichier n'a  pas été sauvé sur machine.  
        # Ce cas survient quand l'utilisatur quitte la fenetre de sauvegarde sans sauver le fichier.
        if not filename: 
            msg = "The file is not saved.\n\nConsider to save the file before running the tests."
            raise NotSavedFileException(msg)

        if not editor.get_current_editor_content().strip():  # L'éditeur est vide. 
            # on a pas envie d'envoyer une commande au backend si le fichier est vide.
            # Dans tous les cas y a rien à tester.
            raise EmptyEditorException("The editor is empty!\n")
        
        # si on est là alors le fichier est bien sauvegardé et contient quelque chose.
        l1test_runner.set_is_running()
        
        send_to_backend(is_selected=is_selected, selected_line=selected_line)
    except FrontendException as e: # on catche que les exception coté view
        l1test_runner.terminate_running()
        l1test_runner.set_has_exception(True) 
        l1test_runner.clean_error_view()
        l1test_runner.show_right_view(error_msg=str(e))
       
def generate_auto_docstring(event): 
    if _writable_text_is_focused(): # on vérifie si la zone séléctionnée est une zone de l'éditeur
        if l1test_options.get_option(l1test_options.AUTO_GENERATON_DOC): 
            text_widget = get_focused_writable_text()
            lineno = get_selected_line(text_widget) - 1
            __generate_docstring(lineno, text_widget)
            
    # Le return est important car il annule l'effet par défaut de saut de ligne. 
    # See : https://stackoverflow.com/questions/22907200/remap-default-keybinding-in-tkinter
    return "break"

def generate_manual_docstring():
    text_widget = get_focused_writable_text()
    lineno = get_selected_line(text_widget)
    __generate_docstring(lineno, text_widget)

def __generate_docstring(selected_lineno:int, text_widget:EditorCodeViewText):
    l1test_runner = get_l1test_runner()
    error_msg, error_title, both = None, None, False
    try:
        filename = get_workbench().get_editor_notebook().get_current_editor().get_filename()
        if not filename:
            filename = "<unknown>" 
        
        assert_one_line_is_selected(text_widget)
        
        # get the content of the selected line
        selected_sig = text_widget.get(str(selected_lineno)+".0", str(selected_lineno+1)+".0").strip("\n")
 
        docGenerator = DocGenerator()
        docGenerator.set_filename(filename)
        docGenerator.generate(selected_sig, selected_lineno, text_widget)    
        
        # si generate réussi on déclare comme quoi y'a pas d'erreur pendant la génération
        l1test_runner.set_has_exception(False)
    except NoFunctionSelectedToDocumentException as e:
        both = True
        if not l1test_runner.has_exception():
            both = False
            l1test_runner.set_has_exception(False)
        pass # Do nothing. We don't generate anything if a selected line is not a function.
    except FrontendException as e: # parsing error
        l1test_runner.set_has_exception(True)
        error_msg, error_title = str(e), CANNOT_GENERATE_THE_DOCSTRING    
              
    l1test_runner.show_right_view(error_msg=error_msg, error_title=error_title, both=both)           
    # Cette ligne est importante pour reprendre le focus sur l'éditeur
    get_workbench().get_editor_notebook().focus_set() 
    
    del docGenerator  # destruction de l'objet en mémoire (for better performance)
    
def _writable_text_is_focused():
    """
    Returns:
        boolean: Returns True if the selected zone is a writable text.
    """
    return get_focused_writable_text() is not None


def __init_l1test_options():
    l1test_options.init_options()
    get_workbench().add_configuration_page(PLUGIN_NAME, PLUGIN_NAME, 
                                           l1test_options.plugin_configuration_page, 30)

def __init_l1test_views():
    get_workbench().add_view(L1TestTreeView, PLUGIN_NAME, "nw", visible_by_default=True)
    get_workbench().add_view(L1TestErrorView, ERROR_VIEW_LABEL, "sw", visible_by_default=False)

def __init_l1test_commands():
    # Création du button l1test au niveau de la barre des commandes
    get_workbench().add_command(command_id=PLUGIN_NAME,
                                menu_name=PLUGIN_NAME,  
                                command_label="Run all tests",
                                handler=run_all_tests,
                                include_in_toolbar=True, #j'inclue ici ce bouton dans la toolbar 
                                image=os.path.join(os.path.dirname(__file__), "docs/res", "l1test_icon.png"),
                                caption=PLUGIN_NAME)
    
    # Création du button L1Test dans la barre de menu en haut.  
    get_workbench().add_command(command_id="Run one test",
                                menu_name=PLUGIN_NAME,  
                                command_label="Run tests for ...",
                                handler=run_outlined_test, 
                                submenu=get_outliner().get_menu()
    )
    
    # Création du bouton dans le menu 'Edit' pour lancer un seul test d'une seul foncton
    get_workbench().add_command(command_id="function test",
                                menu_name="edit",  
                                command_label="Run test for selected function",
                                handler=run_selected_test,
                                tester=_writable_text_is_focused,
    )
    
    # Création du bouton dans le menu 'Edit' pour lancer la génération de docstring
    get_workbench().add_command(command_id="doc_generator",
                                menu_name="edit",  
                                command_label="Generate a docstring",
                                handler=generate_manual_docstring, 
                                tester=_writable_text_is_focused,
                                default_sequence=select_sequence("<Alt-d>", "<Command-Alt-d>", "<Alt-d>"),
                                accelerator="Alt+d"
    )

def __add_event_binding():
    # Quand un saut de ligne est réalisé après la déclaration d'une fonction,
    # alors une docstring sera générée automatiquement.
    get_workbench().bind_class("EditorCodeViewText", "<KeyRelease-Return>", generate_auto_docstring)
    get_workbench().bind("<<RunOneTest>>", update_test_for_one_menu, True)

def load_plugin():
    """
    load_plugin est un nom de fonction spécifique qui permet à thonny de charger les élements du plugin
    """
    __init_l1test_options()
    __init_l1test_views()    
    __init_l1test_commands()
    __add_event_binding()