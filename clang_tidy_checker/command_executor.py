"""Class to execute commands."""

import asyncio
import asyncio.subprocess
import dataclasses
import logging
import typing

try:
    from typing import Self
except ImportError:
    Self = typing.TypeVar("Self", bound="CommandExecutor")  # type: ignore

LOGGER = logging.getLogger(__name__)


@dataclasses.dataclass
class CommandResult:
    """Class of the result of a command."""

    exit_code: int
    stdout: str
    stderr: str


# TODO: better handling.
CONSOLE_ENCODING = "utf8"


class CommandExecutor:
    """Class to execute commands."""

    def __init__(self) -> None:
        # pylint: disable=E1101
        # pylint has a bag (https://github.com/pylint-dev/pylint/issues/1469)
        self._processes: typing.List[asyncio.subprocess.Process] = []

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        self.kill_all()

    async def execute(
        self,
        command: typing.List[str],
        *,
        cwd: typing.Optional[str] = None,
    ) -> CommandResult:
        """Execute a command.

        Args:
            command (typing.List[str]): Command.
            cwd (typing.Optional[str]): Working directory. Defaults to None.

        Returns:
            CommandResult: Result.
        """
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd,
        )

        self._processes.append(process)
        stdout_binary, stderr_binary = await process.communicate()
        self._processes.remove(process)

        exit_code = typing.cast(int, process.returncode)
        stdout = stdout_binary.decode(CONSOLE_ENCODING)
        stderr = stderr_binary.decode(CONSOLE_ENCODING)

        return CommandResult(exit_code=exit_code, stdout=stdout, stderr=stderr)

    def kill_all(self) -> None:
        """Kill all remaining processes."""
        for process in self._processes:
            process.kill()
