import invoke

from pathlib import Path


PACKAGE = "pywappalyzer"
REQUIRED_COVERAGE = 90


@invoke.task(help={"python": "Install required packages"})
def install(arg):
    arg.run("pip install -r requirements.txt")


@invoke.task(name="format")
def format_(arg):
    autoflake = "autoflake -i --recursive --remove-all-unused-imports --remove-duplicate-keys --remove-unused-variables"
    arg.run(f"{autoflake} {PACKAGE} tests", echo=True)
    arg.run(f"isort {PACKAGE} tests", echo=True)
    arg.run(f"black {PACKAGE} tests", echo=True)


@invoke.task(
    help={
        "style": "Check style with flake8, isort, and black",
        "typing": "Check typing with mypy",
    }
)
def check(arg, style=True, typing=True):
    if style:
        arg.run(f"flake8 {PACKAGE} tests", echo=True)
        arg.run(f"isort --diff {PACKAGE} tests --check-only", echo=True)
        arg.run(f"black --diff {PACKAGE} tests --check", echo=True)
    if typing:
        arg.run(f"mypy --no-incremental --cache-dir=/dev/null {PACKAGE} tests", echo=True)


@invoke.task
def test(arg):
    arg.run(
        f"pytest --cov={PACKAGE} --cov-fail-under={REQUIRED_COVERAGE} --cov-report term-missing",
        pty=True,
        echo=True,
    )


@invoke.task
def hooks(arg):
    invoke_path = Path(arg.run("which invoke", hide=True).stdout[:-1])
    for src_path in Path(".hooks").iterdir():
        dst_path = Path(".git/hooks") / src_path.name
        print(f"Installing: {dst_path}")
        with open(str(src_path), "r") as f:
            src_data = f.read()
        with open(str(dst_path), "w") as f:
            f.write(src_data.format(invoke_path=invoke_path.parent))
        arg.run(f"chmod +x {dst_path}")