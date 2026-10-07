import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
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
VALIDATOR_PATH = SCRIPT_DIR / "validate_harness_skill.py"
TEMP_ROOT = Path("C:/tmp")


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_harness_skill", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class HarnessSkillValidatorTests(unittest.TestCase):
    def setUp(self):
        self.validator = load_validator()

    def copy_bundle(self, destination: Path) -> Path:
        target = destination / "harness-engineering"
        shutil.copytree(
            BUNDLE_ROOT,
            target,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        return target

    def test_repository_bundle_passes_complete_validation(self):
        self.assertEqual([], self.validator.validate_bundle(BUNDLE_ROOT))

    def test_invalid_frontmatter_name_is_reported(self):
        with tempfile.TemporaryDirectory(dir=BUNDLE_ROOT.parent) as temp_dir:
            root = self.copy_bundle(Path(temp_dir))
            skill = root / "SKILL.md"
            skill.write_text(
                skill.read_text(encoding="utf-8").replace(
                    "name: harness-engineering", "name: wrong-name", 1
                ),
                encoding="utf-8",
            )

            errors = self.validator.validate_bundle(root)

            self.assertTrue(
                any("frontmatter name must be harness-engineering" in error for error in errors),
                errors,
            )

    def test_broken_skill_resource_link_is_reported(self):
        with tempfile.TemporaryDirectory(dir=BUNDLE_ROOT.parent) as temp_dir:
            root = self.copy_bundle(Path(temp_dir))
            skill = root / "SKILL.md"
            skill.write_text(
                skill.read_text(encoding="utf-8")
                + "\n- Read `references/missing-resource.md` for this branch.\n",
                encoding="utf-8",
            )

            errors = self.validator.validate_bundle(root)

            self.assertTrue(
                any("missing linked resource" in error for error in errors),
                errors,
            )

    def test_generated_python_cache_is_reported(self):
        with tempfile.TemporaryDirectory(dir=BUNDLE_ROOT.parent) as temp_dir:
            root = self.copy_bundle(Path(temp_dir))
            cache = root / "scripts" / "__pycache__" / "generated.pyc"
            cache.parent.mkdir(parents=True)
            cache.write_bytes(b"generated")

            errors = self.validator.validate_bundle(root)

            self.assertTrue(
                any("generated cache artifact" in error for error in errors),
                errors,
            )

    def test_public_validator_reports_contract_drift(self):
        with tempfile.TemporaryDirectory(dir=BUNDLE_ROOT.parent) as temp_dir:
            root = self.copy_bundle(Path(temp_dir))
            contract = root / "references" / "output-contract.md"
            contract.write_text(
                contract.read_text(encoding="utf-8").replace(
                    "scope_result", "scope-outcome"
                ),
                encoding="utf-8",
            )

            errors = self.validator.validate_bundle(root)

            self.assertTrue(
                any("closure-fields" in error for error in errors),
                errors,
            )

    def test_validator_cli_does_not_generate_python_cache(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temp_dir:
            root = self.copy_bundle(Path(temp_dir))
            result = subprocess.run(
                [sys.executable, str(root / "scripts" / "validate_harness_skill.py"), str(root)],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertFalse((root / "scripts" / "__pycache__").exists())

    def test_plain_unittest_discover_does_not_generate_python_cache(self):
        if os.environ.get("HARNESS_SKIP_NESTED_DISCOVER") == "1":
            self.skipTest("avoid recursive nested unittest discovery")

        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temp_dir:
            root = self.copy_bundle(Path(temp_dir))
            env = dict(os.environ)
            env["HARNESS_SKIP_NESTED_DISCOVER"] = "1"
            result = subprocess.run(
                [sys.executable, "-m", "unittest", "discover", "-p", "test_*.py", "-v"],
                cwd=root / "scripts",
                capture_output=True,
                text=True,
                check=False,
                env=env,
            )

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertFalse((root / "scripts" / "__pycache__").exists())


if __name__ == "__main__":
    unittest.main()
