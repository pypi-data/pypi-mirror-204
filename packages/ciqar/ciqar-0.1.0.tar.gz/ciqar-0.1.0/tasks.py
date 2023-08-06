"""
invoke file for the Ciqar project.

(This is similar to a 'Makefile' - see https://www.pyinvoke.org/)
"""

from invoke import Context, task


@task
def test(ctx: Context) -> None:
    """
    Run all unit tests and create a HTML code coverage report.
    """
    ctx.run("PYTHONPATH=src py.test")


@task
def mypy(ctx: Context) -> None:
    """
    Analyze all sources using MyPy.
    """
    ctx.run("mypy --config-file mypy.ini src test | tee mypy.log")


@task
def pyright(ctx: Context) -> None:
    """
    Analyze all sources using Pyright.
    """
    ctx.run("pyright --outputjson src test > pyright.json")


@task
def build(ctx: Context) -> None:
    """
    Build PyPI package
    """
    ctx.run("flit build")
