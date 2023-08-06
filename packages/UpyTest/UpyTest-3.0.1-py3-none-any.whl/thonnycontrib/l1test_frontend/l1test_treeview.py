from thonny import  tktextext, ui_utils
from thonny.ui_utils import scrollbar_style
from thonnycontrib.utils import get_font_size_option, get_font_family_option
from .l1test_error_view import L1TestErrorView
from ..properties import *
from ..backend.verdicts.EmptyTest import EmptyTest
from ..backend.verdicts.ExceptionTest import ExceptionTest
from ..backend.verdicts.FailedTest import FailedTest
from ..backend.verdicts.Test import Test
from ..backend.verdicts.FailedWhenExceptionExpectedTest import *
from ..backend.verdicts.PassedTest import PassedTest
from ..utils import *
from functools import partial
from ..l1test_configuration.l1test_options import *
import os, tkinter as tk, tkinter.font as tk_font, thonny
from collections import namedtuple
from thonny.codeview import *
from collections import defaultdict
from typing import Dict, List

# La hauteur, par défault, d'une ligne dans une Treeview
ROW_HEIGHT  = 40

clickable_tag = "clickable"

# L'objet qui représente un summarize
Summarize = namedtuple('Summarize', ["total", "success", "failures", "errors", "empty"])

# Palette de couleurs utilisée par la treeview
COLORS:dict = { 'orange': '#e8770e',
                'red': 'red',
                'lightred': '#fcdbd9',
                'darkred': '#f7140c',
                'green': 'darkgreen',
                'blue': '#0000cc',
                'gray': 'gray'
            }

