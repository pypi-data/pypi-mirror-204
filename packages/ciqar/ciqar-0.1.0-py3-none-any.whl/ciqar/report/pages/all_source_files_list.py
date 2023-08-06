from __future__ import annotations
from pathlib import Path
from typing_extensions import override  # @UnresolvedImport

from ciqar.report.pages.single_file_base import SingleFileGenerator
from ciqar.templates.api import ReportFile, FileListRow


class AllSourceFilesListGenerator(SingleFileGenerator):
    """
    Template Method implementation for generating the source file list.
    It also summarizes some results for each file (e.g. violation count).
    """

    @override
    def _get_template_filename(self) -> str:
        return "all_source_files_list.html.in"

    @override
    def _get_output_filepath(self, report_base_path: Path) -> Path:
        return report_base_path.joinpath("all_source_files_list.html")

    @override
    def _create_template_data(self) -> ReportFile:
        source_files_data = []
        for source_file in self._source_file_collector.get_all_source_files():
            line_count = self._linter_results.get_line_count(source_file.absolute_path)
            violation_count = self._linter_results.get_violation_count(source_file.absolute_path)
            rating = 2
            if violation_count == 0:
                rating = 0
            elif violation_count < 10:
                rating = 1
            source_files_data.append(FileListRow(
                display_filename=str(source_file.project_relative_path),
                report_filename=str(Path("sources").joinpath(
                    self._create_corresponding_report_output_file_path(source_file.project_relative_path)
                )),
                line_count=source_file.line_count,
                bad_line_count=line_count,
                violation_count=violation_count,
                rating=rating,
            ))

        files_page = ReportFile(
            report_title=self._report_name,
            path_to_report_root=self._get_relative_url_to_report_root(),
            ciqar_tag=self._application_tag,
            file_list_data=source_files_data
        ) 
        return files_page
