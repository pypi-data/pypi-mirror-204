from __future__ import annotations
from pathlib import Path
from typing import Iterable, Optional, Sequence

from ciqar.input.linter.result_parser import LinterResultParser, Violation


class LinterResults:
    """
    Represents the set of all violations reported by the selected parser.
    An instance of this class provides information about the reported violation. It allows different
    kind of queries for the different view.
    Violation information is loaded from the provided parser.
    """

    def __init__(self, result_parser: LinterResultParser, excluded_source_files: Sequence[Path]):
        self.analyzer_name = result_parser.analyzer_name
        self.__result_parser: Optional[LinterResultParser] = result_parser
        """
        The parser to load result data from. Set to None after loading all results to show the "results
        available" state (because the data dicts may stay empty if there are no violations at all).
        """
        self.__excluded_source_files = excluded_source_files
        self.global_messages: list[str] = []
        self.__message_index: dict[Path, dict[int, list[Violation]]] = {}
        self.__message_to_files_index: dict[str, dict[Path, list[int]]] = {}

    def get_filenames(self) -> Iterable[Path]:
        self.__load_linter_result_data()
        return self.__message_index.keys()

    def get_line_count(self, filename) -> int:
        self.__load_linter_result_data()
        return len(self.__message_index.get(filename, {}))

    def get_total_line_count(self) -> int:
        self.__load_linter_result_data()
        return sum(len(i) for i in self.__message_index.values())

    def get_total_violation_count(self) -> int:
        self.__load_linter_result_data()
        total_violation_count = 0
        for lineno_violation_dict in self.__message_index.values():
            total_violation_count += sum(len(violation_list) for violation_list in lineno_violation_dict.values())
        return total_violation_count

    def get_violation_count(self, filename: Path) -> int:
        self.__load_linter_result_data()
        return sum(len(violations) for violations in self.__message_index.get(filename, {}).values())

    def get_filtered_violation_count(self, filename: Path, violation_type: str) -> int:
        self.__load_linter_result_data()
        violation_count = sum(
            len([violation for violation in violation_list if violation.message_id == violation_type])
            for violation_list in self.__message_index.get(filename, {}).values()
        )
        return violation_count

    def get_violations(self, filename: Path, lineno: int) -> Iterable[Violation]:
        self.__load_linter_result_data()
        return self.__message_index.get(filename, {}).get(lineno, [])

    def __load_linter_result_data(self) -> None:
        if self.__result_parser is None:
            return

        for source_line_info in self.__result_parser.parse():
            if source_line_info.filename in self.__excluded_source_files:
                # Also ignore all violations from this file.
                # TODO: Maybe it would be of interest to see which excluded files had been analyzed?
                continue

            self.__message_index.setdefault(source_line_info.filename, {}).setdefault(source_line_info.linenumber, []).append(source_line_info)
            if source_line_info.message_id:
                self.__message_to_files_index.setdefault(source_line_info.message_id, {}).setdefault(source_line_info.filename, []).append(source_line_info.linenumber)

        self.global_messages = self.__result_parser.global_messages
        self.__result_parser = None

    def get_distinct_messages(self) -> Iterable[str]:
        """
        Returns all reported linter message IDs, each ID is returned only once.
        """
        self.__load_linter_result_data()
        return self.__message_to_files_index.keys()

    def get_message_count(self, message_id: str) -> int:
        self.__load_linter_result_data()
        affected_files = self.__message_to_files_index.get(message_id, {})
        return sum([len(affected_lines) for affected_lines in affected_files.values()])

    def get_example_violation(self, violation_type: str) -> Optional[Violation]:
        """
        Returns the message of the first violation with the given type.
        If no violation of this type occurred, None is returned.
        """
        self.__load_linter_result_data()
        files_and_lines = self.__message_to_files_index.get(violation_type, {})
        example_filename, linenumbers = next(iter(files_and_lines.items()), (None, []))
        if not (example_filename and linenumbers):
            return None
        return next(iter(self.get_violations(filename=example_filename, lineno=linenumbers[0])), None)

    def get_violation_files(self, violation_type: str) -> Iterable[Path]:
        """
        Returns all files that caused a violation of the given type.
        Result is empty if there are no such files.
        """
        self.__load_linter_result_data()
        return self.__message_to_files_index.get(violation_type, {}).keys()
