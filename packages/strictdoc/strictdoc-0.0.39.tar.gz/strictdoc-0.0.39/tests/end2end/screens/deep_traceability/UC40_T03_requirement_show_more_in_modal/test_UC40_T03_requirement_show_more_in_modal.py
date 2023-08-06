from seleniumbase import BaseCase

from tests.end2end.end2end_test_setup import End2EndTestSetup
from tests.end2end.helpers.components.viewtype_selector import (
    ViewType_Selector,
)
from tests.end2end.helpers.screens.document_tree.screen_document_tree import (
    Screen_DocumentTree,
)
from tests.end2end.server import SDocTestServer


class Test_UC40_T03_requirement_show_more_in_modal(BaseCase):
    def test_01(self):
        test_setup = End2EndTestSetup(path_to_test_file=__file__)

        with SDocTestServer(
            input_path=test_setup.path_to_sandbox
        ) as test_server:
            self.open(test_server.get_host_and_port())

            screen_document_tree = Screen_DocumentTree(self)

            screen_document_tree.assert_on_screen()
            screen_document_tree.assert_contains_document("Document title")

            screen_document = screen_document_tree.do_click_on_first_document()

            screen_document.assert_on_screen_document()
            screen_document.assert_header_document_title("Document title")
            screen_document.assert_text("Hello world!")

            viewtype_selector = ViewType_Selector(self)
            screen_deep_traceability = (
                viewtype_selector.do_go_to_deep_traceability()
            )
            screen_deep_traceability.assert_on_screen_deep_traceability()

            section = screen_deep_traceability.get_section()

            section.assert_section_title("Section title")
            section.assert_node_does_not_contain("Section text")

            requirement = screen_deep_traceability.get_requirement()

            requirement.assert_requirement_title("Requirement title")
            requirement.assert_requirement_uid("REC_UID")
            requirement.assert_requirement_statement_contains(
                "Requirement statement."
            )
            requirement.assert_node_does_not_contain("Requirement rationale.")

            modal = requirement.do_open_modal_requirement()
            modal.assert_modal()

            # requirement in modal turns out to be the last one on the page
            last = 2

            modal_requirement = screen_deep_traceability.get_requirement_modal(
                last
            )
            modal_requirement.assert_requirement_title("Requirement title")
            modal_requirement.assert_requirement_uid_contains("REC_UID")
            modal_requirement.assert_requirement_statement_contains(
                "Requirement statement."
            )
            modal_requirement.assert_requirement_rationale_contains(
                "Requirement rationale."
            )

            modal.do_close_modal()

        assert test_setup.compare_sandbox_and_expected_output()
