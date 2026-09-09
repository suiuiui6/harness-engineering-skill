import json
import subprocess
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "integrations.json").read_text(encoding="utf-8"))
    errors = []
    if not (root / "SKILL.md").is_file():
        errors.append("Harness entry SKILL.md is missing")
    entries = [*manifest.get("companions", []), *manifest.get("integration_consumers", [])]
    for entry in entries:
        result = subprocess.run(
            ["git", "ls-remote", entry["repository"] + ".git", f"refs/heads/{entry['ref']}"],
            capture_output=True,
            text=True,
            check=False,
        )
        observed = result.stdout.split()[0] if result.returncode == 0 and result.stdout.split() else ""
        if not observed:
            errors.append(f"unreachable integration: {entry['name']}")
        tested = entry.get("tested_commit")
        if tested and observed != tested:
            errors.append(
                f"integration drift for {entry['name']}: expected {tested}, observed {observed}"
            )
    if errors:
        print("\n".join(errors))
        return 1
    print(f"PASS: {len(entries)} Harness integrations reachable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
