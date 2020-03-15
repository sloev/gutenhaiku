import os
import json
from click.testing import CliRunner

from gutenhaiku.app import cli
from gutenhaiku import models


def test_0_splash():
    runner = CliRunner()
    result = runner.invoke(cli)
    with open("tests/app_splash.txt") as f:
        assert result.output == f.read()


def test_1_setup():
    runner = CliRunner()
    result = runner.invoke(cli, ["setup"])
    setup = open("tests/app_setup.txt").read()
    already_downloaded_setup = open("tests/app_setup_already_downloaded.txt").read()
    assert any(result.output == output for output in [setup, already_downloaded_setup])


def test_2_extract_haikus():
    runner = CliRunner()
    input_text = open("tests/input_text.txt").read()

    with runner.isolated_filesystem():
        with open("input_text.txt", "w") as f:
            f.write(input_text)

        result = runner.invoke(
            cli,
            [
                "-o",
                "haikus.json",
                "-f",
                "input_text.txt",
                "-a",
                "mary shelley",
                "-t",
                "frankenstein",
                "-d",
                "1818-01-01",
            ],
        )

        haikus = [json.loads(l) for l in open("haikus.json").readlines()]
        print(json.dumps(haikus))

        assert haikus == [
            {
                "page": 0,
                "word_number": 33,
                "haiku": [
                    "Towards the corpse of.",
                    "My wife I rushed towards the.",
                    "Window and drawing.",
                ],
                "author": "mary shelley",
                "title": "frankenstein",
                "date": "1818-01-01T00:00:00",
            }
        ]
