"""Execute clang-tidy."""

import dataclasses
import logging

import trio

from clang_tidy_checker.config import Config

LOGGER = logging.getLogger(__name__)


@dataclasses.dataclass
class ExecutionResult:
    """Class of the result of an execution."""

    input_file: str
    exit_code: int
    stdout: str
    stderr: str


# TODO: better handling.
CONSOLE_ENCODING = "utf8"


async def execute_clang_tidy(*, config: Config, input_file: str) -> ExecutionResult:
    """Execute clang-tidy.

    Args:
        config (Config): Configuration.
        input_file (str): Input file path.

    Returns:
        ExecutionResult: Result of execution.
    """

    result = await trio.run_process(
        [
            config.clang_tidy_path,
            "--quiet",
            "--warnings-as-errors=*",
            "-p",
            config.build_dir,
            input_file,
        ],
        capture_stdout=True,
        capture_stderr=True,
        check=False,
    )
    stdout = result.stdout.decode(encoding=CONSOLE_ENCODING)
    stderr = result.stderr.decode(encoding=CONSOLE_ENCODING)

    if result.returncode == 0:
        LOGGER.info(
            "Check of %s finished with exit code %s.", input_file, result.returncode
        )
        if result.stdout != "":
            LOGGER.debug("%s", stdout)
        if result.stderr != "":
            LOGGER.debug("%s", stderr)
    else:
        LOGGER.warning(
            "Check of %s finished with exit code %s.\n%s\n%s",
            input_file,
            result.returncode,
            stdout,
            stderr,
        )

    return ExecutionResult(
        input_file=input_file,
        exit_code=result.returncode,
        stdout=stdout,
        stderr=stderr,
    )
