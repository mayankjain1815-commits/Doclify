from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10
    import pytest

    tomllib = pytest.importorskip("tomli")

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = REPO_ROOT / "doclify"


def _package_data_patterns():
    pyproject = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    return pyproject["tool"]["setuptools"]["package-data"]["doclify"]


def test_prompt_files_are_included_in_package_data():
    prompt_files = {
        path.relative_to(PACKAGE_ROOT).as_posix()
        for path in (PACKAGE_ROOT / "prompts").glob("*.txt")
    }
    assert prompt_files, "expected prompt files to exist in doclify/prompts"

    included = set()
    for pattern in _package_data_patterns():
        included.update(
            path.relative_to(PACKAGE_ROOT).as_posix()
            for path in PACKAGE_ROOT.glob(pattern)
            if path.is_file()
        )

    missing = sorted(prompt_files - included)
    assert not missing, (
        "prompt files are missing from [tool.setuptools.package-data] and will "
        f"not be installed: {missing}"
    )
