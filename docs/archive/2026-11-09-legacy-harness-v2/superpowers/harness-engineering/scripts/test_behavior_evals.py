import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True


def _remove_module_cache_file() -> None:
    cached = globals().get("__cached__")
    if not cached:
        return
    cached_path = Path(cached)
    try:
        if cached_path.is_file():
            cached_path.unlink()
        parent = cached_path.parent
        if parent.name == "__pycache__" and parent.is_dir() and not any(parent.iterdir()):
            parent.rmdir()
    except OSError:
        pass


_remove_module_cache_file()


SCRIPT_DIR = Path(__file__).resolve().parent
BUNDLE_ROOT = SCRIPT_DIR.parent
TEMP_ROOT = Path("C:/tmp")
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import behavior_evals


class BehaviorEvalTests(unittest.TestCase):
    maxDiff = None

    def copy_evals(self, destination: Path) -> Path:
        root = destination / "bundle"
        (root / "evals").mkdir(parents=True)
        for filename in ("codex-behavior-evals.json", "claude-behavior-evals.json"):
            shutil.copy2(BUNDLE_ROOT / "evals" / filename, root / "evals" / filename)
        return root

    def load_eval_file(self, root: Path, filename: str) -> dict:
        return json.loads((root / "evals" / filename).read_text(encoding="utf-8"))

    def test_current_eval_definitions_are_valid_and_globally_unique(self):
        definitions, errors = behavior_evals.load_eval_definitions(BUNDLE_ROOT)

        self.assertEqual([], errors)
        self.assertEqual(6, len(definitions))
        self.assertEqual({1, 2, 3, 101, 102, 103}, {definition["id"] for definition in definitions})
        self.assertEqual(6, len({definition["name"] for definition in definitions}))
        self.assertEqual({"codex", "claude-code"}, {definition["host"] for definition in definitions})

    def test_duplicate_eval_id_is_rejected(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temp_dir:
            root = self.copy_evals(Path(temp_dir))
            claude_catalog = self.load_eval_file(root, "claude-behavior-evals.json")
            claude_catalog["evals"][0]["id"] = 1
            (root / "evals" / "claude-behavior-evals.json").write_text(
                json.dumps(claude_catalog, indent=2) + "\n",
                encoding="utf-8",
            )

            _, errors = behavior_evals.load_eval_definitions(root)

            self.assertTrue(any("duplicate behavior eval id" in error for error in errors), errors)

    def test_boolean_eval_id_is_rejected(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temp_dir:
            root = self.copy_evals(Path(temp_dir))
            codex_catalog = self.load_eval_file(root, "codex-behavior-evals.json")
            codex_catalog["evals"][0]["id"] = True
            (root / "evals" / "codex-behavior-evals.json").write_text(
                json.dumps(codex_catalog, indent=2) + "\n",
                encoding="utf-8",
            )

            _, errors = behavior_evals.load_eval_definitions(root)

            self.assertIn("codex-behavior-evals.json eval[0] must have integer id", errors)

    def test_grade_response_returns_pass_for_matching_expectations(self):
        definitions, errors = behavior_evals.load_eval_definitions(BUNDLE_ROOT)
        self.assertEqual([], errors)
        eval_definition = next(
            definition for definition in definitions if definition["name"] == "codex-explicit-invocation"
        )

        result = behavior_evals.grade_response(
            eval_definition,
            "Classification: bootstrap\nstarting from Layer 0\nRequired reads: SPEC.md\nPlease read these files before implementation.",
        )

        self.assertEqual("pass", result["status"])
        self.assertEqual(1, result["eval_id"])
        self.assertEqual("codex-explicit-invocation", result["eval_name"])
        self.assertEqual("codex", result["host"])
        self.assertEqual({"passed": 3, "failed": 0, "total": 3, "pass_rate": 1.0}, result["summary"])
        self.assertEqual(3, len(result["expectations"]))
        self.assertTrue(all(expectation["passed"] for expectation in result["expectations"]))
        self.assertTrue(
            any("matched required terms" in expectation["evidence"] for expectation in result["expectations"])
        )
        self.assertEqual(
            {"eval_id", "eval_name", "host", "status", "expectations", "summary"},
            set(result),
        )

    def test_grade_response_returns_fail_for_forbidden_content(self):
        definitions, errors = behavior_evals.load_eval_definitions(BUNDLE_ROOT)
        self.assertEqual([], errors)
        eval_definition = next(
            definition for definition in definitions if definition["name"] == "codex-near-miss-local-fix"
        )

        result = behavior_evals.grade_response(
            eval_definition,
            "This is a local repair, but Classification: bootstrap and starting from Layer 0 anyway.",
        )

        self.assertEqual("fail", result["status"])
        self.assertEqual({"passed": 1, "failed": 1, "total": 2, "pass_rate": 0.5}, result["summary"])
        self.assertTrue(
            any("forbidden terms present" in expectation["evidence"] for expectation in result["expectations"]),
            result["expectations"],
        )

    def test_grade_response_does_not_treat_layer_number_as_substring_match(self):
        eval_definition = {
            "id": 999,
            "name": "layer-phrase-match",
            "host": "codex",
            "expectations": [{"text": "requires layer 5", "all": ["Layer 5"], "any": [], "none": []}],
        }

        result = behavior_evals.grade_response(eval_definition, "Classification: maintenance starting from Layer 50.")

        self.assertEqual("fail", result["status"])
        self.assertEqual(["missing required terms: ['Layer 5']"], [item["evidence"] for item in result["expectations"]])

    def test_grade_response_does_not_treat_mode_label_as_substring_match(self):
        eval_definition = {
            "id": 1000,
            "name": "mode-phrase-match",
            "host": "codex",
            "expectations": [{"text": "requires bootstrap", "all": ["bootstrap"], "any": [], "none": []}],
        }

        result = behavior_evals.grade_response(eval_definition, "This is not bootstrap; keep the local fix narrow.")

        self.assertEqual("fail", result["status"])
        self.assertEqual(["missing required terms: ['bootstrap']"], [item["evidence"] for item in result["expectations"]])

    def test_missing_response_is_not_run(self):
        definitions, errors = behavior_evals.load_eval_definitions(BUNDLE_ROOT)
        self.assertEqual([], errors)
        eval_definition = next(definition for definition in definitions if definition["id"] == 101)

        result = behavior_evals.grade_response(eval_definition, None)

        self.assertEqual("not-run", result["status"])
        self.assertEqual({"passed": 0, "failed": 0, "total": 0, "pass_rate": None}, result["summary"])
        self.assertEqual([], result["expectations"])

    def test_load_recorded_responses_returns_empty_result_for_none_manifest(self):
        self.assertEqual(({}, []), behavior_evals.load_recorded_responses(None))

    def test_load_recorded_responses_resolves_paths(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temp_dir:
            root = Path(temp_dir)
            evidence_dir = root / "fixtures"
            evidence_dir.mkdir()
            response_path = evidence_dir / "response.md"
            response_path.write_text("Classification: bootstrap", encoding="utf-8")
            manifest_dir = root / "evals"
            manifest_dir.mkdir()
            manifest_path = manifest_dir / "recorded-responses.example.json"
            manifest_path.write_text(
                json.dumps(
                    {
                        "responses": [
                            {
                                "eval_id": 1,
                                "response_path": "../fixtures/response.md",
                                "model": "example-model",
                                "timestamp": "2000-01-01T00:00:00Z",
                            }
                        ]
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            responses, errors = behavior_evals.load_recorded_responses(manifest_path)

            self.assertEqual([], errors)
            self.assertEqual(response_path.resolve(), responses[1]["resolved_path"])

    def test_load_recorded_responses_rejects_manifest_without_responses_list(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temp_dir:
            root = Path(temp_dir)
            manifest_path = root / "recorded-responses.example.json"
            manifest_path.write_text(json.dumps({"items": []}, indent=2) + "\n", encoding="utf-8")

            responses, errors = behavior_evals.load_recorded_responses(manifest_path)

            self.assertEqual({}, responses)
            self.assertEqual(["recorded response manifest must contain a responses list"], errors)

    def test_load_recorded_responses_rejects_manifest_entry_without_response_path(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temp_dir:
            root = Path(temp_dir)
            manifest_path = root / "recorded-responses.example.json"
            manifest_path.write_text(
                json.dumps({"responses": [{"eval_id": 1}]}, indent=2) + "\n",
                encoding="utf-8",
            )

            responses, errors = behavior_evals.load_recorded_responses(manifest_path)

            self.assertEqual({}, responses)
            self.assertIn("recorded response 1 must have response_path", errors)

    def test_load_recorded_responses_rejects_duplicate_eval_id(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temp_dir:
            root = Path(temp_dir)
            response_path = root / "response.md"
            response_path.write_text("ok", encoding="utf-8")
            manifest_path = root / "recorded-responses.example.json"
            manifest_path.write_text(
                json.dumps(
                    {
                        "responses": [
                            {"eval_id": 1, "response_path": "response.md"},
                            {"eval_id": 1, "response_path": "response.md"},
                        ]
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            responses, errors = behavior_evals.load_recorded_responses(manifest_path)

            self.assertEqual({1}, set(responses))
            self.assertIn("duplicate recorded response eval_id: 1", errors)


if __name__ == "__main__":
    unittest.main()
