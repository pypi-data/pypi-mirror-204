"""
Contains the data types that are handed over to the Jinja2 templates.
This is the template API.
"""

from __future__ import annotations
import attrs


@attrs.define
class ReportFile:
    """
    Providess all data needed to render a single file of the report.

    Besides some basic data, a ReportFile instance can contain additional optional data depending on the
    template file being rendered (e.g. a template file for a "summary" page will have the optional
    `summary_data` property set to some useful data).
    """

    report_title: str = attrs.field()
    """ Title of the whole report (e.g. "MyPy check report"). """

    path_to_report_root: str = attrs.field()
    """ Relative path from the current file to the report root, "" if the file is in root. """

    ciqar_tag: str
    """ Ciqar name and version. """

    context_name: str = attrs.field(default="")
    """
    Display name of the context object which may be displayed e.g. as part of the page title.
    For example, the context can be the file to be shown or the linter rule to show files/violations of.
    In these cases, `context_name` would be the file name or the rule name respectively.
    May be empty if there is not special context.
    """

    summary_data: SummaryData | None = attrs.field(default=None)
    """ Report summary data, if requested. """

    rule_list_data: list[RuleListRow] | None = attrs.field(default=None)
    """ Rule list data, if requested. """

    file_list_data: list[FileListRow] | None = attrs.field(default=None)
    """ File list data, if requeted. """

    source_content_data: list[SourceLine] | None = attrs.field(default=None)
    """ Data for a source listing, if requested, """ 


@attrs.define
class SummaryData:
    """
    Provides all data needed for a short report summarization.
    """

    source_file_count: int
    """ Total number of found source files. """

    violation_count: int
    """ Total number of violations. """

    line_count: int
    """ Total number of source lines. """

    bad_line_count: int
    """ Total number of bad source lines. """

    generation_time: str
    """ Date and time of the report generation, formatted suitable for displaying. """

    analyzer_tag: str
    """ Displayable analyzer name tag, e.g. a linter's name + version. """

    global_linter_messages: list[str]
    """ Linter messages that are not assigned to a certain source code line (e.g. warning messages). """


@attrs.define
class RuleListRow:
    """
    Provides the data of a single row in a list of rules.
    "Rule" is the linter option/check/rule that causes a certain violation. Usually, rules can be enabled or
    disabled in the linter settings. The exact denomination varies between different linters, but Ciqar uses
    the term "rule".
    """

    rule_name: str
    """ Name/ID of the linter rule. """

    violation_count: int
    """ Number of violations caused by this rule. """

    example_message: str
    """
    Example message for supporting the user in understanding the rules.
    This is simply one of the found messages.
    """


@attrs.define
class FileListRow:
    """
    Provides the data of a single row in a list of source files.
    """

    display_filename: str
    """ File path and name as shown in the report. """

    report_filename: str
    """ File path to the destination file in the report (relative to the report root). """

    line_count: int
    """ Number of code lines in this file (empty lines do not count). """

    bad_line_count: int
    """ Number of lines that caused at elast one violation. """

    violation_count: int
    """ Number of violations caused by this file. """

    rating: int  # TODO: May there is a better rating than just numbers? I.e. "good", "bad", "?"?
    """ Rating of this file based on the report result: 0 = "good" to 2 = "bad". """


@attrs.define
class SourceLine:
    """
    Provides all data of a single line in a source code file.
    """

    lineno: int
    """ Line number. """

    content: str
    """ Line content. """

    rating: str
    """ Rating of this line based on the report result: 0 = "good" to 2 = "bad". """

    messages: list[str]
    """ List of all Violation messages caused by this line. """


@attrs.define
class Violation:

    SEVERITY_ERROR = "error"
    SEVERITY_WARNING = "warning"
    SEVERITY_INFO = "info"

    """
    Provides all data of a single violation.
    """

    rule: str
    """ Linter rule that enables/disables this violation. """

    severity: str
    """
    Severity of this violation.
    One of the SEVERITY* constants. Not all linters support different severities.
    TODO: Better use an enum here - But does this work with Jinja?
    """

    message_lines: list[str]
    """
    Message text of this violation, one line per list item.
    There is always at least one line. Storing multiline messages as list of strings allows the template to
    easily control the handling of line breaks (e.g. "\n" vs. "<br/>").
    """
