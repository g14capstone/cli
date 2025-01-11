import unittest
from click.testing import CliRunner
from src.commands.metrics import metrics


class TestMachineMetricsCommand(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.runner = CliRunner()

    def test_cli_machine_metrics(self):
        result = self.runner.invoke(metrics)
        assert result.exit_code == 0
        assert "Function not yet supported." in result.output
