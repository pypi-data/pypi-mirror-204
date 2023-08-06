from seleniumbase import BaseCase

from tests.end2end.end2end_test_setup import End2EndTestSetup
from tests.end2end.helpers.constants import TEXT_WITH_TRAILING_WHITESPACES
from tests.end2end.helpers.screens.document.form_edit_requirement import (
    Form_EditRequirement,
)
from tests.end2end.helpers.screens.document_tree.screen_document_tree import (
    Screen_DocumentTree,
)
from tests.end2end.server import SDocTestServer


class Test_UC06_T08_SanitizeTrailingSymbols(BaseCase):
    def test_01(self):
        test_setup = End2EndTestSetup(path_to_test_file=__file__)

        with SDocTestServer(
            input_path=test_setup.path_to_sandbox
        ) as test_server:
            self.open(test_server.get_host_and_port())

            screen_document_tree = Screen_DocumentTree(self)

            screen_document_tree.assert_on_screen()
            screen_document_tree.assert_contains_document("Document 1")

            screen_document = screen_document_tree.do_click_on_first_document()

            screen_document.assert_on_screen_document()
            screen_document.assert_header_document_title("Document 1")

            screen_document.assert_text("Hello world!")

            # Requirement
            root_node = screen_document.get_root_node()
            root_node_menu = root_node.do_open_node_menu()
            form_edit_requirement: Form_EditRequirement = (
                root_node_menu.do_node_add_requirement_first()
            )

            form_edit_requirement.do_fill_in_field_title("Requirement title #1")
            form_edit_requirement.do_fill_in_field_statement(
                TEXT_WITH_TRAILING_WHITESPACES
            )
            form_edit_requirement.do_form_submit()

            # Check the resulting TOC.
            requirement = screen_document.get_requirement()
            requirement.assert_requirement_title("Requirement title #1", "1")
            screen_document.assert_toc_contains("Requirement title #1")

        assert test_setup.compare_sandbox_and_expected_output()
