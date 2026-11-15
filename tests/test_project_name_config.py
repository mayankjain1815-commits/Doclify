from doclify.components import run as run_module
from doclify.components import update as update_module


CONFIG = """\
project: My Awesome Project
structure:
  - main.py
llm:
  model: test-model
"""


def _write_project(tmp_path):
    (tmp_path / "doclify.yaml").write_text(CONFIG, encoding="utf-8")
    (tmp_path / "main.py").write_text("x = 1\n", encoding="utf-8")


def _fake_extract(path):
    return [f"File: {path}\n```python\nx = 1\n```"]


def test_run_passes_configured_project_name_to_readme(tmp_path, monkeypatch):
    _write_project(tmp_path)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(run_module, "extract_file_content", _fake_extract)
    monkeypatch.setattr(run_module, "generate_doc", lambda *args, **kwargs: "summary")

    captured = {}

    def fake_generate_readme(cache, config, llm_config=None, metadata=None):
        captured.update(metadata or {})
        return True

    monkeypatch.setattr(run_module, "generate_readme_file", fake_generate_readme)

    run_module.run_docs()

    assert captured.get("project_name") == "My Awesome Project"


def test_update_passes_configured_project_name_to_readme(tmp_path, monkeypatch):
    _write_project(tmp_path)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(update_module, "extract_file_content", _fake_extract)
    monkeypatch.setattr(update_module, "generate_doc", lambda *args, **kwargs: "summary")
    monkeypatch.setattr(update_module.Confirm, "ask", lambda *args, **kwargs: True)

    captured = {}

    def fake_generate_readme(cache, config, llm_config=None, metadata=None):
        captured.update(metadata or {})
        return True

    monkeypatch.setattr(update_module, "generate_readme_file", fake_generate_readme)

    update_module.update_docs(".")

    assert captured.get("project_name") == "My Awesome Project"
