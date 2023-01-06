"""Execute clang-tidy."""

import asyncio
import dataclasses
import logging

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

    command = (
        [
            config.clang_tidy_path,
            "--quiet",
            "--warnings-as-errors=*",
            "-p",
            config.build_dir,
        ]
        + config.extra_args
        + [
            input_file,
        ]
    )

    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout_binary, stderr_binary = await process.communicate()
    except Exception:
        process.kill()
        await process.communicate()
        raise

    stdout = stdout_binary.decode(encoding=CONSOLE_ENCODING)
    stderr = stderr_binary.decode(encoding=CONSOLE_ENCODING)
    exit_code = process.returncode
    assert exit_code is not None

    if exit_code == 0:
        LOGGER.info("Check of %s finished with exit code %s.", input_file, exit_code)
        if stdout != "":
            LOGGER.debug("%s", stdout)
        if stderr != "":
            LOGGER.debug("%s", stderr)
    else:
        LOGGER.warning(
            "Check of %s finished with exit code %s.\n%s\n%s",
            input_file,
            exit_code,
            stdout,
            stderr,
        )

    return ExecutionResult(
        input_file=input_file,
        exit_code=exit_code,
        stdout=stdout,
        stderr=stderr,
    )
