# pylint: disable=invalid-name
from seleniumbase import BaseCase

from tests.end2end.helpers.form.form import Form


class Form_EditRequirement(Form):  # pylint: disable=invalid-name
    def __init__(self, test_case: BaseCase) -> None:
        assert isinstance(test_case, BaseCase)
        super().__init__(test_case)

    # comment actions

    def assert_form_has_no_comments(self) -> None:
        self.test_case.assert_element_not_present(
            "(//*[@data-testid='form-requirement[COMMENT]-field'])"
        )

    def do_form_add_field_comment(self) -> None:
        super().do_add_field("comment")

    def do_delete_comment(self, field_order: int = 1) -> None:
        super().do_delete_field("requirement[COMMENT]", field_order)

    def do_fill_in_field_comment(
        self, field_value: str, field_order: int = 1
    ) -> None:
        assert isinstance(field_value, str)
        super().do_fill_in("requirement[COMMENT]", field_value, field_order)

    # parent-link actions

    def assert_form_has_no_parents(self) -> None:
        self.test_case.assert_element_not_present(
            "(//*[@data-testid='form-requirement[REFS_PARENT][]-field'])"
        )

    def do_form_add_field_parent_link(self) -> None:
        super().do_add_field("parent-link")

    def do_delete_parent_link(self, field_order: int = 1) -> None:
        super().do_delete_field("requirement[REFS_PARENT][]", field_order)

    def do_fill_in_field_parent_link(
        self, field_value: str, field_order: int = 1
    ) -> None:
        assert isinstance(field_value, str)
        super().do_fill_in(
            "requirement[REFS_PARENT][]", field_value, field_order
        )

    # fill in the named fields

    def do_fill_in_field_uid(self, field_value: str) -> None:
        assert isinstance(field_value, str)
        super().do_fill_in("requirement[UID]", field_value)

    def do_fill_in_field_title(self, field_value: str) -> None:
        assert isinstance(field_value, str)
        super().do_fill_in("requirement[TITLE]", field_value)

    def do_fill_in_field_statement(self, field_value: str) -> None:
        assert isinstance(field_value, str)
        super().do_fill_in("requirement[STATEMENT]", field_value)

    def do_fill_in_field_rationale(self, field_value: str) -> None:
        assert isinstance(field_value, str)
        super().do_fill_in("requirement[RATIONALE]", field_value)
