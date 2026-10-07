from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from behavior_evals import load_eval_definitions
from contract_consistency import validate_contract_consistency


REQUIRED_SKILL_ROUTES = [
    "references/runtime-stages.md",
    "references/delivery-arc.md",
    "references/output-contract.md",
    "adapters/codex/host-map.md",
    "adapters/claude-code/host-map.md",
    "adapters/codex/assembly.md",
    "adapters/claude-code/assembly.md",
    "core/capability-model.md",
    "REQUIRED-EXECUTION-RECORD.template.md",
    "scripts/validate_harness_skill.py",
    "evals/contract-invariants.json",
    "scripts/contract_consistency.py",
    "scripts/behavior_evals.py",
    "scripts/render_skill_review.py",
]

LINKED_RESOURCE_PATTERN = re.compile(r"`([^`]+\.(?:md|py|json))`")


def read_text(path: Path, errors: list[str]) -> str:
    if not path.exists():
        errors.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def require_tokens(path: Path, tokens: list[str], errors: list[str]) -> None:
    text = read_text(path, errors)
    if not text:
        return
    for token in tokens:
        if token not in text:
            errors.append(f"missing token in {path.name}: {token}")


def parse_frontmatter(text: str, errors: list[str]) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        errors.append("SKILL.md must start with YAML frontmatter")
        return {}

    try:
        end = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration:
        errors.append("SKILL.md frontmatter is missing its closing delimiter")
        return {}

    values: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            errors.append(f"invalid SKILL.md frontmatter line: {line}")
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def validate_frontmatter(root: Path, text: str, errors: list[str]) -> None:
    values = parse_frontmatter(text, errors)
    expected_name = root.name
    if values.get("name") != expected_name:
        errors.append(f"frontmatter name must be {expected_name}")
    if not values.get("description"):
        errors.append("frontmatter description must be non-empty")


def validate_linked_resources(root: Path, skill_text: str, errors: list[str]) -> None:
    for relative_path in sorted(set(LINKED_RESOURCE_PATTERN.findall(skill_text))):
        if not (root / relative_path).is_file():
            errors.append(f"missing linked resource from SKILL.md: {relative_path}")


def validate_generated_artifacts(root: Path, errors: list[str]) -> None:
    for path in root.rglob("*"):
        if path.name == "__pycache__" or path.suffix == ".pyc":
            errors.append(f"generated cache artifact must not ship: {path.relative_to(root)}")


def validate_bundle(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    skill_path = root / "SKILL.md"
    skill_text = read_text(skill_path, errors)

    if skill_text:
        validate_frontmatter(root, skill_text, errors)
        validate_linked_resources(root, skill_text, errors)
        for route in REQUIRED_SKILL_ROUTES:
            if f"`{route}`" not in skill_text:
                errors.append(f"SKILL.md does not route bundled resource: {route}")

    require_tokens(
        skill_path,
        [
            "Trigger -> Load -> Inject -> Orchestrate -> Return",
            "scope_result",
            "operation_state",
        ],
        errors,
    )
    require_tokens(
        root / "references" / "runtime-stages.md",
        ["## Trigger", "## Load", "## Inject", "## Orchestrate", "## Return"],
        errors,
    )
    require_tokens(
        root / "references" / "delivery-arc.md",
        [
            "Foundation and capability proof",
            "Engineering loop",
            "Productization",
            "## Layer 5 guardrail",
            "Reopen Layer 5 whenever quality, security, submission, review, release, or readiness policy changes.",
            "Do not skip Layer 5 just because code already works locally.",
        ],
        errors,
    )
    require_tokens(
        root / "references" / "output-contract.md",
        [
            "## Classification Reply",
            "## Layer Gate Reply",
            "## Closure Reply",
            "scope_result",
            "operation_state",
            "bootstrap_exited",
            "maintenance_continues",
            "in_progress",
        ],
        errors,
    )
    require_tokens(
        root / "adapters" / "codex" / "host-map.md",
        [
            "## Codex Native Entry Surfaces",
            "`AGENTS.md`",
            "`.codex/skills/harness-engineering/SKILL.md`",
            "shell_command",
            "commentary",
            "apply_patch",
            "multi_tool_use.parallel",
            "higher-priority runtime instructions",
            "do not assume the host will automatically prefer the bundle",
            "scope_result",
            "operation_state",
            "update_plan",
        ],
        errors,
    )
    require_tokens(
        root / "adapters" / "codex" / "assembly.md",
        [
            "## 0. Install Shape",
            "## 3. Execution Contract",
            "## 4. Delegation Contract",
            "## 5. Validation Call",
            "higher-priority runtime instructions",
            "do not assume Codex will automatically prefer the bundle",
            "scope_result",
            "operation_state",
            "update_plan",
            "multi_tool_use.parallel",
            "optional templates rather than required host-native agents",
        ],
        errors,
    )
    require_tokens(
        root / "adapters" / "claude-code" / "host-map.md",
        [
            "## Claude Code Native Entry Surfaces",
            "`CLAUDE.md`",
            "`.claude/skills/harness-engineering/SKILL.md`",
            "TaskCreate/TaskUpdate",
            "Agent",
            "higher-priority runtime instructions",
            "do not assume Claude Code will automatically prefer the bundle",
            "scope_result",
            "operation_state",
            "bootstrap_exited",
            "maintenance_continues",
            "in_progress",
        ],
        errors,
    )
    require_tokens(
        root / "adapters" / "claude-code" / "assembly.md",
        [
            "## 0. Install Shape",
            "## 3. Skill Invocation Contract",
            "## 4. Agent Delegation Contract",
            "## 5. Validation Call",
            "higher-priority runtime instructions",
            "do not assume Claude Code will automatically prefer the bundle",
            "scope_result",
            "operation_state",
            "Agent",
            "delegation preserves layer discipline instead of hiding it",
            "`.claude/agents/`",
            "optional templates rather than required host-native agents",
        ],
        errors,
    )
    validate_generated_artifacts(root, errors)
    errors.extend(validate_contract_consistency(root))
    _, eval_errors = load_eval_definitions(root)
    errors.extend(eval_errors)
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python validate_harness_skill.py <bundle-root>")
        return 2

    errors = validate_bundle(Path(sys.argv[1]))
    if errors:
        print("\n".join(errors))
        return 1

    print("OK: shared harness-engineering structure present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
