"""Class to execute clang-tidy."""

import abc
import dataclasses
import logging
import typing

from clang_tidy_checker.command_executor import CommandExecutor
from clang_tidy_checker.config import Config

LOGGER = logging.getLogger(__name__)


@dataclasses.dataclass
class CheckResult:
    """Class of the result of a check."""

    success: bool
    stdout: str
    stderr: str


class IClangTidyExecutor(abc.ABC):
    """Interface for clang-tidy executor."""

    @abc.abstractmethod
    async def __aenter__(self) -> typing.Self:
        pass

    @abc.abstractmethod
    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        pass

    @abc.abstractmethod
    async def execute(self, *, config: Config, input_file: str) -> CheckResult:
        """Execute clang-tidy.

        Args:
            config (Config): Configuration.
            input_file (str): Input file path.

        Returns:
            CheckResult: Result.
        """


class ClangTidyExecutor(IClangTidyExecutor):
    """Class to execute clang-tidy."""

    def __init__(self) -> None:
        self._command_executor = CommandExecutor()

    async def __aenter__(self) -> typing.Self:
        await self._command_executor.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self._command_executor.__aexit__(exc_type, exc_value, traceback)

    async def execute(self, *, config: Config, input_file: str) -> CheckResult:
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

        result = await self._command_executor.execute(
            command=command, cwd=config.build_dir
        )
        exit_code = result.exit_code
        stdout = result.stdout
        stderr = result.stderr

        if exit_code == 0:
            LOGGER.info(
                "Check of %s finished with exit code %s.", input_file, exit_code
            )
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

        return CheckResult(success=(exit_code == 0), stdout=stdout, stderr=stderr)
