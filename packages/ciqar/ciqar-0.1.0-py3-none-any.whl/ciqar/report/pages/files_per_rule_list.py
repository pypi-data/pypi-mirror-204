from __future__ import annotations
from pathlib import Path
from typing_extensions import override  # @UnresolvedImport

from ciqar.report.pages.single_file_base import SingleFileGenerator
from ciqar.templates.api import ReportFile, FileListRow
from ciqar.input.violations import LinterResults
from ciqar.input.sourcefiles import SourceFileCollector
from ciqar.report.jinja_wrapper import JinjaWrapper


class FilesPerRuleListGenerator(SingleFileGenerator):
    """
    Template Method implementation for generating the list of all files causing violation of a certain rule.
    It also summarizes some results for each files (e.g. number of occurences).
    """

    def __init__(
            self,
            jinja_wrapper: JinjaWrapper,
            source_file_collector: SourceFileCollector,
            linter_results: LinterResults,
            report_name: str,
            report_base_path: Path,
            rule_name: str,
            application_tag: str,
    ):
        super().__init__(
            jinja_wrapper,
            source_file_collector,
            linter_results,
            report_name,
            report_base_path,
            application_tag
        )
        self.__rule_name = rule_name

    @override
    def _get_template_filename(self) -> str:
        return "files_per_rule_list.html.in"

    @override
    def _get_output_filepath(self, report_base_path: Path) -> Path:
        return report_base_path.joinpath("rules", "{}.html".format(self.__rule_name))

    @override
    def _create_template_data(self) -> ReportFile:
        file_list_data = []
        for filepath in self._linter_results.get_violation_files(self.__rule_name):
            source_file = self._source_file_collector.get_source_file(filepath)
            violation_count = self._linter_results.get_filtered_violation_count(filepath, self.__rule_name)
            line_count = self._linter_results.get_line_count(source_file.absolute_path)
            rating = 2
            if violation_count == 0:
                rating = 0
            elif violation_count < 10:
                rating = 1

            file_list_data.append(FileListRow(
                display_filename=str(source_file.project_relative_path),
                report_filename=str(Path("sources").joinpath(
                    self._create_corresponding_report_output_file_path(source_file.project_relative_path)
                )),
                line_count=source_file.line_count,
                bad_line_count=line_count,
                violation_count=violation_count,
                rating=rating,
            ))

        violations_page = ReportFile(
            report_title=self._report_name,
            path_to_report_root="../",
            ciqar_tag=self._application_tag,
            context_name=self.__rule_name,
            file_list_data=file_list_data,
        )

        return violations_page
