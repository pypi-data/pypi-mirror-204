from seleniumbase import BaseCase

from tests.end2end.end2end_test_setup import End2EndTestSetup
from tests.end2end.helpers.components.toc import TOC
from tests.end2end.helpers.components.viewtype_selector import (
    ViewType_Selector,
)
from tests.end2end.helpers.screens.document_tree.screen_document_tree import (
    Screen_DocumentTree,
)
from tests.end2end.server import SDocTestServer


class Test_UC112_T02_UI_toc_saves_state(BaseCase):
    def test_01(self):
        test_setup = End2EndTestSetup(path_to_test_file=__file__)

        with SDocTestServer(
            input_path=test_setup.path_to_sandbox
        ) as test_server:
            self.open(test_server.get_host_and_port())

            screen_document_tree = Screen_DocumentTree(self)

            # start: on the document tree
            screen_document_tree.assert_on_screen()

            # go to document
            screen_document = screen_document_tree.do_click_on_first_document()
            screen_toc: TOC = screen_document.get_toc()

            viewtype_selector = ViewType_Selector(self)

            # toc is on the document view, opened
            screen_document.assert_on_screen_document()
            screen_toc.assert_toc_opened()

            # go to table view
            screen_table = viewtype_selector.do_go_to_table()

            # toc is on the table view, opened
            screen_table.assert_on_screen_table()
            screen_toc.assert_toc_opened()

            # hide the toc
            screen_toc.do_toggle_toc()

            # toc is on the table view, closed
            screen_table.assert_on_screen_table()
            screen_toc.assert_toc_closed()

            # go back to document view
            screen_document = viewtype_selector.do_go_to_document()
            # toc is on the document view, closed
            screen_document.assert_on_screen_document()
            screen_toc.assert_toc_closed()

            # show the toc
            screen_toc.do_toggle_toc()

            # toc is open
            screen_document.assert_on_screen_document()
            screen_toc.assert_toc_opened()

        assert test_setup.compare_sandbox_and_expected_output()
