import pytest
from click.testing import CliRunner
from src.commands.metrics import machine_metrics


@pytest.fixture
def runner():
    return CliRunner()


def test_machine_metrics(runner):
    result = runner.invoke(machine_metrics)
    assert result.exit_code == 0
    assert "Function not yet supported." in result.output
