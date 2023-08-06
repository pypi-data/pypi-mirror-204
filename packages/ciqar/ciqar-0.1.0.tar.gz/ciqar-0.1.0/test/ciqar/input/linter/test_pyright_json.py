"""
Unit tests for the pyright_json module.
"""

from __future__ import annotations
from pathlib import Path
from pyfakefs.fake_filesystem import FakeFilesystem
import pytest

from ciqar.input.linter.pyright_json import PyrightJsonParser
from ciqar.input.linter.result_parser import Violation


class TestPyrightJsonParser:
    """
    Unit tests for the PyrightJsonParser class.
    """

    @pytest.mark.parametrize("jsonfile_content, expected_violations", [
        (  # Minimal valid JSON file
            "{}", []
        ),

        (  # Result file without violations
            """
{
    "version": "1.1.301",
    "generalDiagnostics": [],
    "summary": {}
}
            """,
            []
        ),

        (  # Normal violations
           """
{
    "version": "1.1.301",
    "generalDiagnostics": [
        {
            "file": "/path/to/file1.py",
            "severity": "error",
            "message": "No parameter named \\"message_type\\"",
            "range": {
                "start": {
                    "line": 68,
                    "character": 12
                },
                "end": {
                    "line": 68,
                    "character": 24
                }
            },
            "rule": "reportGeneralTypeIssues"
        },
        {
            "file": "/path/to/file2.py",
            "severity": "error",
            "message": "Dataclass field without type annotation will cause runtime exception",
            "range": {
                "start": {
                    "line": 26,
                    "character": 17
                },
                "end": {
                    "line": 26,
                    "character": 30
                }
            },
            "rule": "reportGeneralTypeIssues"
        }
    ]
}
            """,
            [
                Violation(filename=Path("/path/to/file1.py"), linenumber=68,
                    message_type="error", message_id="reportGeneralTypeIssues",
                    message_text="No parameter named \"message_type\"",
                ),
                Violation(filename=Path("/path/to/file2.py"), linenumber=26,
                    message_type="error", message_id="reportGeneralTypeIssues",
                    message_text="Dataclass field without type annotation will cause runtime exception",
                ),
            ]
        ),

        (  # Violation without the 'rule' field
            """
{
    "version": "1.1.301",
    "generalDiagnostics": [
        {
            "file": "/path/to/file.py",
            "severity": "error",
            "message": "No parameter named \\"message_id\\"",
            "range": {
                "start": {
                    "line": 7,
                    "character": 5
                },
                "end": {
                    "line": 7,
                    "character": 17
                }
            }
        }
    ]
}
            """,
            [
                Violation(filename=Path("/path/to/file.py"), linenumber=7,
                    message_type="error", message_id="unknownRule",
                    message_text="No parameter named \"message_id\"",
                )
            ]
        ),
    ])
    def test_parse(self, jsonfile_content:str, expected_violations: list[Violation], fs: FakeFilesystem) -> None:
        PYRIGHT_JSON_FILE = Path("/tmp/pyright.json")

        fs.create_file(PYRIGHT_JSON_FILE, contents=jsonfile_content.strip())
        parser = PyrightJsonParser(result_file=PYRIGHT_JSON_FILE, result_base_path=Path("/out"))

        violations = list(parser.parse())
        assert len(expected_violations) == len(violations)
        for expected, parsed in zip(expected_violations, violations):
            assert str(expected.filename) == str(parsed.filename)
            assert expected.linenumber == parsed.linenumber
            assert expected.message_type ==parsed.message_type
            assert expected.message_text == parsed.message_text
            assert expected.message_id == parsed.message_id

    def test_analyzer_name(self):
        parser = PyrightJsonParser(result_file=Path("/tmp/result.json"))
        assert parser.analyzer_name == "Pyright"
