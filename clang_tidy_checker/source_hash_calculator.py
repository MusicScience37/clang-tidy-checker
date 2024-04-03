"""Class to calculate hash of source codes."""

import asyncio
import base64
import hashlib
import json
import logging
import os
import shlex
import typing

from clang_tidy_checker.command_executor import CommandExecutor
from clang_tidy_checker.config import Config

try:
    from typing import Self
except ImportError:
    Self = typing.TypeVar("Self", bound="SourceHashCalculator")  # type: ignore

LOGGER = logging.getLogger(__name__)


class SourceHashCalculator:
    """Class to calculate hash of source codes.

    Args:
        config: Configuration.
    """

    def __init__(self, config: Config) -> None:
        self._command_executor = CommandExecutor()
        self._config = config

        with open(
            os.path.join(self._config.build_dir, "compile_commands.json"),
            encoding="utf8",
        ) as file:
            self._compile_commands = json.load(file)

    async def __aenter__(self) -> Self:
        await self._command_executor.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self._command_executor.__aexit__(exc_type, exc_value, traceback)

    async def calculate(self, input_file: str) -> str:
        """Calculate a hash of a source code.

        Args:
            input_file (str): Input file path.

        Returns:
            str: Hash.
        """
        absolute_input_file = os.path.abspath(input_file)
        for compile_command in self._compile_commands:
            if compile_command["file"] == absolute_input_file:
                break
        else:
            raise ValueError(
                f"{absolute_input_file} is not found in compile_commands.json"
            )
        args = shlex.split(compile_command["command"])

        # Remove output file option to get the result from stdout.
        for index, arg in enumerate(args):
            if arg == "-o":
                del args[index : index + 2]
                break

        args.append("-E")

        preprocess_result = await self._command_executor.execute(
            args, cwd=compile_command["directory"]
        )

        if preprocess_result.exit_code != 0:
            LOGGER.error("Failed to preprocess %s.", input_file)
            LOGGER.error(preprocess_result.stderr)
            raise RuntimeError(f"Failed to preprocess {input_file}.")

        return await asyncio.to_thread(
            self._calculate_hash_of_string, preprocess_result.stdout
        )

    @staticmethod
    def _calculate_hash_of_string(string: str) -> str:
        """Calculate a hash of a string.

        Args:
            string (str): Input.

        Returns:
            str: Hash.
        """
        return base64.b64encode(hashlib.sha3_512(string.encode()).digest()).decode(
            "ascii"
        )
