# Harness Skill Quality Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a deterministic quality gate that detects high-value contract drift, validates and grades recorded behavior evals, and renders truthful review evidence for the `harness-engineering` skill bundle.

**Architecture:** Keep `scripts/validate_harness_skill.py` as the stable public entry point and delegate focused work to three modules: contract consistency, behavior eval grading, and review rendering. Store validation-only invariants in JSON, preserve external benchmark/model execution as a separate concern, and represent missing live responses as `not-run` rather than success.

**Tech Stack:** Python 3 standard library (`unittest`, `json`, `argparse`, `pathlib`, `datetime`), Markdown, JSON, PowerShell test commands.

**Harness Classification:** `maintenance`, starting from Layer `5` because this changes governance, validation, and evidence closure without changing the method topology or product contracts.

---

## File Structure

- `harness-engineering/evals/contract-invariants.json`
  Validation-only catalog of shared concepts and the documents in which each concept must remain discoverable.

- `harness-engineering/scripts/contract_consistency.py`
  Loads and validates the invariant catalog, then reports missing documents or concepts.

- `harness-engineering/scripts/test_contract_consistency.py`
  Unit tests for valid catalogs, malformed catalogs, and deliberate document drift.

- `harness-engineering/scripts/behavior_evals.py`
  Validates host eval definitions and grades recorded response text into skill-creator-compatible expectation records.

- `harness-engineering/scripts/test_behavior_evals.py`
  Unit tests for eval schema errors, duplicate IDs, pass/fail grading, and `not-run` behavior.

- `harness-engineering/scripts/render_skill_review.py`
  CLI and pure renderer that combines structure, consistency, eval-definition, recorded-response, and optional benchmark evidence.

- `harness-engineering/scripts/test_render_skill_review.py`
  Unit tests for truthful status rendering and evidence paths.

- `harness-engineering/scripts/validate_harness_skill.py`
  Existing public validator; modified only to orchestrate the focused validators.

- `harness-engineering/scripts/test_validate_harness_skill.py`
  Existing integration tests; extended to prove drift and malformed eval definitions fail the public command path.

- `harness-engineering/evals/codex-behavior-evals.json`
- `harness-engineering/evals/claude-behavior-evals.json`
  Existing host prompts migrated to structured, deterministic expectations while keeping human-readable expected output.

- `harness-engineering/evals/recorded-responses.example.json`
  Example manifest showing how real host outputs are supplied without claiming the example was executed.

- `harness-engineering/docs/reviews/2026-07-12-harness-engineering-skill-review.md`
  Generated evidence report. Missing live responses remain visibly `not-run`.

- `harness-engineering/SKILL.md`
  Adds cold-path routing to the quality-gate command without expanding the hot-path method.

## Stable Interfaces

```python
# contract_consistency.py
def validate_contract_consistency(
    root: Path,
    catalog_path: Path | None = None,
) -> list[str]: ...

# behavior_evals.py
def load_eval_definitions(root: Path) -> tuple[list[dict], list[str]]: ...
def grade_response(eval_definition: dict, response_text: str | None) -> dict: ...
def load_recorded_responses(manifest_path: Path | None) -> tuple[dict[int, dict], list[str]]: ...

# render_skill_review.py
def build_review(
    root: Path,
    response_manifest: Path | None = None,
    benchmark_path: Path | None = None,
    generated_at: str | None = None,
) -> tuple[str, list[str]]: ...
```

---

### Task 1: Add the Contract Invariant Checker

**Files:**
- Create: `harness-engineering/evals/contract-invariants.json`
- Create: `harness-engineering/scripts/contract_consistency.py`
- Create: `harness-engineering/scripts/test_contract_consistency.py`

- [ ] **Step 1: Write failing tests for valid documents, deliberate drift, and malformed catalog data**

Create `harness-engineering/scripts/test_contract_consistency.py`:

```python
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from contract_consistency import validate_contract_consistency


SCRIPT_DIR = Path(__file__).resolve().parent
BUNDLE_ROOT = SCRIPT_DIR.parent


class ContractConsistencyTests(unittest.TestCase):
    def copy_bundle(self, destination: Path) -> Path:
        target = destination / "harness-engineering"
        shutil.copytree(
            BUNDLE_ROOT,
            target,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        return target

    def test_current_bundle_satisfies_contract_invariants(self):
        self.assertEqual([], validate_contract_consistency(BUNDLE_ROOT))

    def test_missing_mirrored_concept_reports_invariant_and_path(self):
        with tempfile.TemporaryDirectory(dir=BUNDLE_ROOT.parent) as temp_dir:
            root = self.copy_bundle(Path(temp_dir))
            flow = root / "core" / "flow.md"
            flow.write_text(
                flow.read_text(encoding="utf-8")
                .replace("smallest affected layer", "an unspecified layer", 1)
                .replace("minimum rollback scope", "broad rollback", 1),
                encoding="utf-8",
            )

            errors = validate_contract_consistency(root)

            self.assertTrue(
                any(
                    "minimal-rollback" in error and "core/flow.md" in error
                    for error in errors
                ),
                errors,
            )

    def test_duplicate_invariant_id_is_rejected(self):
        with tempfile.TemporaryDirectory(dir=BUNDLE_ROOT.parent) as temp_dir:
            root = self.copy_bundle(Path(temp_dir))
            catalog = root / "evals" / "contract-invariants.json"
            data = json.loads(catalog.read_text(encoding="utf-8"))
            data["invariants"].append(data["invariants"][0])
            catalog.write_text(json.dumps(data), encoding="utf-8")

            errors = validate_contract_consistency(root)

            self.assertTrue(any("duplicate invariant id" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and verify RED**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\scripts'
python -m unittest test_contract_consistency.py -v
```

