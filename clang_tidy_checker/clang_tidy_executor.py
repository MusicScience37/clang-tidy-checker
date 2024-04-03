"""Class to execute clang-tidy."""

import abc
import logging
import os
import typing

from clang_tidy_checker.cache_table import create_cache_table_at
from clang_tidy_checker.check_result import CheckResult
from clang_tidy_checker.command_executor import CommandExecutor
from clang_tidy_checker.config import Config
from clang_tidy_checker.source_hash_calculator import SourceHashCalculator

try:
    from typing import Self
except ImportError:
    Self = typing.TypeVar("Self", bound="IClangTidyExecutor")  # type: ignore

LOGGER = logging.getLogger(__name__)


class IClangTidyExecutor(abc.ABC):
    """Interface for clang-tidy executor."""

    @abc.abstractmethod
    async def __aenter__(self) -> Self:
        pass

    @abc.abstractmethod
    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        pass

    @abc.abstractmethod
    async def execute(self, *, input_file: str) -> CheckResult:
        """Execute clang-tidy.

        Args:
            input_file (str): Input file path.

        Returns:
            CheckResult: Result.
        """


def write_result_log(input_file: str, exit_code: int, stdout: str, stderr: str) -> None:
    """Write log of the result.

    Args:
        input_file (str): Input file path.
        exit_code (int): Exit code.
        stdout (str): Standard output.
        stderr (str): Standard error.
    """

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


class ClangTidyExecutor(IClangTidyExecutor):
    """Class to execute clang-tidy."""

    def __init__(self, config: Config) -> None:
        self._config = config
        self._command_executor = CommandExecutor()

    async def __aenter__(self) -> Self:
        await self._command_executor.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self._command_executor.__aexit__(exc_type, exc_value, traceback)

    async def execute(self, *, input_file: str) -> CheckResult:
        command = (
            [
                self._config.clang_tidy_path,
                "--quiet",
                "--warnings-as-errors=*",
                "-p",
                self._config.build_dir,
            ]
            + self._config.extra_args
            + [
                input_file,
            ]
        )

        result = await self._command_executor.execute(
            command=command, cwd=self._config.build_dir
        )
        exit_code = result.exit_code
        stdout = result.stdout
        stderr = result.stderr

        write_result_log(
            exit_code=exit_code,
            input_file=input_file,
            stdout=stdout,
            stderr=stderr,
        )

        return CheckResult(exit_code=exit_code, stdout=stdout, stderr=stderr)


class CachedClangTidyExecutor(IClangTidyExecutor):
    """Class to execute clang-tidy but with caching of results."""

    def __init__(self, config: Config) -> None:
        self._clang_tidy_executor = ClangTidyExecutor(config=config)
        self._source_hash_calculator = SourceHashCalculator(config=config)
        if config.cache_dir is None:
            raise ValueError("Cache directory is required for CachedClangTidyExecutor.")
        self._cache_dir = config.cache_dir
        os.makedirs(config.cache_dir, exist_ok=True)
        self._cache_table = create_cache_table_at(
            f"{config.cache_dir}/clang_tidy_cache_v2.db",
            max_cache_entries=config.max_cache_entries,
        )

    async def __aenter__(self) -> Self:
        await self._clang_tidy_executor.__aenter__()
        await self._source_hash_calculator.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self._clang_tidy_executor.__aexit__(exc_type, exc_value, traceback)
        await self._source_hash_calculator.__aexit__(exc_type, exc_value, traceback)

    async def execute(self, *, input_file: str) -> CheckResult:
        source_hash = await self._source_hash_calculator.calculate(
            input_file=input_file
        )

        result = self._cache_table.load(source_hash=source_hash)
        if result is None:
            result = await self._clang_tidy_executor.execute(input_file=input_file)
            self._cache_table.save(source_hash=source_hash, result=result)

        write_result_log(
            exit_code=result.exit_code,
            input_file=input_file,
            stdout=result.stdout,
            stderr=result.stderr,
        )

        return result
