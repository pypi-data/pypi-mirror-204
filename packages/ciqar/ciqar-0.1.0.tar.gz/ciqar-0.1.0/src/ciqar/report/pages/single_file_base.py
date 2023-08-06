from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path

from ciqar.input.sourcefiles import SourceFileCollector
from ciqar.input.violations import LinterResults
from ciqar.report.jinja_wrapper import JinjaWrapper
from ciqar.templates.api import ReportFile


class SingleFileGenerator(ABC):
    """
    "Template method" (design pattern) base class for generating a concrete report file.
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
        self._jinja_wrapper = jinja_wrapper
        self._linter_results = linter_results
        self._source_file_collector = source_file_collector
        self._report_name = report_name
        self._report_base_path = report_base_path  # Path to the report output directory
        self._application_tag = application_tag

    def generate(self) -> None:
        """
        Generate the file repesented by this instance.
        This is the template method which implements the basic algorithm.
        """
        template_data = self._create_template_data()
        template_file = self._get_template_filename()
        rendered_file_content = self._jinja_wrapper.render_template(template_file, data=template_data)

        output_filepath = self._get_output_filepath(self._report_base_path)
        self.__write_rendered_file(output_filepath, rendered_file_content)

    def __write_rendered_file(self, output_file_name: Path, content: str) -> None:
        output_file = self._report_base_path.joinpath(output_file_name)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(data=content, encoding="utf8")

    def _get_relative_url_to_report_root(self) -> str:
        """
        Returns the relative path from this report's output file to the report root.
        Derived classes may provide this path to the template which may need it for generating links to
        other report files.

        :return: Plain, relative URL path from the current output file to the report root (e.g. "../../").
        """
        relative_filepath = (
            self._get_output_filepath(self._report_base_path)
            .relative_to(self._report_base_path)
        )
        path_to_report_root = "../" * len(relative_filepath.parent.parts)
        return path_to_report_root

    @abstractmethod
    def _get_template_filename(self) -> str:
        """
        """

    @abstractmethod
    def _create_template_data(self) -> ReportFile:
        """
        """

    @abstractmethod
    def _get_output_filepath(self, report_base_path: Path) -> Path:
        """
        Returned path must be within the provided report_base_path!
        """

    def _create_corresponding_report_output_file_path(self, project_relative_file_path: Path) -> Path:
        """
        Return the relative report file name that corresponds to the given (project relative) source file
        path.
        The original source tree is duplicated in the report (starting with the project base dir), just
        replacing the file suffix with ".html".

        :param project_relative_file_path: Original file path, relative to the project root.
        :return: Corresponding destination file path in the report output (relative to the report root).
        """
        return project_relative_file_path.with_suffix(".html")

    def _create_absolute_report_output_file_path(self, project_relative_file_path: Path) -> Path:
        """
        Return the absolute report file name that corresponds to the given (project relative) source file
        path.
        The original source tree is duplicated in the report (starting with the project base dir), just
        replacing the file suffix with ".html".

        :param project_relative_file_path: Original file path, relative to the project root.
        :return: Corresponding absolute destination file path in the report output.
        """
        return self._report_base_path.joinpath(
            self._create_corresponding_report_output_file_path(project_relative_file_path)
        )
