from __future__ import annotations
from pathlib import Path
from typing_extensions import override  # @UnresolvedImport

from ciqar.report.pages.single_file_base import SingleFileGenerator
from ciqar.templates.api import ReportFile, RuleListRow


class RuleListGenerator(SingleFileGenerator):
    """
    Template Method implementation for generating the list of linter rules.
    It also summarizes some results for each rule (e.g. number of caused violations).
    """

    @override
    def _get_template_filename(self) -> str:
        return "rule_list.html.in"

    @override
    def _get_output_filepath(self, report_base_path: Path) -> Path:
        return report_base_path.joinpath("rule_list.html")

    @override
    def _create_template_data(self) -> ReportFile:
        rule_list_data = []
        for rule_name in self._linter_results.get_distinct_messages():
            violation_count = self._linter_results.get_message_count(rule_name)
            example_violation = self._linter_results.get_example_violation(rule_name)
            rule_list_data.append(RuleListRow(
                rule_name=rule_name,
                violation_count=violation_count,
                example_message=example_violation.message_text if example_violation else "",
            ))

        violations_page = ReportFile(
            report_title=self._report_name,
            path_to_report_root="",
            ciqar_tag=self._application_tag,
            rule_list_data=rule_list_data
        )
        return violations_page
