import os
from click.testing import CliRunner

from gutenhaiku.app import cli
from gutenhaiku import models


def test_splash():
    runner = CliRunner()
    result = runner.invoke(cli)
    with open("tests/app_splash.txt") as f:
        assert result.output == f.read()
