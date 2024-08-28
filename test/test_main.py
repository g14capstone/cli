from click.testing import CliRunner
from src.main import main


def test_main():
    """test main entrypoint with basic input"""
    runner = CliRunner()
    result = runner.invoke(main, ["--msg=sample message"])
    assert result.exit_code == 0
    assert result.output == "sample message\n"