Expected: ERROR with `ModuleNotFoundError: No module named 'contract_consistency'`.

- [ ] **Step 3: Add the validation-only invariant catalog**

Create `harness-engineering/evals/contract-invariants.json`:

```json
{
  "version": 1,
  "invariants": [
    {
      "id": "entry-classification",
      "description": "Execution distinguishes bootstrap from maintenance before selecting a layer.",
      "documents": [
        {"path": "SPEC.md", "required_any": [["bootstrap mode"], ["maintenance mode"]]},
        {"path": "PHASES.md", "required_any": [["bootstrap mode", "bootstrap"], ["maintenance mode", "maintenance"]]},
        {"path": "core/flow.md", "required_any": [["bootstrap mode"], ["maintenance mode"]]},
        {"path": "references/runtime-stages.md", "required_any": [["bootstrap"], ["maintenance"]]}
      ]
    },
    {
      "id": "evidence-before-advance",
      "description": "No layer advances without pass evidence.",
      "documents": [
        {"path": "SPEC.md", "required_any": [["pass evidence", "PASS"]]},
        {"path": "PHASES.md", "required_any": [["pass evidence"]]},
        {"path": "core/flow.md", "required_any": [["pass criteria"]]},
        {"path": "CHECKS.md", "required_any": [["evidence pointer"]]}
      ]
    },
    {
      "id": "minimal-rollback",
      "description": "Rollback targets the smallest layer whose assumption failed.",
      "documents": [
        {"path": "SPEC.md", "required_any": [["smallest upstream layer", "roll back minimally"]]},
        {"path": "PHASES.md", "required_any": [["minimal scope", "smallest layer scope"]]},
        {"path": "core/flow.md", "required_any": [["smallest affected layer", "minimum rollback scope"]]},
        {"path": "core/exit-and-reentry.md", "required_any": [["smallest layer"]]}
      ]
    },
    {
      "id": "layer5-product-contract",
      "description": "Layer 5 requires all four Product Contract fields.",
      "documents": [
        {"path": "SPEC.md", "required_any": [["version declaration"], ["boundary definition"], ["change log"], ["acceptance criteria"]]},
        {"path": "CHECKS.md", "required_any": [["version declaration"], ["boundary definition"], ["change log"], ["acceptance criteria"]]},
        {"path": "core/checklists.md", "required_any": [["version declaration"], ["boundary definition"], ["change log"], ["acceptance criteria"]]}
      ]
    },
    {
      "id": "closure-fields",
      "description": "Closure exposes scope_result and operation_state.",
      "documents": [
        {"path": "SPEC.md", "required_any": [["scope_result"], ["operation_state"]]},
        {"path": "PHASES.md", "required_any": [["scope_result"], ["operation_state"]]},
        {"path": "references/output-contract.md", "required_any": [["scope_result"], ["operation_state"]]}
      ]
    },
    {
      "id": "runtime-writeback",
      "description": "Runtime facts that contradict docs require write-back or rollback.",
      "documents": [
        {"path": "SPEC.md", "required_any": [["runtime facts"], ["write-back", "write back"]]},
        {"path": "PHASES.md", "required_any": [["runtime facts"], ["write back", "written back"]]},
        {"path": "CHECKS.md", "required_any": [["runtime facts"], ["write-back", "write back"]]}
      ]
    }
  ]
}
```

- [ ] **Step 4: Implement the minimal checker**

Create `harness-engineering/scripts/contract_consistency.py`:

