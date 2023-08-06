from __future__ import annotations
from pathlib import Path
from typing_extensions import override  # @UnresolvedImport

from ciqar.input.sourcefiles import SourceFileCollector, SourceFile
from ciqar.input.violations import LinterResults
from ciqar.report.jinja_wrapper import JinjaWrapper
from ciqar.report.pages.single_file_base import SingleFileGenerator
from ciqar.templates.api import ReportFile, SourceLine


class SourceFileGenerator(SingleFileGenerator):
    """
    Template Method implementation for generating the detailed report for a single source file.
    """

    def __init__(
            self,
            jinja_wrapper: JinjaWrapper,
            source_file_collector: SourceFileCollector,
            linter_results: LinterResults,
            report_name: str,
            report_base_path: Path,
            source_file: SourceFile,
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
        self.__source_file = source_file

    @override
    def _get_template_filename(self) -> str:
        return "source_file.html.in"

    @override
    def _get_output_filepath(self, report_base_path: Path) -> Path:
        report_relative_path = Path("sources").joinpath(self.__source_file.project_relative_path)
        return self._create_absolute_report_output_file_path(report_relative_path)

    @override
    def _create_template_data(self) -> ReportFile:
        source_lines = []
        for idx, code in enumerate(self.__source_file.content):
            lineno = idx + 1
            violations = self._linter_results.get_violations(self.__source_file.absolute_path, lineno)

            source_lines.append(SourceLine(
                lineno=lineno,
                content=code.rstrip("\n").rstrip("\r"),
                rating="good" if not violations else "bad",
                messages = [
                    "{}: {}".format(violation.message_type, violation.message_text)
                    for violation in violations
                ]
            ))

        source_page = ReportFile(
            report_title=self._report_name,
            path_to_report_root=self._get_relative_url_to_report_root(),
            ciqar_tag=self._application_tag,
            context_name=str(self.__source_file.project_relative_path),
            source_content_data=source_lines
        )
        return source_page
