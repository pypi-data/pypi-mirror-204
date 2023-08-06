from __future__ import annotations
from pathlib import Path
import shutil

from ciqar.input.sourcefiles import SourceFileCollector
from ciqar.input.violations import LinterResults
from ciqar.report.jinja_wrapper import JinjaWrapper
from ciqar.report.pages.all_source_files_list import AllSourceFilesListGenerator
from ciqar.report.pages.source_file import SourceFileGenerator
from ciqar.report.pages.files_per_rule_list import FilesPerRuleListGenerator
from ciqar.report.pages.rule_list import RuleListGenerator
from ciqar.report.pages.summary import ReportSummeryGenerator


class ReportGenerator:
    """
    This creates the following pages/view (from templates):
     - Source listing for each source code file
     - List of all violation types
     - List of all source files
     - List of all source files with a certain violation type
     - Report summary
    """

    def __init__(
            self,
            source_collector: SourceFileCollector,
            violations_parser,
            template_name: str,
            output_path: Path,
            application_tag: str
    ):
        self.__source_collector = source_collector
        self.__linter_results = LinterResults(violations_parser, source_collector.get_excluded_source_files())
        self.__jinja_wrapper = JinjaWrapper(template_name)
        self.__output_path = output_path
        self.__report_name = "{} Code Quality Report".format(self.__linter_results.analyzer_name)
        self._application_tag = application_tag

    def generate_report(self):
        self.__prepare_output_dir()

        self.__generate_summary_page()
        self.__generate_all_source_file_pages()
        self.__generate_all_source_files_list_page()
        self.__generate_rule_list_page()
        self.__generate_all_files_per_rule_list_pages()

    def __prepare_output_dir(self):
        # TODO: Check (and warn?) if directory already exists (and is not empty)
        self.__output_path.mkdir(parents=True, exist_ok=True)
        static_file = self.__jinja_wrapper.get_static_file("style.css")
        self.__copy_static_file(static_file)

    def __generate_all_source_file_pages(self) -> None:
        for source_file in self.__source_collector.get_all_source_files():
            generator = SourceFileGenerator(
                jinja_wrapper=self.__jinja_wrapper,
                source_file_collector=self.__source_collector,
                linter_results=self.__linter_results,
                report_name=self.__report_name,
                report_base_path=self.__output_path,
                source_file=source_file,
                application_tag=self._application_tag,
            )
            generator.generate()

    def __generate_all_source_files_list_page(self):
        generator = AllSourceFilesListGenerator(
            jinja_wrapper=self.__jinja_wrapper,
            source_file_collector=self.__source_collector,
            linter_results=self.__linter_results,
            report_name=self.__report_name,
            report_base_path=self.__output_path,
            application_tag=self._application_tag,
        )
        generator.generate()

    def __generate_rule_list_page(self):
        generator = RuleListGenerator(
            jinja_wrapper=self.__jinja_wrapper,
            source_file_collector=self.__source_collector,
            linter_results=self.__linter_results,
            report_name=self.__report_name,
            report_base_path=self.__output_path,
            application_tag=self._application_tag,
        )
        generator.generate()

    def __generate_all_files_per_rule_list_pages(self) -> None:
        for rule_name in self.__linter_results.get_distinct_messages():
            generator = FilesPerRuleListGenerator(
                jinja_wrapper=self.__jinja_wrapper,
                source_file_collector=self.__source_collector,
                linter_results=self.__linter_results,
                report_name=self.__report_name,
                report_base_path=self.__output_path,
                rule_name=rule_name,
                application_tag=self._application_tag,
            )
            generator.generate()

    def __generate_summary_page(self):
        generator = ReportSummeryGenerator(
            jinja_wrapper=self.__jinja_wrapper,
            source_file_collector=self.__source_collector,
            linter_results=self.__linter_results,
            report_name=self.__report_name,
            report_base_path=self.__output_path,
            application_tag=self._application_tag,
        )
        generator.generate()

    def __copy_static_file(self, static_file_path):
        shutil.copy(static_file_path, self.__output_path.joinpath(static_file_path.name))