```python
import json
from pathlib import Path


def _load_json(path: Path, errors: list[str]) -> object | None:
    if not path.is_file():
        errors.append(f"missing invariant catalog: {path}")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid invariant catalog {path}: {exc}")
        return None


def _validate_catalog(data: object, errors: list[str]) -> list[dict]:
    if not isinstance(data, dict) or data.get("version") != 1:
        errors.append("contract invariant catalog must be an object with version 1")
        return []
    invariants = data.get("invariants")
    if not isinstance(invariants, list):
        errors.append("contract invariant catalog must contain an invariants list")
        return []

    valid: list[dict] = []
    seen: set[str] = set()
    for index, invariant in enumerate(invariants):
        if not isinstance(invariant, dict):
            errors.append(f"invariant at index {index} must be an object")
            continue
        invariant_id = invariant.get("id")
        documents = invariant.get("documents")
        if not isinstance(invariant_id, str) or not invariant_id:
            errors.append(f"invariant at index {index} must have a non-empty id")
            continue
        if invariant_id in seen:
            errors.append(f"duplicate invariant id: {invariant_id}")
            continue
        seen.add(invariant_id)
        if not isinstance(documents, list) or not documents:
            errors.append(f"invariant {invariant_id} must have documents")
            continue
        valid.append(invariant)
    return valid


def validate_contract_consistency(
    root: Path,
    catalog_path: Path | None = None,
) -> list[str]:
    root = root.resolve()
    catalog_path = catalog_path or root / "evals" / "contract-invariants.json"
    errors: list[str] = []
    invariants = _validate_catalog(_load_json(catalog_path, errors), errors)

    for invariant in invariants:
        invariant_id = invariant["id"]
        for document in invariant["documents"]:
            if not isinstance(document, dict):
                errors.append(f"invariant {invariant_id} has a non-object document rule")
                continue
            relative_path = document.get("path")
            required_any = document.get("required_any")
            if not isinstance(relative_path, str) or not isinstance(required_any, list):
                errors.append(f"invariant {invariant_id} has a malformed document rule")
                continue
            path = root / relative_path
            if not path.is_file():
                errors.append(f"invariant {invariant_id} missing document: {relative_path}")
                continue
            text = path.read_text(encoding="utf-8").casefold()
            for alternatives in required_any:
                if not isinstance(alternatives, list) or not alternatives:
                    errors.append(
                        f"invariant {invariant_id} has an empty alternative group for {relative_path}"
                    )
                    continue
                if not any(
                    isinstance(term, str) and term.casefold() in text
                    for term in alternatives
                ):
                    errors.append(
                        f"invariant {invariant_id} missing concept in {relative_path}: "
                        f"one of {alternatives}"
                    )
    return errors
```

- [ ] **Step 5: Run the tests and verify GREEN**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\scripts'
python -m unittest test_contract_consistency.py -v
```

Expected: 3 tests, all `OK`.

- [ ] **Step 6: Commit the isolated checker**

```powershell
git add -- harness-engineering/evals/contract-invariants.json harness-engineering/scripts/contract_consistency.py harness-engineering/scripts/test_contract_consistency.py
git commit -m "test(harness-engineering): add contract drift checker"
```

### Task 2: Integrate Contract and Eval Definition Checks into the Public Validator

**Files:**
- Modify: `harness-engineering/scripts/validate_harness_skill.py`
- Modify: `harness-engineering/scripts/test_validate_harness_skill.py`

- [ ] **Step 1: Add a failing public-path drift test**

Add this test to `HarnessSkillValidatorTests` in `test_validate_harness_skill.py`:

```python
    def test_public_validator_reports_contract_drift(self):
        with tempfile.TemporaryDirectory(dir=BUNDLE_ROOT.parent) as temp_dir:
            root = self.copy_bundle(Path(temp_dir))
            output_contract = root / "references" / "output-contract.md"
            output_contract.write_text(
                output_contract.read_text(encoding="utf-8").replace(
                    "scope_result", "scope-outcome"
                ),
                encoding="utf-8",
            )

            errors = self.validator.validate_bundle(root)

            self.assertTrue(
                any("closure-fields" in error for error in errors),
                errors,
            )
```

- [ ] **Step 2: Run the test and verify RED**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\scripts'
python -m unittest test_validate_harness_skill.HarnessSkillValidatorTests.test_public_validator_reports_contract_drift -v
```

Expected: FAIL because `validate_bundle()` does not yet call the invariant checker.

- [ ] **Step 3: Import and call the focused checker**

At the top of `validate_harness_skill.py`, after the standard imports, add:

```python
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from contract_consistency import validate_contract_consistency
```

Before `return errors` in `validate_bundle`, add:

```python
    errors.extend(validate_contract_consistency(root))
```

- [ ] **Step 4: Run public validator tests and verify GREEN**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\scripts'
python -m unittest test_validate_harness_skill.py -v
```

Expected: all public validator tests pass.

- [ ] **Step 5: Commit the integration**

```powershell
git add -- harness-engineering/scripts/validate_harness_skill.py harness-engineering/scripts/test_validate_harness_skill.py
git commit -m "feat(harness-engineering): enforce contract invariants"
```

### Task 3: Add Structured Behavior Eval Validation and Recorded-Response Grading

**Files:**
- Create: `harness-engineering/scripts/behavior_evals.py`
- Create: `harness-engineering/scripts/test_behavior_evals.py`
- Modify: `harness-engineering/evals/codex-behavior-evals.json`
- Modify: `harness-engineering/evals/claude-behavior-evals.json`
- Create: `harness-engineering/evals/recorded-responses.example.json`
- Modify: `harness-engineering/scripts/validate_harness_skill.py`

- [ ] **Step 1: Write failing schema and grading tests**

Create `harness-engineering/scripts/test_behavior_evals.py`:

```python
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from behavior_evals import grade_response, load_eval_definitions