class L1TestTreeView(ttk.Frame):    
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master, borderwidth=0, relief="flat")
        self.workbench = thonny.get_workbench()
        
        self._init_treeview()
        
        self._origin_verdicts: Dict[ast.AST, List[Test]] = dict()
        self._copy_verdicts = self._origin_verdicts.copy()
        
        # Le binding est censé augmenter/diminuer automatiquement la taille de la treeview
        self.workbench.bind("<Control-plus>", self.__observe_font_changing, True)
        self.workbench.bind("<Control-minus>", self.__observe_font_changing, True)
            
    def _init_treeview(self):
        """
        Creates the treeview widget.
        """
        self.vert_scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, style=scrollbar_style("Vertical"))
        self.vert_scrollbar.grid(row=0, column=1, sticky=tk.NSEW, rowspan=3)
        
        self.init_header(row=0, column=0)
        
        spacer = ttk.Frame(self, height=1)
        spacer.grid(row=1, sticky="nsew")

        self.treeview = ttk.Treeview(self,yscrollcommand=self.vert_scrollbar.set)
        
        rows, columns = 2, 0
        self.treeview.grid(row=rows, column=columns, sticky=tk.NSEW)
        self.vert_scrollbar["command"] = self.treeview.yview
        self.columnconfigure(columns, weight=1)
        self.rowconfigure(rows, weight=1)
        
        # configure the only tree column
        self.treeview.column("#0", anchor=tk.W, stretch=tk.YES)
        
        # self.tree.heading('#0', text='Item (type @ line)', anchor=tk.W)
        self.treeview["show"] = ("tree",)

        for color_name, color in COLORS.items():
            if color_name == "lightred":
                self.treeview.tag_configure(color_name, background=color)
            else:
                self.treeview.tag_configure(color_name, foreground=color)
             
        self.treeview.tag_bind("clickable", "<<TreeviewSelect>>", self._on_select)
        self.treeview.tag_bind("nonClickable", "<<TreeviewSelect>>", self._remove_highlight_selection_effect)
        
        self.style = ttk.Style()
        self.style_mapping = self.style.map('Treeview')

        self.__update_tree_font(get_font_family_option(), get_font_size_option())
       
        # le chemin c'est par rapport au dossier /l1test 
        # donc il faut remonter vers /thonnycontrib/ pour rentrer dans docs/res
        parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        
        self.passed_icon = tk.PhotoImage(file=os.path.join(parent_dir, "docs/res", "passed.png"))
        self.failed_icon = tk.PhotoImage(file=os.path.join(parent_dir, "docs/res", "failed.png"))
        self.warning_icon = tk.PhotoImage(file=os.path.join(parent_dir, "docs/res", "warning.png"))
        self.pending_img = tk.PhotoImage(file=os.path.join(parent_dir, "docs/res", "pending_icon.png"))
        
        # add a menu to the treeview
        self.menu = tk.Menu(self.treeview, name="menu", tearoff=False)

        # Here we handle the motion event of the treeview
        self.treeview.bind("<Configure>", partial(self.__wrap_tree_content, self.treeview))
        self.selected_item = None
        
    # ------------------------------------
    # Fonctions pour le Header du treeview
    # ------------------------------------
    
    def init_header(self, row=0, column=0):
        """
        Initialize the header of the treeview. Initially, the header contains 
        only a `menu button` at the top right of the treeview. The options of the 
        menu are created by `post_button_menu()` method.

        Args:
            row (int): Always set to 0. Defaults to 0.
            column (int): Always set to 0. Defaults to 0.
        """
        header_frame = ttk.Frame(self, style="ViewToolbar.TFrame")
        header_frame.grid(row=row, column=column, sticky="nsew")
        header_frame.columnconfigure(0, weight=1)
        
        self.header_bar = tktextext.TweakableText(
            header_frame,
            borderwidth=0,
            relief="flat",
            height=1,
            wrap="word",
            padx=ui_utils.ems_to_pixels(0.6),
            pady=ui_utils.ems_to_pixels(0.5),
            insertwidth=0,
            highlightthickness=0,
            background=ui_utils.lookup_style_option("ViewToolbar.TFrame", "background"),
        )
        
        for color_name, color in COLORS.items():
            self.header_bar.tag_configure(color_name, foreground=color)
        
        self.header_bar.grid(row=0, column=0, sticky="nsew")
        self.header_bar.set_read_only(True)
        self.menu_button = ttk.Button(
                                header_frame, 
                                text=" ≡ ", 
                                style="ViewToolbar.Toolbutton", 
                                width=3,
                                command=self.post_button_menu
                            )
        self.header_bar.bind("<Configure>", self.resize_header_bar, True)
        self.header_bar.configure(height=1)

        self.menu_button.place(anchor="ne", rely=0, relx=1)
        self.disable_menu()
     
    def post_button_menu(self):
        """
            The handler of the menu button located in the header of the treeview.
            When clicking the menu button a popoup is opened and shows several options.
        """
        self.add_menu_options()
        self.menu.tk_popup(
            self.menu_button.winfo_rootx(),
            self.menu_button.winfo_rooty() + self.menu_button.winfo_height(),
        )
    
    def add_menu_options(self):
        """
            Adds the options inside the menu button.
        """
        self.menu.delete(0, "end") 
        
        self.menu.add_command(label=PLACE_RED_TEST_ON_TOP_LABEL, command=self.sort_by_red_tests)
        self.menu.add_command(label=RESUME_ORIGINAL_ORDER, command=self.remove_sort_filter)
        self.menu.add_separator() 
        self.menu.add_command(label=SHOW_ONLY_RED_TESTS, command=self.show_only_red_tests)
        self.menu.add_command(label=SHOW_ALL_TESTS, command=self.show_all_tests)
        self.menu.add_separator()
        self.menu.add_command(label=GROUP_BY_VERDICTS, command=self.group_by_verdicts)
        self.menu.add_separator()    
        self.menu.add_command(label=EXPAND_TEST_RESULTS, command=self.expand_rows)
        self.menu.add_command(label=FOLD_TEST_RESULTS, command=self.fold_rows)
        self.menu.add_separator()
        self.menu.add_command(label=UPDATE_FONT_LABEL, command=self.update_font)
        self.menu.add_command(label=REDUCE_SPACE_BETWEEN_ROWS, command=self.reduce_space_between_rows)
        self.menu.add_command(label=REMOVE_ERROR_DETAILS if not get_option(EXCEPTION_DETAIL) else INCLUDE_ERROR_DETAILS, 
                              command=self.remove_error_details)
        self.menu.add_separator()
        self.menu.add_command(label=CLEAR_LABEL, command=self.clear_tree) 
         
    def resize_header_bar(self, event=None):
        """
            Resize the height of the header.
            Always keep this method otherwise the header will take the whole treeview.
        """
        height = self.tk.call((self.header_bar, "count", "-update", "-displaylines", "1.0", "end"))
        self.header_bar.configure(height=height)

    def update_font(self, event=None):
        """
            This is the handler of the `Update the font` option. The handler inserts the 
            time when the treeview was refreshed. 
            
            It also update the font size of the treeview if and 
            only if the font is changed in thonny.
            
            Note : if a row of the treeview is selected so the effect of the selection will 
            be removed after refresh.
        """
        all_childs = get_all_tree_childrens(self.treeview)
        rowheight = ROW_HEIGHT
        if all_childs:
            # on calcule le meilleure height à appliquer pour la treeview.
            # Cela est fait quand la taille de la police a changé dans thonny.
            rowheight = self.get_optimal_row_height(self.treeview, all_childs)
                     
        self.resize_header_bar()
        # on applique la nouvelle police pour la treeview
        self.__observe_font_changing(rowheight=rowheight)
    
    def sort_by_red_tests(self):
        priority = Test._FAILED_STATUS
        # On filtre que les noeuds qui ont au moins un test rouge.
        sorted_failed_nodes = {node: results for node, results in self._copy_verdicts.items() \
                                    if priority in self.__deduce_global_node_verdict(node, results).keys()
                            } 
        
        # On met les tests rouges en haut et cela pour tous les noeuds AST qui ont au moins un test rouge.
        sorted_failed_tests = {node: sorted(results, key=lambda x: isinstance(x, (FailedTest, ExceptionTest)), reverse=True) \
                                    for node, results in sorted_failed_nodes.items() \
                                        if priority in self.__deduce_global_node_verdict(node, results).keys() 
                            }
        
        # On récupère les autres neouds AST 
        others = {node: results for node, results in self._copy_verdicts.items() \
                                    if priority not in self.__deduce_global_node_verdict(node, results).keys()
                } 
         # l'addition de tous les noeuds
        sorted_failed_tests.update(others)

        if self.treeview.get_children(): # on met à jour que si la treeview possède des éléments
            self._copy_verdicts = sorted_failed_tests
            self.update_tree_contents(sorted_failed_tests)
    
    def remove_sort_filter(self):
        """
        When invoking this method the treeview will restore 
        the original order of its rows.
        """
        def __is_verdicts_copy_equals_to_original():
            if len(self._copy_verdicts) != len(self._origin_verdicts):
                return False
            for o_node, o_tests in self._origin_verdicts.items():
                c_tests = self._copy_verdicts[o_node]
                if len(o_tests) != len(c_tests): 
                    return False 
            return True
        if self.treeview.get_children(): # on met à jour que si la treeview possède des éléments
            if __is_verdicts_copy_equals_to_original():
                self._copy_verdicts = self._origin_verdicts
            self.update_tree_contents(self._copy_verdicts)
    
    def show_only_red_tests(self):
        red_verdicts = (Test._FAILED_STATUS, Test._EXCEPTION_STATUS)
        
        only_reds = {}
        for node, tests in self._copy_verdicts.items():
            red_tests = []
            for test in tests:
                if test.get_status() in red_verdicts:
                    red_tests += [test]
            if red_tests:
                only_reds[node] = red_tests
                            
        if self.treeview.get_children(): # on met à jour que si la treeview possède des éléments
            self._copy_verdicts = only_reds
            self.update_tree_contents(only_reds)
     
    def show_all_tests(self):
        self._copy_verdicts = self._origin_verdicts
        self.update_tree_contents(self._copy_verdicts)
    
    def __group_by_verdicts(self, verdicts: dict[ast.AST, List[Test]], status_order: List[str]=None) :
        """
        Group verdicts by status and order the statuses according to the provided 
        status order.
        
        :param status_order: A list of strings that specifies the order 
        in which to group the verdicts by status.
        :return: A dictionary of verdicts grouped by status.
        """
        status_groups = {}
        for ast_node, verdict_list in verdicts.items():
            for verdict in verdict_list:
                status = verdict.get_status()
                if status not in status_groups:
                    status_groups[status] = {}
                if ast_node not in status_groups[status]:
                    status_groups[status][ast_node] = []
                status_groups[status][ast_node].append(verdict)

        if status_order is None:
            status_order = Test.get_statutes_by_priority()
        
        # mettre en ordre les catégories selon l'ordre défini par le paramètre `status_order`
        ordered_groups = {}
        for status in status_order:
            if status in status_groups:
                ordered_groups[status] = status_groups[status]
        status_groups = ordered_groups
        
        return status_groups
    
    def group_by_verdicts(self): 
        grouped = self.__group_by_verdicts(self._origin_verdicts)
        if self.treeview.get_children(): # on met à jour que si la treeview possède des éléments
            self.clear_tree(clear_all=False) 
            for status, verdicts in grouped.items():
                open = False
                if status in (Test._EXCEPTION_STATUS, Test._FAILED_STATUS) and verdicts:
                    open = True
                row_id = self.insert_row(text=status, open=open, tags=())
                self.__add_verdicts_to_treeview(verdicts, row_id)
    
    def expand_rows(self): 
        """Spreads only the node rows"""
        self.__apply_row_change(False)
    
    def fold_rows(self):
        """Folds only the node rows"""
        self.__apply_row_change(True)
    
    def __apply_row_change(self, to_fold:bool):
        """Depending on the `to_fold` it folds or spreads the rows that
        correspond to the ast nodes.
         
        - If `to_fold` is True, the ast nodes are folded.
        - If `to_fold` is False, the ast nodes are expanded.

        Args:
            to_fold (bool): set to True to fold the rows that correspond
            to the ast nodes. Set to False to expand the rows that correspond
            to the ast nodes.
        """
        if self.treeview.get_children(): # on met à jour que si la treeview possède des éléments
            from copy import copy
            # on sauvegarde la valeur initiale de l'option GLOBAL_VIEW
            initial_val = copy(get_option(GLOBAL_VIEW))
            # on applique la nouvelle valeur de l'option `GLOBAL_VIEW`
            set_option(GLOBAL_VIEW, to_fold)
            # update_tree invoque dynamiquement la valeur de l'option(`GLOBAL_VIEW`) courante
            self.update_tree_contents(self._copy_verdicts)
            # on restaure la valeur initiale de l'option ??!
            # set_option(GLOBAL_VIEW, initial_val)
    
    def remove_error_details(self):
        if self.treeview.get_children():
            should_report = get_option(EXCEPTION_DETAIL)
            set_option(EXCEPTION_DETAIL, not should_report)
            if not should_report:
                error_view:L1TestErrorView = self.workbench.get_view(L1TestErrorView.__name__)
                error_view.clear()
                error_view.hide_view()
            self.update_tree_contents(self._copy_verdicts)
            
    def reduce_space_between_rows(self):
        all_childrens = get_all_tree_childrens(self.treeview)
        all_texts = self.__extract_wrapped_texts(self.treeview, all_childrens)
        max_lines = self.__get_longest_wrapped_line(all_texts)
        current_height = self.__compute_optimal_height(max_lines, margin=0.66, padding=1.5)
        self.style.configure("Treeview", rowheight=current_height)
        
    # -------------------------------------------
    # Fin des fonction pour le Header du treeview
    # -------------------------------------------
    
    def __observe_font_changing(self, event=None, rowheight=ROW_HEIGHT):
        """
            Changes the font of the treeview.
        """
        self.__update_tree_font(get_font_family_option(), 
                                get_font_size_option(), 
                                rowheight=rowheight)
        #self.header_bar.config(font=(get_font_family_option(), 
        #                             get_font_size_option()))
        return "break"
    
    def __update_tree_font(self, font_family, font_size, rowheight=ROW_HEIGHT):
        """
            Applies the new font to the treeview.
        """
        self.style.configure("Treeview", 
                             justify="left", 
                             rowheight=rowheight, 
                             font=(font_family, font_size), 
                             wrap=tk.WORD)  
    
    def __wrap_tree_content(self, tree: ttk.Treeview, event):
        """
            This function wraps the text of treeview to follow its width.
        """
        widget = event.widget if event else tree
        
        if (isinstance(widget, ttk.Treeview)): 
            if (self.workbench.get_view(self.__class__.__name__).winfo_ismapped()):  
                if not self.is_treeview_cleared():
                    width = widget.winfo_width()
                    
                    # Une heuristique a été fait pour décider du nombre de caractères par 100 pixels.
                    chars_per_100_pixels = width // (get_font_size_option()-2)
                    
                    all_childrens = get_all_tree_childrens(self.treeview)
                    for iid in all_childrens:
                        text = widget.item(iid)["text"]
                        wrapped = wrap(text, chars_per_100_pixels)   
                        tree.item(iid, text=wrapped)
                    # il faut changer la hauteur des rows pour afficher tout le texte
                    new_height = self.get_optimal_row_height(widget, all_childrens)
                    self.style.configure("Treeview", rowheight=new_height)
    
    def __extract_wrapped_texts(self, widget: ttk.Treeview, all_childrens:list):
        """
            Returns a list containing all the wrapped texts of all nodes of the treeview.
        """
        return [widget.item(iid)["text"] for iid in all_childrens]
    
    def get_optimal_row_height(self, widget: ttk.Treeview, all_childrens:list):
        """
            Returns the new optimal height.
        """
        all_texts = self.__extract_wrapped_texts(widget, all_childrens)
        
        # Quand le contenu est wrappé, on ajuste la hauteur des lignes, 
        # pour s'assurer que tout le contenu d'une ligne est affichée
        max_lines = self.__get_longest_wrapped_line(all_texts)
        return self.__compute_optimal_height(max_lines)        
        
    def __get_longest_wrapped_line(self, all_texts:list[str]):
        """
            Returns the longest wrapped text in the treeview.
        """ 
        sizes:list = [len(text.split("\n")) for text in all_texts]
        return max(sizes) if sizes else 1
    
    def __compute_optimal_height(self, max_lines:int=None, margin=0.8, padding=1.55):
        """
            Uses the default font metrics to calculate the optimal row height.
            The default font metrics is multiplied by the given `max_lines`.
            
            The algorithm uses heuristics to calculate the optimal height by eliminating 
            unnecessary padding between rows of the tree as much as possible. 
            
            Args:
                max_lines(int): The number of lines of the longest row in the treeview.
            Return:
                (int): The new height.
        """
        default_font = tk_font.nametofont("TkDefaultFont")
        font_size = round(default_font.metrics("linespace") * padding) * margin 
        lines_per_row = max_lines * font_size if max_lines else font_size
        return round(lines_per_row)
    
    def update_tree_contents(self, results:dict, parent="", full_clear=True):
        """
            This function contructs and inserts the rows into the treeview.
        """
        def __update_tree_header__():            
            # We build the summarize object 
            summarize: Summarize = self.build_summarize_object(self._origin_verdicts)
            # We insert the summarize infos into the header bar of the treeview
            self.insert_summarize_in_header_bar(summarize, self.header_bar)
            self.resize_header_bar()
        
        self._show_highlight_selection_effect()   
        self.clear_tree(clear_all=full_clear)
   
        if not self.__check_if_editor_is_open():
            return

        self.__add_verdicts_to_treeview(results, parent)
        
        if self.treeview.get_children():
            __update_tree_header__()
    
    def __add_verdicts_to_treeview(self, results:dict, parent=""):
        for node, verdicts in results.items():
            _tests = self._origin_verdicts[node]
            current_node = self._add_node_to_tree(node, _tests, parent)
            self._add_verdicts_to_node(current_node, verdicts)
        
        self.__wrap_tree_content(self.treeview, None)
        self.enable_menu()
    
    def _add_node_to_tree(self, node:ast.AST, tests:list[Test], parent=""):      
        self.__update_tree_font(get_font_family_option(), get_font_size_option())
                
        global_verdict = self.__deduce_global_node_verdict(node, tests)
        for _, verdict_config in global_verdict.items():
            return self.treeview.insert(parent, "end", values=node.lineno, 
                                        tags=(clickable_tag, ), **verdict_config)
    
    def _add_verdicts_to_node(self, current_node:str, tests:list[Test]):
        """ 
        This function adds to the treeview all the rows that correspond 
        to the given ast node.
        """
        def __add_as_many_rows_as_text_lines(parent, text:str, lineno:int, tags:str):
            """
            Adds the necessary rows of each text to be inserted in the treeview.
            An exception message can be reported on several line, so we should 
            add as many rows as text lines. 
            """
            splitted = text.split("\n")
            for line in splitted:
                self.treeview.insert(parent, "end", text=line, values=lineno, tags=tags) 
                
        # insert the sub-rows that represents the verdicts of the executed tests 
        # of the current AST node.
        for test in tests:
            item_text = " " + str(test)
            verdict_tags = (test.get_tag(), clickable_tag)
            if isinstance(test, FailedTest):
                current_test = self.treeview.insert(current_node, "end",  text=item_text, 
                                                    open=get_option(OPEN_RED_ROWS), 
                                                  values=test.get_lineno(), tags=verdict_tags)   
                if (isinstance(test, FailedWhenExceptionExpectedTest)):
                    # le detail d'une `failure` ne doit pas être cliquable
                    verdict_tags = (verdict_tags[0], "nonClickable")
                # a failure message can be reported on several line, so we should add as many rows as text lines. 
                __add_as_many_rows_as_text_lines(current_test, test.get_detail_failure(), test.get_lineno(), tags=verdict_tags)
            elif isinstance(test, ExceptionTest):
                extra_tags = ("lightred", ) if get_option(HIGHLIGHT_EXCEPTIONS) else ()
                current_test = self.treeview.insert(current_node, "end",  text=item_text, 
                                                    values=[test.get_lineno(), test.__class__.__name__, test.get_detail_failure()], 
                                                    tags=verdict_tags+extra_tags,
                                                    open=get_option(OPEN_RED_ROWS))
                # le detail d'une `exception` ne doit pas être cliquable
                error_detail_tags = (verdict_tags[0], "nonClickable")
                
                if not get_option(EXCEPTION_DETAIL):
                    __add_as_many_rows_as_text_lines(current_test, test.get_detail_failure(), test.get_lineno(), tags=error_detail_tags)               
            else :
                current_test = self.treeview.insert(current_node, "end", text=item_text, values=test.get_lineno(), tags=verdict_tags)
             
    def insert_row(self, parent="", text="", clear:bool=False, values=(), 
                   open=False, tags:str="", add_empty_line:bool=False):
        """
        Insert a simple row into the treeview. 

        Args:
            text (str): the text to insert. Defaults to "".
            clear (bool): if True the content of the treeview will be cleared before 
                        insert the text. Defaults to False.
            tags (str): any tags supported by the ttk.Treeview. Defaults to "".
            add_empty_line (bool): if True the text will be inserted after an 
                                empty line. Defaults to False.
        """
        if clear:
            self.clear_tree()
        if add_empty_line:
            self.treeview.insert("", "end", text="")    
        
        item = self.treeview.insert(parent, "end", text=text, open=open, tags=tags, values=values)
        self.__wrap_tree_content(self.treeview, None)
        return item
        
    def __check_if_editor_is_open(self) -> bool:
        """
            Returns True if an editor is already opened in thonny. 
            Otherwise, returns False 
        """
        return False if not self.workbench.get_editor_notebook().get_current_editor() else True
    
    def __deduce_global_node_verdict(self, node:ast.AST, tests: list[Test]):
        """
        Returns the status of a treeview node(ie. the row that represents the AST node).
        
        - If a node contains at least one Failure or one Exception verdict so `FAILED_STATUS`
        will be returned.
        
        - If a node contains only passed verdicts so a `PASSED_STATUS` for the current AST node 
        will be returned.
        
        - If none of the previous conditions is respected so a `WARNING_STATUS` wil be returned.

        Args:
            tests (list[Test]): The verdicts of an AST node.

        Returns:
            dict: a status of the ast node associated with some configs.
        """
        node_repr = " %s" % create_node_representation(node)   
        def _add_number_passed_tests():
            """
                Adds how many tests are executed of the current AST node
            """
            # The first space is necessary so that all text will be aligned
            return "%s ~%s passed~" %(node_repr, len([test for test in tests if test.get_status() == Test._PASSED_STATUS]))
        
        if any([test.get_status() in (Test._FAILED_STATUS, Test._EXCEPTION_STATUS) for test in tests]):
            return {Test._FAILED_STATUS: dict(text=_add_number_passed_tests(), image=self.failed_icon, open=not get_option(GLOBAL_VIEW))}
        elif all([test.get_status() == Test._PASSED_STATUS for test in tests]):
            return {Test._PASSED_STATUS: dict(text=_add_number_passed_tests(), image=self.passed_icon, open=False)}
        return {Test._EMPTY_STATUS: dict(text=node_repr, image=self.warning_icon, open=False)}

    def insert_summarize_in_header_bar(self, summarize:Summarize, view: tktextext.TweakableText):
        """
        Builds the summarize test to be inserted in the header of the treeview.
        
        Args:
            summarize (Summarize): a named tuple that contains the summarize infos.
        """
        tests_run = "Tests run: %s\n" % summarize.total
        view.direct_insert("end", tests_run)
        
        insert_label = lambda label, color : view.direct_insert("end", label, tags=(color,)) 
        insert_how_many = lambda how_many, is_last=False: view.direct_insert("end", f"{how_many}" if is_last else f"{how_many}, ")
      
        insert_label("Success: ", "green")
        insert_how_many(summarize.success)
        
        insert_label("Failures: ", "darkred")
        insert_how_many(summarize.failures)
        
        insert_label("Errors: ", "darkred")
        insert_how_many(summarize.errors)
        
        insert_label("Empty: ", "orange")
        insert_how_many(summarize.empty, is_last=True)
            
    def build_summarize_object(self, results:dict[ast.AST: List[Test]]) -> Summarize:
        """
        Builds the summarize informations. 
        The summarize contains :
            - Total number of executed tests.
            - How many succesed tests, failed tests, error tests, and empty tests.
        
        Args:
            results (dict): all the verdicts of all the AST nodes.

        Returns:
            Summarize: a namedtuple that represents the summarize object.
        """
        from collections import Counter
        # Count the number of tests of each type
        counts = Counter([t.get_status() for tests in results.values() for t in tests])
       
        # Get the counts for each type of test
        success = counts[Test._PASSED_STATUS]
        failures = counts[Test._FAILED_STATUS] 
        errors = counts[Test._EXCEPTION_STATUS]
        empty = counts[Test._EMPTY_STATUS]
        total = success + failures + errors
        return Summarize(total, success, failures, errors, empty)
                   
    def clear_tree(self, event=None, clear_all=True):
        """Clears the treeview by deleting all items. 
        
        Note: this method is also called when the button `clear` is clicked.
        
        Args:
            event: when the button `clear` is clicked the event is not None.
            clear_all: If True, the treeview and the header of the tree will be cleaned.
            if False, only the treeview will be cleaned.
        """
        # on supprime le contenu du header
        if clear_all:
            self.clear_header_bar()
        for child_id in self.treeview.get_children():
            self.treeview.delete(child_id)
        self.disable_menu()
        error_view:L1TestErrorView = self.workbench.get_view(L1TestErrorView.__name__)
        error_view.clear()

    def clear_header_bar(self):
        """Clears the header of the treeview."""
        if self.header_bar:
            self.header_bar.direct_delete("1.0", "end")
            self.resize_header_bar()
    
    def _remove_highlight_selection_effect(self, event=None):
        """
            This function remove the selection effect. When a treeview's row is selected
            it removes the highlight effect on the selected row. So the selected row 
            will look like it is not selected.
        """
        self.style.map('Treeview', background=[], foreground=[])
    
    def _show_highlight_selection_effect(self):
        """
            This function show the selection effect. When a treeview's row is selected
            it shows the highlight effect on the selected row. 
        """
        self.style.map('Treeview', 
                       background=[('selected', 'focus', '#ADD8E6'), ('selected', '!focus', '#ADD8E6')], 
                       foreground=[('selected', 'focus', 'black'), ('selected', '!focus', 'black')])
    
    def _highlight_line_on_editor(self, lineno, editor: CodeView):
        index = editor.text.index(str(lineno) + ".0")
        editor.text.see(index)  # make sure that the double-clicked item is visible
        editor.text.select_lines(lineno, lineno)
        
    def _on_select(self, event):
        """
            When a row is selected this function will be triggered. This function highlights 
            the line in the editor that corresponds to the seelcted row in the treeview. 
        """
        editor = self.workbench.get_editor_notebook().get_current_editor()
        self._show_highlight_selection_effect()
        if editor:
            code_view = editor.get_code_view()
            focus = self.treeview.focus()
            if not focus: 
                return

            item = self.treeview.item(focus)
            values = item["values"]
            if not values:
                return
            
            if focus == self.selected_item:
                # Item is already selected, so toggle the selection state
                if self.treeview.selection():
                    self.selected_item = None
                    self._remove_highlight_selection_effect()
                    self._highlight_line_on_editor(-1, code_view)
                    if get_option(EXCEPTION_DETAIL):
                        self.workbench.event_generate(L1TREE_VIEW_EVENT, has_exception=False)
                else:
                    self._show_highlight_selection_effect()
            else:
                # Item is not selected, so select it and remove the previous selection
                if self.selected_item:
                    self.selected_item = None
                    self._remove_highlight_selection_effect()
                    self._highlight_line_on_editor(-1, code_view)
                    if get_option(EXCEPTION_DETAIL):
                        self.workbench.event_generate(L1TREE_VIEW_EVENT, has_exception=False)
                
                self._show_highlight_selection_effect()
                self.selected_item = focus 
                
                if get_option(EXCEPTION_DETAIL): 
                    if ExceptionTest.__name__ in values:
                        self.workbench.event_generate(L1TREE_VIEW_EVENT, has_exception=True, both=True,
                                                    error_msg=values[-1], error_title=item["text"])
                           
                lineno = values[0]
                self._highlight_line_on_editor(lineno, code_view)
                self.workbench.event_generate(
                    "OutlineDoubleClick", item_text=self.treeview.item(self.treeview.focus(), option="text")
                )
  
    def disable_menu(self):
        """disable the menu button of the treeview"""
        self.menu_button.state([tk.DISABLED])
        
    def enable_menu(self):
        """enable the menu button of the treeview"""
        self.menu_button.state(["!disabled"])
     
    def insert_in_header(self, text, image=None, clear=False, tags=tuple()):
        """
        Insert in the header of the treeview a text. 
        If image is not None so the image will be added before the texte.
        """
        if clear:
            self.header_bar.direct_delete("1.0", tk.END)
        if image:
            self.header_bar.image_create(tk.END, image=self.pending_img)
            text = " " + text
        self.header_bar.direct_insert(tk.END, text, tags=tags)
        self.resize_header_bar()
           
    def is_treeview_cleared(self):
        return len(self.treeview.get_children()) == 0
    
    def is_header_bar_cleared(self): 
        return not self.header_bar.get("1.0", tk.END).strip("\n")    
    
    def hide_view(self):
        self.workbench.hide_view(self.__class__.__name__)
    
    def show_view(self):
        self.workbench.show_view(self.__class__.__name__)
        
    def set_verdicts(self, verdicts: dict):
        self._origin_verdicts = verdicts
        self._copy_verdicts = self._origin_verdicts.copy()
    
    def get_treeview(self):
        return self.treeview