from __future__ import annotations
from datetime import datetime
from pathlib import Path
import time
from typing_extensions import override  # @UnresolvedImport

from ciqar.input.sourcefiles import SourceFileCollector
from ciqar.input.violations import LinterResults
from ciqar.report.jinja_wrapper import JinjaWrapper
from ciqar.report.pages.single_file_base import SingleFileGenerator
from ciqar.templates.api import ReportFile, SummaryData


class ReportSummeryGenerator(SingleFileGenerator):
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

    @override
    def _get_template_filename(self) -> str:
        return "summary.html.in"

    @override
    def _get_output_filepath(self, report_base_path: Path) -> Path:
        return report_base_path.joinpath("index.html")

    @override
    def _create_template_data(self) -> ReportFile:
        timestring = "{0} ({1})".format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            time.tzname[time.daylight]
        )

        all_source_files = self._source_file_collector.get_all_source_files()
        summary_data = SummaryData(
            source_file_count=len(all_source_files),
            violation_count=self._linter_results.get_total_violation_count(),
            line_count=sum(sf.line_count for sf in all_source_files),
            bad_line_count=self._linter_results.get_total_line_count(),
            generation_time=timestring,
            analyzer_tag=self._linter_results.analyzer_name,
            global_linter_messages=self._linter_results.global_messages,
        )
        summary_page = ReportFile(
            report_title=self._report_name,
            path_to_report_root=self._get_relative_url_to_report_root(),
            ciqar_tag=self._application_tag,
            summary_data=summary_data
        )

        return summary_page
