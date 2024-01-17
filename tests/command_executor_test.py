"""Test of CommandExecutor."""

import asyncio

import pytest

from clang_tidy_checker.command_executor import CommandExecutor


@pytest.mark.asyncio
async def test_execute_command():
    """Test to execute commands."""
    executor = CommandExecutor()
    async with executor:
        result = await executor.execute(["echo", "test"])
        assert result.exit_code == 0
        assert result.stdout == "test\n"
        assert result.stderr == ""


@pytest.mark.asyncio
async def test_kill_all_commands():
    """Test to kill all commands."""
    executor = CommandExecutor()
    async with executor:
        task = asyncio.create_task(executor.execute(["sleep", "1"]))
        await asyncio.sleep(0.01)

    result = await task
    assert result.exit_code < 0
