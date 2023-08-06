from __future__ import annotations
from abc import ABC, abstractmethod
import attrs
from pathlib import Path
from typing import Iterable, Optional


@attrs.define
class Violation:
    """
    Represents a single violation from the linter result. This is the data type provided
    by LinterResultParser implementation.
    """

    filename: Path = attrs.field()
    """
    Full path to the source file this violation was reported in.
    """

    linenumber: int = attrs.field()
    """
    Line number this violation was reported for.
    """

    message_type = attrs.field()  # TODO: Rename to "message_severity" and use an enum
    message_text = attrs.field()  # TODO: Refactor to a list of string (multiline messages)
    message_id = attrs.field()  # TODO: Rename to "rule" and use an enum


class LinterResultParser(ABC):
    """
    Base class for all result parser implementations.
    Represents a parser providing all reported violations one by one.
    """

    def __init__(self, result_file: Path, result_base_path: Optional[Path]=None):
        """
        :param result_file: Linter result file to read violation information from.
        :param result_base_path: The absolute path any relative paths in the linter result file are
                                 relative to.
        """
        self._result_file = result_file
        self._result_base_path = result_base_path if result_base_path else self._result_file.parent.resolve()
        self.global_messages: list[str] = []
        """
        List of linter messages that are not tied to a certain source location (e.g. general warnings or
        errors).
        """

    @property
    @abstractmethod
    def analyzer_name(self) -> str:
        """
        Name of the code analyzer that created the result result file processed by this parser.
        """

    @abstractmethod
    def parse(self) -> Iterable[Violation]:
        """
        Parses the result data into violation data and returns them one by one.
        """
