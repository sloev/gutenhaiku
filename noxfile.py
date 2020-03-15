"""
for info on how to run nox together with pyenv see:
https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/MAC_SETUP.md#using-pyenv-virtualenv
"""

import nox

nox.options.sessions = [
    "lint",
    "test",
]


@nox.session(python=False)
def install_pyenv_versions(session):
    session.run("pyenv", "install", "-s", "3.7.5", external=True, silent=True)


@nox.session(python=["3.7"], reuse_venv=True)
def test(session):
    session.run("gutenhaiku", "setup", external=True)
    session.run("pytest", "tests")


@nox.session(python=["3.7"], reuse_venv=True)
def lint(session):
    session.install("black")
    session.run("black", "--check", ".")
