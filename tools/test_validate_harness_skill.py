import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate_harness_skill.py"

SKILL = """---
name: harness-engineering
description: A methodology for building multi-component projects with evidence gates at every layer.
---

# Harness Engineering

Layer 0 Layer 1 Layer 2 Layer 3 Layer 4 Layer 5 Layer 6
"""


def build_minimal(root: Path) -> None:
    for relative, content in {
        "SKILL.md": SKILL,
        "README.md": "# Readme\n",
        "README.zh-CN.md": "# Readme\n",
        "core/flow.md": "# Flow\n",
        "core/layer-details.md": "# Layers\n",
        "core/checklists.md": "# Checks\n",
        "core/exit-and-reentry.md": "# Exit\n",
        "core/capability-model.md": "# Capability\n",
        "adapters/claude-code/host-map.md": "# Host\n",
        "adapters/claude-code/assembly.md": "# Assembly\n",
        "adapters/codex/host-map.md": "# Host\n",
        "adapters/codex/assembly.md": "# Assembly\n",
        "references/methodology.md": "# Method\n",
        "references/agent-templates/chatbot-planner.md": "# Planner\n",
        "references/agent-templates/chatbot-coder.md": "# Coder\n",
        "references/agent-templates/chatbot-debugger.md": "# Debugger\n",
        "references/agent-templates/chatbot-reviewer.md": "# Reviewer\n",
        "goal/SKILL.md": "# Goal\n",
        "goal/references/protocol.json": "{}\n",
        "goal/scripts/validate_goal_skill.py": "",
        "deployment/AGENTS.md": "# Agents\n",
    }.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def run(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-B", str(VALIDATOR), str(root)],
        capture_output=True,
        text=True,
    )


def run_with_flag(root: Path, *flags: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-B", str(VALIDATOR), str(root), *flags],
        capture_output=True,
        text=True,
    )


def test_repository_passes_its_own_validator():
    result = run(ROOT)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS" in result.stdout


def test_minimal_tree_passes(tmp_path):
    build_minimal(tmp_path)
    result = run(tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr


def test_missing_required_file_fails(tmp_path):
    build_minimal(tmp_path)
    (tmp_path / "core" / "flow.md").unlink()
    result = run(tmp_path)
    assert result.returncode == 1
    assert "missing required file: core/flow.md" in result.stdout


def test_broken_relative_link_fails(tmp_path):
    build_minimal(tmp_path)
    (tmp_path / "README.md").write_text("[missing](docs/nope.md)\n", encoding="utf-8")
    result = run(tmp_path)
    assert result.returncode == 1
    assert "broken link" in result.stdout


def test_legacy_reference_fails(tmp_path):
    build_minimal(tmp_path)
    (tmp_path / "core" / "flow.md").write_text("see superpowers/harness-engineering\n", encoding="utf-8")
    result = run(tmp_path)
    assert result.returncode == 1
    assert "legacy reference" in result.stdout


def test_frontmatter_name_is_enforced(tmp_path):
    build_minimal(tmp_path)
    (tmp_path / "SKILL.md").write_text(SKILL.replace("name: harness-engineering", "name: other"), encoding="utf-8")
    result = run(tmp_path)
    assert result.returncode == 1
    assert "frontmatter name" in result.stdout


def test_installed_mode_allows_a_skill_copy_without_repo_docs(tmp_path):
    build_minimal(tmp_path)
    shutil.rmtree(tmp_path / "goal")
    (tmp_path / "deployment" / "AGENTS.md").unlink()
    (tmp_path / "deployment").rmdir()
    (tmp_path / "README.md").unlink()
    (tmp_path / "README.zh-CN.md").unlink()
    result = run_with_flag(tmp_path, "--installed")
    assert result.returncode == 0, result.stdout + result.stderr