SCRIPT_DIR = Path(__file__).resolve().parent
BUNDLE_ROOT = SCRIPT_DIR.parent


class BehaviorEvalTests(unittest.TestCase):
    def test_current_eval_definitions_are_valid_and_globally_unique(self):
        definitions, errors = load_eval_definitions(BUNDLE_ROOT)
        self.assertEqual([], errors)
        self.assertEqual(6, len(definitions))
        self.assertEqual(6, len({item["id"] for item in definitions}))

    def test_duplicate_eval_id_is_rejected(self):
        with tempfile.TemporaryDirectory(dir=BUNDLE_ROOT.parent) as temp_dir:
            root = Path(temp_dir)
            shutil.copytree(BUNDLE_ROOT / "evals", root / "evals")
            path = root / "evals" / "codex-behavior-evals.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            data["evals"].append(data["evals"][0])
            path.write_text(json.dumps(data), encoding="utf-8")

            _, errors = load_eval_definitions(root)

            self.assertTrue(any("duplicate behavior eval id" in error for error in errors), errors)

    def test_grade_response_returns_pass_and_assertion_evidence(self):
        definition = {
            "id": 1,
            "name": "classification",
            "host": "codex",
            "expectations": [
                {
                    "text": "classifies bootstrap from Layer 0",
                    "all": ["bootstrap", "Layer 0"],
                    "any": [],
                    "none": ["maintenance"],
                }
            ],
        }
        result = grade_response(definition, "Classification: bootstrap, starting from Layer 0")
        self.assertEqual("pass", result["status"])
        self.assertTrue(result["expectations"][0]["passed"])
        self.assertIn("matched", result["expectations"][0]["evidence"])

    def test_grade_response_returns_fail_for_forbidden_content(self):
        definition = {
            "id": 1,
            "name": "classification",
            "host": "codex",
            "expectations": [
                {
                    "text": "does not classify maintenance",
                    "all": ["bootstrap"],
                    "any": [],
                    "none": ["maintenance"],
                }
            ],
        }
        result = grade_response(definition, "bootstrap and maintenance")
        self.assertEqual("fail", result["status"])
        self.assertFalse(result["expectations"][0]["passed"])
        self.assertIn("forbidden", result["expectations"][0]["evidence"])

    def test_missing_response_is_not_run(self):
        definition = {"id": 1, "name": "x", "host": "codex", "expectations": []}
        result = grade_response(definition, None)
        self.assertEqual("not-run", result["status"])
        self.assertEqual(0, result["summary"]["total"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and verify RED**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\scripts'
python -m unittest test_behavior_evals.py -v
```

Expected: ERROR with `ModuleNotFoundError: No module named 'behavior_evals'`.

- [ ] **Step 3: Migrate eval definitions to structured expectations**

Use globally unique integer IDs and preserve each existing prompt and `expected_output`. Each eval must have this shape:

```json
{
  "id": 1,
  "name": "codex-explicit-invocation",
  "prompt": "/harness-engineering 我们要替换核心检索组件并重做 bridge 契约。先判断 mode 和 start layer，再说你要读哪些文件。",
  "expected_output": "Triggers the skill, classifies bootstrap, chooses Layer 0 as the smallest valid start layer, and explicitly names the next reads before any implementation.",
  "files": [],
  "expectations": [
    {"text": "classifies bootstrap", "all": ["bootstrap"], "any": [], "none": []},
    {"text": "starts from Layer 0", "all": ["Layer 0"], "any": [], "none": []},
    {"text": "names required reads", "all": [], "any": ["Required reads", "要读取", "read"], "none": []}
  ]
}
```

Keep the top level exactly `{"skill_name": "harness-engineering", "host": "<host>", "evals": [...]}`. Preserve every current prompt and `expected_output`, then use this exact matcher matrix:

| File | ID / name | Expectation matchers |
|---|---|---|
| Codex | `1 / codex-explicit-invocation` | `all=["bootstrap"]`; `all=["Layer 0"]`; `any=["Required reads","要读取","read"]` |
| Codex | `2 / codex-layer-5-governance` | `all=["maintenance"]`; `all=["Layer 5"]`; `any=["evidence","证据","baseline","基线"]` |
| Codex | `3 / codex-near-miss-local-fix` | `any=["local","局部","focused","稳定契约"]`; `none=["Classification: bootstrap","starting from Layer 0","从 Layer 0 开始"]` |
| Claude Code | `101 / claude-explicit-invocation` | `all=["bootstrap"]`; `all=["Layer 0"]`; `any=["evidence","gate","proof"]` |
| Claude Code | `102 / claude-claude-md-entry` | `all=["maintenance"]`; `all=["Layer 2"]`; `any=["bridge","topology","拓扑"]` |
| Claude Code | `103 / claude-agent-discipline` | `any=["Agent","delegation","delegate"]`; `all=["scope_result"]`; `all=["operation_state"]` |

For each semicolon-separated matcher, create one expectation object with a descriptive `text`; fields not shown in the matrix are empty lists. Keep each eval's `files: []`.

- [ ] **Step 4: Implement schema loading and grading**

Create `harness-engineering/scripts/behavior_evals.py`:

```python
import json
from pathlib import Path


EVAL_FILES = (
    "codex-behavior-evals.json",
    "claude-behavior-evals.json",
)


def _load_json(path: Path, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing behavior eval file: {path}")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid behavior eval file {path}: {exc}")
    return None


def _validate_expectation(expectation: object, label: str, errors: list[str]) -> bool:
    if not isinstance(expectation, dict) or not isinstance(expectation.get("text"), str):
        errors.append(f"{label} expectation must contain text")
        return False
    for field in ("all", "any", "none"):
        value = expectation.get(field)
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            errors.append(f"{label} expectation {field} must be a string list")
            return False
    return True


def load_eval_definitions(root: Path) -> tuple[list[dict], list[str]]:
    definitions: list[dict] = []
    errors: list[str] = []
    seen_ids: set[int] = set()
    seen_names: set[str] = set()
    for filename in EVAL_FILES:
        data = _load_json(root / "evals" / filename, errors)
        if not isinstance(data, dict):
            continue
        host = data.get("host")
        evals = data.get("evals")
        if data.get("skill_name") != "harness-engineering" or not isinstance(host, str):
            errors.append(f"{filename} must name the harness-engineering skill and host")
            continue
        if not isinstance(evals, list):
            errors.append(f"{filename} must contain an evals list")
            continue
        for index, item in enumerate(evals):
            label = f"{filename} eval[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{label} must be an object")
                continue
            eval_id = item.get("id")
            name = item.get("name")
            expectations = item.get("expectations")
            if not isinstance(eval_id, int) or not isinstance(name, str) or not name:
                errors.append(f"{label} must have integer id and non-empty name")
                continue
            if eval_id in seen_ids:
                errors.append(f"duplicate behavior eval id: {eval_id}")
                continue
            if name in seen_names:
                errors.append(f"duplicate behavior eval name: {name}")
                continue
            if not isinstance(item.get("prompt"), str) or not isinstance(
                item.get("expected_output"), str
            ):
                errors.append(f"{label} must have prompt and expected_output")
                continue
            files = item.get("files")
            if not isinstance(files, list) or not all(isinstance(path, str) for path in files):
                errors.append(f"{label} files must be a string list")
                continue
            if not isinstance(expectations, list) or not expectations:
                errors.append(f"{label} must have non-empty expectations")
                continue
            if not all(
                _validate_expectation(expectation, label, errors)
                for expectation in expectations
            ):
                continue
            seen_ids.add(eval_id)
            seen_names.add(name)
            definitions.append({**item, "host": host})
    return definitions, errors


def grade_response(eval_definition: dict, response_text: str | None) -> dict:
    if response_text is None:
        return {
            "eval_id": eval_definition["id"],
            "eval_name": eval_definition["name"],
            "host": eval_definition["host"],
            "status": "not-run",
            "expectations": [],
            "summary": {"passed": 0, "failed": 0, "total": 0, "pass_rate": None},
        }

    folded = response_text.casefold()
    graded: list[dict] = []
    for expectation in eval_definition["expectations"]:
        missing_all = [term for term in expectation["all"] if term.casefold() not in folded]
        matched_any = [term for term in expectation["any"] if term.casefold() in folded]
        forbidden = [term for term in expectation["none"] if term.casefold() in folded]
        any_ok = not expectation["any"] or bool(matched_any)
        passed = not missing_all and any_ok and not forbidden
        evidence_parts = []
        if not missing_all and any_ok:
            evidence_parts.append("matched required terms")
        if missing_all:
            evidence_parts.append(f"missing required terms: {missing_all}")
        if not any_ok:
            evidence_parts.append(f"matched none of: {expectation['any']}")
        if forbidden:
            evidence_parts.append(f"forbidden terms present: {forbidden}")
        graded.append(
            {
                "text": expectation["text"],
                "passed": passed,
                "evidence": "; ".join(evidence_parts),
            }
        )

    passed_count = sum(item["passed"] for item in graded)
    total = len(graded)
    failed_count = total - passed_count
    return {
        "eval_id": eval_definition["id"],
        "eval_name": eval_definition["name"],
        "host": eval_definition["host"],
        "status": "pass" if failed_count == 0 else "fail",
        "expectations": graded,
        "summary": {
            "passed": passed_count,
            "failed": failed_count,
            "total": total,
            "pass_rate": passed_count / total if total else None,
        },
    }


def load_recorded_responses(
    manifest_path: Path | None,
) -> tuple[dict[int, dict], list[str]]:
    if manifest_path is None:
        return {}, []
    errors: list[str] = []
    data = _load_json(manifest_path, errors)
    if not isinstance(data, dict) or not isinstance(data.get("responses"), list):
        errors.append("recorded response manifest must contain a responses list")
        return {}, errors
    responses: dict[int, dict] = {}
    for index, item in enumerate(data["responses"]):
        if not isinstance(item, dict) or not isinstance(item.get("eval_id"), int):
            errors.append(f"recorded response[{index}] must have integer eval_id")
            continue
        eval_id = item["eval_id"]
        if eval_id in responses:
            errors.append(f"duplicate recorded response eval_id: {eval_id}")
            continue
        response_path = item.get("response_path")
        if not isinstance(response_path, str):
            errors.append(f"recorded response {eval_id} must have response_path")
            continue
        resolved = (manifest_path.parent / response_path).resolve()
        if not resolved.is_file():
            errors.append(f"recorded response {eval_id} missing file: {resolved}")
            continue
        responses[eval_id] = {**item, "resolved_path": resolved}
    return responses, errors
```

- [ ] **Step 5: Add the non-executed example response manifest**

Create `harness-engineering/evals/recorded-responses.example.json`:

```json
{
  "responses": [
    {
      "eval_id": 1,
      "response_path": "../../external-eval-workspace/codex-explicit-invocation/response.md",
      "model": "example-model",
      "timestamp": "2000-01-01T00:00:00Z"
    }
  ]
}
```

The filename and illustrative values make clear that this is documentation, not executed evidence. Do not feed this example into the report generator during verification.

- [ ] **Step 6: Run the tests and verify GREEN**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\scripts'
python -m unittest test_behavior_evals.py -v
```

Expected: 5 tests, all `OK`.

- [ ] **Step 7: Add eval-definition validation to the public validator**

Import `load_eval_definitions` in `validate_harness_skill.py` beside the contract checker and add this before `return errors`:

```python
    _, eval_errors = load_eval_definitions(root)
    errors.extend(eval_errors)
```

Do not change `REQUIRED_SKILL_ROUTES` in this task. Task 5 adds all new routes together after every routed file exists, preserving a green intermediate state.

- [ ] **Step 8: Commit structured eval support**

```powershell
git add -- harness-engineering/evals harness-engineering/scripts/behavior_evals.py harness-engineering/scripts/test_behavior_evals.py harness-engineering/scripts/validate_harness_skill.py
git commit -m "feat(harness-engineering): grade recorded behavior evals"
```

### Task 4: Generate a Truthful Skill Review Report

**Files:**
- Create: `harness-engineering/scripts/render_skill_review.py`
- Create: `harness-engineering/scripts/test_render_skill_review.py`
- Modify: `harness-engineering/docs/reviews/2026-07-12-harness-engineering-skill-review.md`

- [ ] **Step 1: Write failing report tests**

Create `harness-engineering/scripts/test_render_skill_review.py`:

```python
from pathlib import Path
import tempfile
import unittest

from render_skill_review import build_review


SCRIPT_DIR = Path(__file__).resolve().parent
BUNDLE_ROOT = SCRIPT_DIR.parent


class RenderSkillReviewTests(unittest.TestCase):
    def test_missing_live_responses_are_rendered_as_not_run(self):
        report, errors = build_review(
            BUNDLE_ROOT,
            generated_at="2026-07-12T00:00:00Z",
        )
        self.assertEqual([], errors)
        self.assertIn("Overall behavior status: `not-run`", report)
        self.assertIn("codex-explicit-invocation", report)
        self.assertNotIn("pass/fail", report)

    def test_missing_benchmark_is_reported_without_becoming_a_failure(self):
        missing = BUNDLE_ROOT / "evals" / "missing-benchmark.json"
        report, errors = build_review(
            BUNDLE_ROOT,
            benchmark_path=missing,
            generated_at="2026-07-12T00:00:00Z",
        )
        self.assertTrue(any("benchmark" in error for error in errors), errors)
        self.assertIn("External benchmark: `not-run`", report)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and verify RED**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\scripts'
python -m unittest test_render_skill_review.py -v
```

Expected: ERROR with `ModuleNotFoundError: No module named 'render_skill_review'`.

- [ ] **Step 3: Implement the renderer and CLI**

Create `harness-engineering/scripts/render_skill_review.py`:

```python
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

from behavior_evals import grade_response, load_eval_definitions, load_recorded_responses
from contract_consistency import validate_contract_consistency


def _benchmark_summary(path: Path | None) -> tuple[list[str], list[str]]:
    if path is None:
        return ["External benchmark: `not-run`"], []
    if not path.is_file():
        return ["External benchmark: `not-run`"], [f"missing benchmark: {path}"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        metadata = data["metadata"]
        summary = data["run_summary"]
        with_skill = summary["with_skill"]["pass_rate"]["mean"]
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        return ["External benchmark: `fail`"], [f"invalid benchmark {path}: {exc}"]
    return [
        "External benchmark: `pass`",
        f"- Evidence: `{path}`",
        f"- Model: `{metadata.get('executor_model', 'unknown')}`",
        f"- With-skill mean pass rate: `{with_skill}`",
    ], []


def build_review(
    root: Path,
    response_manifest: Path | None = None,
    benchmark_path: Path | None = None,
    generated_at: str | None = None,
) -> tuple[str, list[str]]:
    root = root.resolve()
    generated_at = generated_at or datetime.now(timezone.utc).isoformat()
    invariant_errors = validate_contract_consistency(root)
    definitions, definition_errors = load_eval_definitions(root)
    responses, response_errors = load_recorded_responses(response_manifest)
    errors = [*invariant_errors, *definition_errors, *response_errors]

    grades = []
    for definition in definitions:
        recorded = responses.get(definition["id"])
        response_text = None
        evidence_path = None
        if recorded is not None:
            evidence_path = recorded["resolved_path"]
            response_text = evidence_path.read_text(encoding="utf-8")
        grade = grade_response(definition, response_text)
        grade["evidence_path"] = evidence_path
        grades.append(grade)

    behavior_status = "not-run"
    if grades and all(item["status"] != "not-run" for item in grades):
        behavior_status = "pass" if all(item["status"] == "pass" for item in grades) else "fail"
    elif any(item["status"] == "fail" for item in grades):
        behavior_status = "fail"

    benchmark_lines, benchmark_errors = _benchmark_summary(benchmark_path)
    errors.extend(benchmark_errors)
    lines = [
        "# Harness Engineering Skill Review Log — 2026-07-12",
        "",
        f"Generated at: `{generated_at}`",
        "",
        "## Bundle Quality Gate",
        "",
        f"Contract consistency: `{'pass' if not invariant_errors else 'fail'}`",
        f"Eval definition schema: `{'pass' if not definition_errors else 'fail'}`",
        "",
        "## Recorded Host Behavior",
        "",
        f"Overall behavior status: `{behavior_status}`",
        "",
    ]
    for grade in grades:
        lines.append(f"### {grade['eval_name']}")
        lines.append("")
        lines.append(f"- Host: `{grade['host']}`")
        lines.append(f"- Status: `{grade['status']}`")
        if grade["evidence_path"] is not None:
            lines.append(f"- Evidence: `{grade['evidence_path']}`")
        else:
            lines.append("- Evidence: recorded response not supplied")
        for expectation in grade["expectations"]:
            status = "pass" if expectation["passed"] else "fail"
            lines.append(f"- `{status}` {expectation['text']}: {expectation['evidence']}")
        lines.append("")
    lines.extend(["## Imported External Benchmark", "", *benchmark_lines, ""])
    if errors:
        lines.extend(["## Validation Errors", ""])
        lines.extend(f"- {error}" for error in errors)
        lines.append("")
    return "\n".join(lines), errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle_root", type=Path)
    parser.add_argument("--responses", type=Path)
    parser.add_argument("--benchmark", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report, errors = build_review(
        args.bundle_root,
        response_manifest=args.responses,
        benchmark_path=args.benchmark,
    )
    args.output.write_text(report + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run renderer tests and verify GREEN**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\scripts'
python -m unittest test_render_skill_review.py -v
```

Expected: 2 tests, all `OK`.

- [ ] **Step 5: Generate the current truthful report without fake live results**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
python .\harness-engineering\scripts\render_skill_review.py .\harness-engineering --output .\harness-engineering\docs\reviews\2026-07-12-harness-engineering-skill-review.md
```

Expected:
- exit `0`;
- report says contract consistency `pass`;
- eval definition schema `pass`;
- overall behavior `not-run`;
- every host eval says recorded response not supplied;
- external benchmark says `not-run`.

- [ ] **Step 6: Commit the review renderer and generated report**

```powershell
git add -- harness-engineering/scripts/render_skill_review.py harness-engineering/scripts/test_render_skill_review.py harness-engineering/docs/reviews/2026-07-12-harness-engineering-skill-review.md
git commit -m "feat(harness-engineering): render quality gate evidence"
```

### Task 5: Route the Quality Gate Without Expanding the Skill Hot Path

**Files:**
- Modify: `harness-engineering/SKILL.md`
- Modify: `harness-engineering/scripts/validate_harness_skill.py`
- Test: `harness-engineering/scripts/test_validate_harness_skill.py`

- [ ] **Step 1: Add a failing route-coverage assertion**

In `validate_harness_skill.py`, extend `REQUIRED_SKILL_ROUTES` with the following entries, but do not edit `SKILL.md` yet:

```python
    "evals/contract-invariants.json",
    "scripts/contract_consistency.py",
    "scripts/behavior_evals.py",
    "scripts/render_skill_review.py",
```

Do not add the example response manifest to required runtime routes. The existing `test_repository_bundle_passes_complete_validation` assertion exercises all required routes.

- [ ] **Step 2: Run the public test and verify RED**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\scripts'
python -m unittest test_validate_harness_skill.HarnessSkillValidatorTests.test_repository_bundle_passes_complete_validation -v
```

Expected: FAIL with `SKILL.md does not route bundled resource` for the four new quality-gate resources.

- [ ] **Step 3: Add one cold-path quality-gate paragraph to `SKILL.md`**

Append this under `## Reusable Resources And Validation`:

```markdown
- For bundle-quality work, use `evals/contract-invariants.json` through `scripts/contract_consistency.py`, validate recorded host outputs with `scripts/behavior_evals.py`, and generate review evidence with `scripts/render_skill_review.py`. Missing host output remains `not-run`; static checks never prove live behavior.
```

Do not add these resources to the Five-Stage Runtime or Hot-Path Rules sections.

- [ ] **Step 4: Run the public validator tests and verify GREEN**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\scripts'
python -m unittest test_validate_harness_skill.py -v
```

Expected: all tests pass.

- [ ] **Step 5: Commit the cold-path route**

```powershell
git add -- harness-engineering/SKILL.md harness-engineering/scripts/test_validate_harness_skill.py
git commit -m "docs(harness-engineering): route skill quality gate"
```

### Task 6: Full Verification and Layer 5 Closure

**Files:**
- Validate: `harness-engineering/scripts/test_*.py`
- Validate: `harness-engineering/scripts/validate_harness_skill.py`
- Validate: `harness-engineering/docs/reviews/2026-07-12-harness-engineering-skill-review.md`
- Validate: all changed files with `git diff --check`

- [ ] **Step 1: Run the complete script test suite**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\scripts'
python -m unittest discover -p 'test_*.py' -v
```

Expected: all tests pass with `OK` and zero failures/errors.

- [ ] **Step 2: Run the public bundle validator**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
python .\harness-engineering\scripts\validate_harness_skill.py .\harness-engineering
```

Expected: exit `0` with `OK: shared harness-engineering structure present`.

- [ ] **Step 3: Regenerate the review report from current workspace evidence**

Run:

```powershell
python .\harness-engineering\scripts\render_skill_review.py .\harness-engineering --output .\harness-engineering\docs\reviews\2026-07-12-harness-engineering-skill-review.md
```

Expected: exit `0`; live host behavior remains `not-run` until real recorded outputs are supplied.

- [ ] **Step 4: Verify no placeholder status or whitespace errors remain**

Run:

```powershell
Select-String -Path '.\harness-engineering\docs\reviews\2026-07-12-harness-engineering-skill-review.md' -Pattern 'pass/fail|Evidence:\s*$'
git diff --check -- harness-engineering docs/superpowers/plans/2026-07-12-harness-skill-quality-gate.md
```

Expected: no placeholder matches and no diff-check output.

- [ ] **Step 5: Inspect only the intended changed-file set**

Run:

```powershell
git status --short -- harness-engineering docs/superpowers/plans/2026-07-12-harness-skill-quality-gate.md
```

Expected: only files named by this plan are changed; unrelated pre-existing worktree changes remain untouched.

- [ ] **Step 6: Commit the final generated evidence if it changed after verification**

```powershell
git add -- harness-engineering/docs/reviews/2026-07-12-harness-engineering-skill-review.md docs/superpowers/plans/2026-07-12-harness-skill-quality-gate.md
git commit -m "test(harness-engineering): close skill quality gate"
```

- [ ] **Step 7: Record Harness Engineering closure**

Use the exact closure fields:

```markdown
Mode: maintenance
Start Layer: 5
Touched Layers: [5]
Layer Outcomes: Layer 5 pass
Evidence Pointers: unit-test output, public validator output, generated review log, git diff check
Rollback Decisions: none
scope_result: accepted
operation_state: maintenance_continues
```

If any verification command fails, set `scope_result: rework-required` and `operation_state: in_progress`; do not claim Layer 5 passed.

---

## Self-Review

### Spec Coverage

- Cross-document semantic consistency: Tasks 1 and 2.
- Deterministic eval-definition validation and recorded-response grading: Task 3.
- Truthful `pass` / `fail` / `not-run` evidence report: Task 4.
- Stable public validator and short Skill hot path: Tasks 2 and 5.
- TDD, compatibility, safety, and fresh closure evidence: every implementation task and Task 6.
- No model invocation, document generation, installed-copy sync, or extra Harness layer: explicitly excluded from all tasks.

### Placeholder Scan

- The strings `pass/fail` and `placeholder` appear only when a test intentionally proves the generated review does not contain them.
- No `TBD`, `TODO`, `implement later`, or `fill in details` instructions remain.

### Type and Schema Consistency

- Eval IDs are globally unique integers: Codex `1..3`, Claude Code `101..103`.
- Every grading result uses `text`, `passed`, and `evidence`.
- Status values are exactly `pass`, `fail`, and `not-run`.
- The public validator continues to return `list[str]` from `validate_bundle(root)` and exit `0` only when the list is empty.
- Missing live outputs never become successful behavior evidence.

### Execution Safety

- Tests mutate temporary bundle copies only.
- No network, model credential, installed Skill directory, push, release, or shared environment is touched.
- Each commit stages explicit paths so unrelated dirty-worktree changes are preserved.
