import importlib.util
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
VALIDATOR_PATH = SCRIPT_DIR / "contract_consistency.py"


def load_validator_module():
    spec = importlib.util.spec_from_file_location("contract_consistency", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ContractConsistencyTests(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        cls.validator = load_validator_module()

    def copy_bundle(self, destination: Path) -> Path:
        target = destination / "harness-engineering"
        shutil.copytree(
            BUNDLE_ROOT,
            target,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        return target

    def load_catalog(self, root: Path = BUNDLE_ROOT) -> dict:
        return json.loads((root / "evals" / "contract-invariants.json").read_text(encoding="utf-8"))

    def test_current_bundle_satisfies_contract_invariants(self):
        self.assertEqual([], self.validator.validate_contract_consistency(BUNDLE_ROOT))

    def test_relative_catalog_path_override_resolves_from_root(self):
        with tempfile.TemporaryDirectory(dir=BUNDLE_ROOT.parent) as temp_dir:
            root = self.copy_bundle(Path(temp_dir))
            errors = self.validator.validate_contract_consistency(
                root,
                Path("evals/contract-invariants.json"),
            )
            self.assertEqual([], errors)

    def test_catalog_stays_shared_contract_focused(self):
        catalog = self.load_catalog()
        invariants = {invariant["id"]: invariant["documents"] for invariant in catalog["invariants"]}

        self.assertEqual(
            {
                "entry-classification",
                "evidence-before-advance",
                "minimal-rollback",
                "layer5-product-contract",
                "closure-fields",
                "runtime-writeback",
            },
            set(invariants),
        )

        all_paths = [
            document["path"]
            for documents in invariants.values()
            for document in documents
        ]
        self.assertFalse(any(path.startswith("adapters/") for path in all_paths), all_paths)

        entry_paths = {document["path"] for document in invariants["entry-classification"]}
        self.assertTrue(
            {"SPEC.md", "PHASES.md", "core/flow.md", "references/runtime-stages.md"}.issubset(entry_paths),
            entry_paths,
        )
        entry_groups = [
            token
            for document in invariants["entry-classification"]
            for group in document["required_any"]
            for token in group
        ]
        self.assertFalse(any("start layer" in token.casefold() for token in entry_groups), entry_groups)
        self.assertFalse(any("smallest valid start layer" in token.casefold() for token in entry_groups), entry_groups)

        evidence_paths = {document["path"] for document in invariants["evidence-before-advance"]}
        self.assertIn("CHECKS.md", evidence_paths)

        rollback_paths = {document["path"] for document in invariants["minimal-rollback"]}
        self.assertIn("core/exit-and-reentry.md", rollback_paths)

        closure_paths = {document["path"] for document in invariants["closure-fields"]}
        self.assertIn("references/output-contract.md", closure_paths)

    def test_harmless_doc_paraphrase_still_passes(self):
        with tempfile.TemporaryDirectory(dir=BUNDLE_ROOT.parent) as temp_dir:
            root = self.copy_bundle(Path(temp_dir))
            phases_path = root / "PHASES.md"
            phases_text = phases_path.read_text(encoding="utf-8")
            phases_text = phases_text.replace(
                "## Phase 0: Intake and Entry Classification",
                "## Phase 0: Work Intake and Mode Classification",
                1,
            )
            phases_text = phases_text.replace(
                "Let runtime facts override stale documents; write back or roll back immediately.",
                "Let runtime findings override stale docs; write back or roll back right away.",
                1,
            )
            phases_path.write_text(phases_text, encoding="utf-8")

            errors = self.validator.validate_contract_consistency(root)

            self.assertEqual([], errors)

    def test_missing_mirrored_concept_reports_invariant_and_path(self):
        with tempfile.TemporaryDirectory(dir=BUNDLE_ROOT.parent) as temp_dir:
            root = self.copy_bundle(Path(temp_dir))
            flow_path = root / "core" / "flow.md"
            flow_path.write_text(
                flow_path.read_text(encoding="utf-8").replace(
                    "minimum rollback scope", "rollback scope", 1
                ),
                encoding="utf-8",
            )

            errors = self.validator.validate_contract_consistency(root)

            self.assertTrue(
                any("minimal-rollback" in error and "core/flow.md" in error for error in errors),
                errors,
            )

    def test_missing_referenced_document_reports_invariant_and_path(self):
        with tempfile.TemporaryDirectory(dir=BUNDLE_ROOT.parent) as temp_dir:
            root = self.copy_bundle(Path(temp_dir))
            target = root / "core" / "exit-and-reentry.md"
            target.unlink()

            errors = self.validator.validate_contract_consistency(root)

            self.assertTrue(
                any(
                    "minimal-rollback" in error and "core/exit-and-reentry.md" in error
                    for error in errors
                ),
                errors,
            )

    def test_duplicate_invariant_id_is_rejected(self):
        with tempfile.TemporaryDirectory(dir=BUNDLE_ROOT.parent) as temp_dir:
            root = self.copy_bundle(Path(temp_dir))
            catalog = self.load_catalog(root)
            catalog["invariants"].append(dict(catalog["invariants"][0]))
            (root / "evals" / "contract-invariants.json").write_text(
                json.dumps(catalog, indent=2) + "\n",
                encoding="utf-8",
            )

            errors = self.validator.validate_contract_consistency(root)

            self.assertTrue(any("duplicate invariant id" in error for error in errors), errors)

    def test_invalid_document_rule_is_rejected(self):
        with tempfile.TemporaryDirectory(dir=BUNDLE_ROOT.parent) as temp_dir:
            root = self.copy_bundle(Path(temp_dir))
            catalog = self.load_catalog(root)
            catalog["invariants"][0]["documents"][0]["path"] = 7
            catalog["invariants"][0]["documents"][1]["required_any"] = "bootstrap mode"
            (root / "evals" / "contract-invariants.json").write_text(
                json.dumps(catalog, indent=2) + "\n",
                encoding="utf-8",
            )

            errors = self.validator.validate_contract_consistency(root)

            self.assertTrue(any("must define a non-empty string path" in error for error in errors), errors)
            self.assertTrue(any("must define non-empty required_any" in error for error in errors), errors)

    def test_malformed_document_rule_does_not_suppress_valid_sibling_drift(self):
        with tempfile.TemporaryDirectory(dir=BUNDLE_ROOT.parent) as temp_dir:
            root = self.copy_bundle(Path(temp_dir))
            catalog = self.load_catalog(root)
            catalog["invariants"][2]["documents"][0]["path"] = 7
            (root / "evals" / "contract-invariants.json").write_text(
                json.dumps(catalog, indent=2) + "\n",
                encoding="utf-8",
            )
            flow_path = root / "core" / "flow.md"
            flow_path.write_text(
                flow_path.read_text(encoding="utf-8").replace(
                    "minimum rollback scope", "rollback scope", 1
                ),
                encoding="utf-8",
            )

            errors = self.validator.validate_contract_consistency(root)

            self.assertTrue(any("must define a non-empty string path" in error for error in errors), errors)
            self.assertTrue(
                any("minimal-rollback" in error and "core/flow.md" in error for error in errors),
                errors,
            )

    def test_invalid_or_missing_catalog_version_is_rejected(self):
        for version in (None, 2):
            with self.subTest(version=version):
                with tempfile.TemporaryDirectory(dir=BUNDLE_ROOT.parent) as temp_dir:
                    root = self.copy_bundle(Path(temp_dir))
                    catalog = self.load_catalog(root)
                    if version is None:
                        catalog.pop("version")
                    else:
                        catalog["version"] = version
                    (root / "evals" / "contract-invariants.json").write_text(
                        json.dumps(catalog, indent=2) + "\n",
                        encoding="utf-8",
                    )

                    errors = self.validator.validate_contract_consistency(root)

                    self.assertTrue(any("catalog version must be 1" in error for error in errors), errors)

    def test_missing_invariants_list_is_rejected(self):
        with tempfile.TemporaryDirectory(dir=BUNDLE_ROOT.parent) as temp_dir:
            root = self.copy_bundle(Path(temp_dir))
            catalog = self.load_catalog(root)
            catalog.pop("invariants")
            (root / "evals" / "contract-invariants.json").write_text(
                json.dumps(catalog, indent=2) + "\n",
                encoding="utf-8",
            )

            errors = self.validator.validate_contract_consistency(root)

            self.assertTrue(any("catalog invariants must be a" in error for error in errors), errors)

    def test_empty_invariants_list_is_rejected(self):
        with tempfile.TemporaryDirectory(dir=BUNDLE_ROOT.parent) as temp_dir:
            root = self.copy_bundle(Path(temp_dir))
            catalog = self.load_catalog(root)
            catalog["invariants"] = []
            (root / "evals" / "contract-invariants.json").write_text(
                json.dumps(catalog, indent=2) + "\n",
                encoding="utf-8",
            )

            errors = self.validator.validate_contract_consistency(root)

            self.assertTrue(any("catalog invariants must be a non-empty list" in error for error in errors), errors)

    def test_missing_catalog_path_returns_error(self):
        missing_path = BUNDLE_ROOT / "evals" / "missing-contract-invariants.json"
        errors = self.validator.validate_contract_consistency(BUNDLE_ROOT, missing_path)
        self.assertTrue(any("missing catalog:" in error for error in errors), errors)

    def test_malformed_json_catalog_returns_error(self):
        with tempfile.TemporaryDirectory(dir=BUNDLE_ROOT.parent) as temp_dir:
            root = self.copy_bundle(Path(temp_dir))
            catalog_path = root / "evals" / "contract-invariants.json"
            catalog_path.write_text("{\n", encoding="utf-8")

            errors = self.validator.validate_contract_consistency(root)

            self.assertTrue(any("invalid catalog json" in error for error in errors), errors)

    def test_malformed_top_level_catalog_is_reported_without_crashing(self):
        with tempfile.TemporaryDirectory(dir=BUNDLE_ROOT.parent) as temp_dir:
            root = self.copy_bundle(Path(temp_dir))
            (root / "evals" / "contract-invariants.json").write_text("[1, 2, 3]\n", encoding="utf-8")

            errors = self.validator.validate_contract_consistency(root)

            self.assertTrue(
                any("catalog top-level value must be an object" in error for error in errors),
                errors,
            )

    def test_mixed_case_match_still_passes(self):
        with tempfile.TemporaryDirectory(dir=BUNDLE_ROOT.parent) as temp_dir:
            root = self.copy_bundle(Path(temp_dir))
            flow_path = root / "core" / "flow.md"
            flow_path.write_text(
                flow_path.read_text(encoding="utf-8").replace(
                    "minimum rollback scope", "MiNiMuM RoLlBaCk ScOpE", 1
                ),
                encoding="utf-8",
            )

            self.assertEqual([], self.validator.validate_contract_consistency(root))


if __name__ == "__main__":
    unittest.main()