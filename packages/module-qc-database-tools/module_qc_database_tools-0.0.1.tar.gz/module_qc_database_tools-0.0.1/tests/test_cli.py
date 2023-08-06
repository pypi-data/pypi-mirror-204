from __future__ import annotations

import pytest
from typer.testing import CliRunner

from module_qc_database_tools.cli import app


@pytest.fixture()
def runner():
    return CliRunner(mix_stderr=False)


def test_generate_yarr_config_help(runner):
    result = runner.invoke(
        app,
        args=[
            "generate-yarr-config",
            "-h",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr


def test_register_component_help(runner):
    result = runner.invoke(
        app,
        args=[
            "register-component",
            "-h",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
