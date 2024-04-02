"""Results of checks using clang-tidy."""

import dataclasses


@dataclasses.dataclass
class CheckResult:
    """Class of the result of a check."""

    exit_code: int
    stdout: str
    stderr: str
