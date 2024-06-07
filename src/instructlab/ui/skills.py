"""
Tool to explore and set skills

Run with:

    python skills.py PATH
"""

import sys

from rich.syntax import Syntax
from rich.json import JSON
from rich.traceback import Traceback

from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll, Horizontal, Vertical
from textual.reactive import var
from textual.widgets import DirectoryTree, Footer, Header, Static, Input, Label, TextArea, TabbedContent, TabPane, Button, Tree
from textual.widgets.tree import TreeNode

class SkillsBrowser(App):
    """SkillsBrowser"""

    BINDINGS = [
        ("f", "toggle_files", "Toggle Files"),
        ('v', "view_file", "View content"),
        ("q", "quit", "Quit")
    ]

    show_tree = var(True)

    # TODO: export to css file
    CSS = '''
        #tree-view {
            max-width: 100%;
        }

        #content-zone {
            max-width: 100%;
        }
        #tree-zone {
            max-width: 30%;
        }
        
        #add-skills  {
            max-width: 100%;
        }

    '''

    def __init__(self, location: str) -> None:
            self.path = location
            super().__init__()

    def watch_show_tree(self, show_tree: bool) -> None:
        """Called when show_tree is modified."""
        self.set_class(show_tree, "-show-tree")

    def compose(self) -> ComposeResult:
        """Compose our UI."""
        path = "./" if len(sys.argv) < 2 else sys.argv[1]
        # yield Header()
        with Horizontal():
            with Vertical(id="tree-zone"):
                yield DirectoryTree(path, id="tree-view")
                yield Button("add skills",id='add-skills')
            with Container(id="content-zone"):
                with TabbedContent(initial=""):
                    with TabPane("content", id="content"):  # main tab
                        yield Input(placeholder="task_description:", type="text")
                        yield Input(placeholder="created_by:", type="text")
                        # TODO: use Collapsible
                        with Container():
                            yield Label('question:')
                            yield TextArea()
                            yield Label('context:')
                            yield TextArea()
                            yield Label('answer:')
                            yield TextArea()
                    with TabPane("add example", id="add-example"):  # main tab
                        yield Input(placeholder="task_description:", type="text")
                        yield Input(placeholder="created_by:", type="text")
                        # TODO: use Collapsible
                        with Container():
                            yield Label('question:')
                            yield TextArea()
                            yield Label('context:')
                            yield TextArea()
                            yield Label('answer:')
                            yield TextArea()
                    with TabPane("YAML", id="YAML"):  # secondary tab
                        with VerticalScroll(id="code-view"):
                            yield Static(id="code", expand=True)
        yield Footer()

    def on_mount(self) -> None:
        print(self.path)
        self.query_one(DirectoryTree).path=self.path
        self.query_one(DirectoryTree).focus()

    def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        event.stop()
        code_view = self.query_one("#code", Static)
        try:
            syntax = Syntax.from_path(
                str(event.path),
                line_numbers=True,
                word_wrap=False,
                indent_guides=True,
                theme="github-dark",
            )
        except Exception:
            code_view.update(Traceback(theme="github-dark", width=None))
            self.sub_title = "ERROR"
        else:
            code_view.update(syntax)
            self.query_one("#code-view").scroll_home(animate=False)
            self.sub_title = str(event.path)

    def action_toggle_files(self) -> None:
        """Called in response to key binding."""
        self.show_tree = not self.show_tree

if __name__ == "__main__":
    # TODO: read from config
    location = "../../../../taxonomy/compositional_skills/"
    SkillsBrowser(location).run()


    # template = """
    # created_by:
    # seed_examples:
    # - answer:' '
    # question:
    # task_description: ' '
    # """