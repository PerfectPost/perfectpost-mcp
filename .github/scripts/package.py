#!/usr/bin/env python3
"""
Standalone skill packager.
Usage: python package.py <skill-dir> <output-dir>
Exits with code 1 on validation failure.
"""

import sys
import zipfile
import os
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: pyyaml is required. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ALLOWED_FRONTMATTER_KEYS = {
    "name", "description", "license", "allowed-tools", "metadata", "compatibility"
}
REQUIRED_FRONTMATTER_KEYS = {"name", "description"}

# Excluded everywhere (any directory level)
EXCLUDED_DIRS = {"__pycache__", "node_modules", ".git"}
EXCLUDED_FILES = {".DS_Store"}
EXCLUDED_EXTENSIONS = {".pyc"}

# Excluded at skill root only
EXCLUDED_ROOT_DIRS = {"evals"}


def parse_frontmatter(skill_md_path: Path) -> dict:
    content = skill_md_path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        raise ValueError("SKILL.md must start with YAML frontmatter (---)")
    parts = content.split("---", 2)
    if len(parts) < 3:
        raise ValueError("SKILL.md frontmatter is not properly closed with ---")
    return yaml.safe_load(parts[1]) or {}


def validate(frontmatter: dict) -> None:
    missing = REQUIRED_FRONTMATTER_KEYS - set(frontmatter.keys())
    if missing:
        raise ValueError(f"Missing required frontmatter keys: {', '.join(sorted(missing))}")

    unknown = set(frontmatter.keys()) - ALLOWED_FRONTMATTER_KEYS
    if unknown:
        raise ValueError(f"Unknown frontmatter keys: {', '.join(sorted(unknown))}")

    name = frontmatter["name"]
    if not isinstance(name, str) or not name.strip():
        raise ValueError("'name' must be a non-empty string")
    if len(name) > 64:
        raise ValueError(f"'name' exceeds 64 characters: {len(name)}")

    description = frontmatter["description"]
    if not isinstance(description, str) or not description.strip():
        raise ValueError("'description' must be a non-empty string")
    if len(description) > 1024:
        raise ValueError(f"'description' exceeds 1024 characters: {len(description)}")


def should_exclude(path: Path, skill_root: Path) -> bool:
    rel = path.relative_to(skill_root)
    parts = rel.parts

    # Check if any component is an excluded dir
    for part in parts[:-1]:  # directories in path
        if part in EXCLUDED_DIRS:
            return True

    if path.is_dir():
        dirname = path.name
        if dirname in EXCLUDED_DIRS:
            return True
        # Exclude evals/ only at skill root
        if dirname in EXCLUDED_ROOT_DIRS and len(parts) == 1:
            return True
    else:
        # Excluded file names
        if path.name in EXCLUDED_FILES:
            return True
        # Excluded extensions
        if path.suffix in EXCLUDED_EXTENSIONS:
            return True
        # Check parent dirs
        for part in parts[:-1]:
            if part in EXCLUDED_DIRS:
                return True
        # Exclude files inside root-excluded dirs
        if parts[0] in EXCLUDED_ROOT_DIRS:
            return True

    return False


def package_skill(skill_dir: Path, output_dir: Path) -> Path:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_dir}")

    frontmatter = parse_frontmatter(skill_md)
    validate(frontmatter)

    skill_name = frontmatter["name"]
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{skill_name}.skill"

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for item in sorted(skill_dir.rglob("*")):
            if should_exclude(item, skill_dir):
                continue
            if item.is_file():
                rel = item.relative_to(skill_dir)
                arcname = f"{skill_name}/{rel}"
                zf.write(item, arcname)

    return output_path


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <skill-dir> <output-dir>", file=sys.stderr)
        sys.exit(1)

    skill_dir = Path(sys.argv[1]).resolve()
    output_dir = Path(sys.argv[2]).resolve()

    try:
        output_path = package_skill(skill_dir, output_dir)
        print(f"Packaged: {output_path}")
    except (ValueError, FileNotFoundError) as e:
        print(f"Validation error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
