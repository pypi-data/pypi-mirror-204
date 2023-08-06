"""
Definition of the PyrightJsonParser class.
"""

from __future__ import annotations
import json
from pathlib import Path
from typing_extensions import override

from ciqar.input.linter.result_parser import LinterResultParser, Violation


class PyrightJsonParser(LinterResultParser):
    """
    Parser implementation for extracting violations from a Pyright JSON result file.
    """

    @property
    @override
    def analyzer_name(self) -> str:
        return "Pyright"

    @override
    def parse(self):
        json_data = json.load(self._result_file.open("rt"))
        for violation_data in json_data.get("generalDiagnostics", []):
            violation = Violation(
                filename=Path(violation_data["file"]),
                linenumber=violation_data["range"]["start"]["line"],
                message_type=violation_data["severity"],
                message_text=violation_data["message"],
                message_id=violation_data.get("rule", "unknownRule"),
            )
            yield violation
