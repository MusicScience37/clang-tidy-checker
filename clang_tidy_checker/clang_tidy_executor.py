"""Class to execute clang-tidy."""

import abc
import dataclasses
import logging
import os
import typing

import msgpack

from clang_tidy_checker.command_executor import CommandExecutor
from clang_tidy_checker.config import Config
from clang_tidy_checker.source_hash_calculator import SourceHashCalculator

try:
    from typing import Self
except ImportError:
    Self = typing.TypeVar("Self", bound="IClangTidyExecutor")  # type: ignore

LOGGER = logging.getLogger(__name__)


@dataclasses.dataclass
class CheckResult:
    """Class of the result of a check."""

    exit_code: int
    stdout: str
    stderr: str


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


def get_cache_file_path(cache_dir: str, source_hash: str) -> str:
    """Get the file path of cache file.

    Args:
        cache_dir (str): Path to the cache directory.
        source_hash (str): Hash of the source code.

    Returns:
        str: Path to the cache file.
    """
    return os.path.join(
        cache_dir, source_hash[-1], source_hash[-2], source_hash[-20:-2]
    )


class CachedClangTidyExecutor(IClangTidyExecutor):
    """Class to execute clang-tidy but with caching of results."""

    def __init__(self, config: Config) -> None:
        self._clang_tidy_executor = ClangTidyExecutor(config=config)
        self._source_hash_calculator = SourceHashCalculator(config=config)
        if config.cache_dir is None:
            raise ValueError("Cache directory is required for CachedClangTidyExecutor.")
        self._cache_dir = config.cache_dir

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
        cache_file_path = get_cache_file_path(
            cache_dir=self._cache_dir, source_hash=source_hash
        )
        if os.path.exists(cache_file_path):
            with open(cache_file_path, "rb") as file:
                result_dict = msgpack.unpack(file)
            exit_code = int(result_dict["error_code"])
            stdout = str(result_dict["stdout"])
            stderr = str(result_dict["stderr"])

            write_result_log(
                exit_code=exit_code,
                input_file=input_file,
                stdout=stdout,
                stderr=stderr,
            )

            return CheckResult(exit_code=exit_code, stdout=stdout, stderr=stderr)

        result = await self._clang_tidy_executor.execute(input_file=input_file)
        os.makedirs(os.path.dirname(cache_file_path), exist_ok=True)
        with open(cache_file_path, "wb") as file:
            msgpack.pack(
                {
                    "error_code": result.exit_code,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                },
                file,
            )
        return result
