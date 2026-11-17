#!/usr/bin/env python3
"""kuy-init helper: detect the project state and install the .agents/ scaffold safely.

  kuy-init.py detect [--root DIR]
      Print JSON: greenfield/brownfield, stack, layout, legacy-convention files, graphify state.
  kuy-init.py install [--root DIR] [--source bundled|DIR] [--only meta|NN,NN] [--dry-run] [--local] [--no-ignore]
                      [--code-analysis auto|force|skip]
      Copy rule files from SOURCE into .agents/rules/, the helper scripts into .agents/scripts/,
      write the managed block of AGENTS.md, ignore .agents/ and AGENTS.md in git, then run the
      wikilink and code-index scripts. Never overwrites a file the user edited (hash manifest in
      .agents/.kuy-init.json) and never touches an existing file outside the managed block.
      Run it first with a DIR of rules you drafted (user standard or legacy rules), then with
      `--source bundled`, which only fills in rule files that are still missing.

Standard library only. Prints a JSON report.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
BUNDLED_RULES = SKILL / "assets" / "rules"
SCRIPTS = ["wikilinks.py", "code-index.py"]
META_RULES = ["08", "09", "11", "13", "14"]  # process rules that never conflict with a legacy stack or style
MANIFEST = ".kuy-init.json"
BLOCK_START, BLOCK_END = "<!-- kuy-init:start -->", "<!-- kuy-init:end -->"
IGNORE_LINES = [".agents/", "AGENTS.md"]
SKIP = {".git", "node_modules", "dist", "build", "out", "vendor", "target", "__pycache__", ".venv", "venv",
        ".agents", "graphify-out", "coverage", ".next", ".idea", ".vscode"}
SOURCE_EXT = {".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".vue", ".svelte", ".php", ".go", ".java", ".kt",
              ".rs", ".rb", ".cs", ".swift"}
LEGACY_FILES = [".editorconfig", ".prettierrc", ".prettierrc.json", ".prettierrc.js", "eslint.config.js",
                "eslint.config.mjs", ".eslintrc", ".eslintrc.json", ".eslintrc.js", "tsconfig.json", "tsconfig.app.json",
                "pyproject.toml", "setup.cfg", "tox.ini", ".flake8", "ruff.toml", "phpcs.xml", "pint.json",
                "phpunit.xml", ".golangci.yml", "rustfmt.toml", ".rubocop.yml", "CONTRIBUTING.md", "CLAUDE.md",
                "AGENTS.md", "README.md", "Makefile", "package.json", "composer.json", "go.mod", "Cargo.toml",
                "pom.xml", "build.gradle", "Gemfile", "vitest.config.ts", "jest.config.js", "pytest.ini", ".github/workflows"]
NODE_HINTS = {"react": "React", "vue": "Vue", "svelte": "Svelte", "next": "Next.js", "nuxt": "Nuxt", "vite": "Vite",
              "express": "Express", "@nestjs/core": "NestJS", "typescript": "TypeScript", "tailwindcss": "Tailwind CSS",
              "bootstrap": "Bootstrap", "vitest": "Vitest", "jest": "Jest", "eslint": "ESLint", "prettier": "Prettier",
              "@tanstack/react-query": "TanStack Query", "axios": "Axios", "zod": "Zod"}
PY_HINTS = {"django": "Django", "fastapi": "FastAPI", "flask": "Flask", "pytest": "pytest", "sqlalchemy": "SQLAlchemy",
            "ruff": "Ruff", "black": "Black", "pydantic": "Pydantic"}
PHP_HINTS = {"laravel/framework": "Laravel", "symfony/framework-bundle": "Symfony", "phpunit/phpunit": "PHPUnit",
             "laravel/pint": "Laravel Pint"}


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def git(root: Path, *args: str) -> str | None:
    try:
        proc = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=True)
        return proc.stdout
    except (OSError, subprocess.CalledProcessError):
        return None


def git_z(root: Path, *args: str) -> list[str] | None:
    """Run git with NUL-separated output; returns the entries, or None when git fails."""
    try:
        proc = subprocess.run(["git", "-C", str(root), *args], capture_output=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return None
    return [e.decode("utf-8", "surrogateescape") for e in proc.stdout.split(b"\0") if e]


def project_files(root: Path) -> list[str]:
    listed = git_z(root, "ls-files", "-z", "-co", "--exclude-standard")
    if listed is not None:
        names = listed
    else:
        names = [str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()]
    return [n for n in names if not set(Path(n).parts[:-1]) & SKIP]


def detect_stack(root: Path) -> list[str]:
    found: list[str] = []

    def add(label: str, source: str) -> None:
        line = f"{label} (from `{source}`)"
        if line not in found:
            found.append(line)

    pkg = root / "package.json"
    if pkg.is_file():
        try:
            data = json.loads(pkg.read_text(encoding="utf-8"))
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            add("Node.js / JavaScript", "package.json")
            for key, label in NODE_HINTS.items():
                if key in deps:
                    add(f"{label} {str(deps[key]).lstrip('^~')}", "package.json")
        except ValueError:
            add("Node.js", "package.json")
    for name in ("pyproject.toml", "requirements.txt", "Pipfile"):
        path = root / name
        if path.is_file():
            text = path.read_text(encoding="utf-8", errors="replace").lower()
            add("Python", name)
            for key, label in PY_HINTS.items():
                if re.search(rf"\b{re.escape(key)}\b", text):
                    add(label, name)
    comp = root / "composer.json"
    if comp.is_file():
        add("PHP", "composer.json")
        text = comp.read_text(encoding="utf-8", errors="replace")
        for key, label in PHP_HINTS.items():
            if key in text:
                add(label, "composer.json")
    for name, label in (("go.mod", "Go"), ("Cargo.toml", "Rust"), ("Gemfile", "Ruby"), ("pom.xml", "Java (Maven)"),
                        ("build.gradle", "Java/Kotlin (Gradle)")):
        if (root / name).is_file():
            add(label, name)
    return found


def detect(root: Path) -> dict:
    files = project_files(root)
    sources = [f for f in files if Path(f).suffix.lower() in SOURCE_EXT]
    commits = git(root, "rev-list", "--count", "HEAD")
    stack = detect_stack(root)
    brown = bool(sources or stack or (commits and commits.strip() not in ("", "0")))
    tops: dict[str, int] = {}
    for name in files:
        parts = Path(name).parts
        if len(parts) > 1:
            tops[parts[0]] = tops.get(parts[0], 0) + 1
    subjects = (git(root, "log", "-30", "--format=%s") or "").splitlines()
    conventional = sum(bool(re.match(r"^(feat|fix|docs|refactor|test|chore|perf|build|ci|style)(\(.+\))?!?:", s)) for s in subjects)
    graph_bin = subprocess.run(["which", "graphify"], capture_output=True, text=True).returncode == 0
    tracked = git_z(root, "ls-files", "-z", ".agents") or []
    return {
        "root": str(root),
        "mode": "brownfield" if brown else "greenfield",
        "stack": stack,
        "source_files": len(sources),
        "commits": int((commits or "0").strip() or 0),
        "top_dirs": dict(sorted(tops.items(), key=lambda kv: -kv[1])[:15]),
        "legacy_files_present": [f for f in LEGACY_FILES if (root / f).exists()],
        "commit_style": {"sampled": len(subjects), "conventional": conventional},
        "has_agents_md": (root / "AGENTS.md").is_file(),
        "has_agents_dir": (root / ".agents").is_dir(),
        "agents_tracked_in_git": len(tracked),
        "is_git_repo": git(root, "rev-parse", "--git-dir") is not None,
        "graphify_installed": graph_bin,
        "graphify_graph": (root / "graphify-out" / "graph.json").is_file(),
    }


def layout_text(info: dict) -> str:
    if not info["top_dirs"]:
        return "No source layout yet. Record the top-level folders here as the project grows."
    return "\n".join(f"- `{d}/`: {n} files" for d, n in info["top_dirs"].items())


def stack_text(info: dict) -> str:
    if info["stack"]:
        return "\n".join(f"- {s}" for s in info["stack"]) + "\n- Anything not listed here is not yet agreed: ask before adding it."
    return ("- Stack not decided yet. Record it here when chosen: language, framework, package manager, "
            "formatter/linter, test runner.")


def managed_block() -> str:
    return f"""{BLOCK_START}
## Project rules (kuy-init)

This project keeps its agent rules in `.agents/`. They are the reference for development; the user may edit them at any time.

- Read [[rules/00-rules|the rules index]] first, then only the rules that match the task. Rules 01-14 are binding for code-writing and review work.
- Find code through the generated symbol index before reading files: `grep -n -i "<name>" .agents/code-analysis/*.md` ([[code-analysis/INDEX|code-analysis index]]). If graphify is installed, prefer `graphify query "<question>"`.
- Every Markdown document under `.agents/` must be wikilinked from its folder hub ([[rules/14-wikilinks]]). After adding or moving documents run `python3 .agents/scripts/wikilinks.py`.
- After changing code run `python3 .agents/scripts/code-index.py` to refresh the symbol index.
- Search long logs with `grep`, never read them whole. When a rule must be broken, follow [[rules/09-exceptions-override]].
{BLOCK_END}
"""


class Installer:
    def __init__(self, root: Path, dry: bool):
        self.root, self.dry = root, dry
        self.agents = root / ".agents"
        mf = self.agents / MANIFEST
        try:
            self.manifest = json.loads(mf.read_text(encoding="utf-8")) if mf.is_file() else {}
        except ValueError:
            self.manifest = {}
        self.manifest.setdefault("files", {})
        self.report = {"created": [], "updated": [], "kept_user_edited": [], "unchanged": [], "notes": []}

    def inside_root(self, path: Path) -> bool:
        try:
            path.resolve().relative_to(self.root.resolve())
            return True
        except ValueError:
            return False

    def put(self, rel: str, content: str) -> None:
        path = self.agents / rel
        key = f".agents/{rel}"
        if not self.inside_root(path):
            self.report["notes"].append(f"{key} resolves outside the project (symlink?): skipped")
            return
        new_hash = sha(content)
        if not path.exists():
            self.report["created"].append(key)
        else:
            current = sha(path.read_text(encoding="utf-8", errors="replace"))
            if current == new_hash:
                self.manifest["files"][key] = new_hash
                self.report["unchanged"].append(key)
                return
            if self.manifest["files"].get(key) != current:
                self.report["kept_user_edited"].append(key)
                return
            self.report["updated"].append(key)
        self.manifest["files"][key] = new_hash
        if not self.dry:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    def agents_md(self) -> None:
        path = self.root / "AGENTS.md"
        if not self.inside_root(path):
            self.report["notes"].append("AGENTS.md resolves outside the project (symlink?): skipped")
            return
        if not path.exists():
            text = "# AGENTS.md\n\nOrchestrator for this project's agent rules and documents.\n\n" + managed_block()
            self.report["created"].append("AGENTS.md")
        else:
            with open(path, encoding="utf-8", newline="") as handle:
                old = handle.read()
            eol = "\r\n" if "\r\n" in old else "\n"
            block = managed_block().replace("\n", eol)
            start, end = old.find(BLOCK_START), old.find(BLOCK_END)
            if (start == -1) != (end == -1) or (start != -1 and end < start):
                self.report["notes"].append("AGENTS.md has damaged kuy-init markers: left untouched, fix or remove them and re-run")
                return
            if start != -1:
                text = old[:start] + block.rstrip(eol) + old[end + len(BLOCK_END):]
            else:
                text = old.rstrip("\r\n") + eol + eol + block
            if text == old:
                self.report["unchanged"].append("AGENTS.md")
                return
            self.report["updated"].append("AGENTS.md (managed block only)")
        if not self.dry:
            with open(path, "w", encoding="utf-8", newline="") as handle:
                handle.write(text)

    def ignore(self, local: bool, info: dict) -> None:
        if info["agents_tracked_in_git"]:
            self.report["notes"].append(f"git already tracks {info['agents_tracked_in_git']} file(s) under .agents/: left out of the ignore list")
            lines = [l for l in IGNORE_LINES if l != ".agents/"]
        else:
            lines = list(IGNORE_LINES)
        if (git(self.root, "ls-files", "AGENTS.md") or "").strip():
            lines = [l for l in lines if l != "AGENTS.md"]
            self.report["notes"].append("AGENTS.md is already tracked by git: not ignored")
        if local:
            target = git(self.root, "rev-parse", "--git-path", "info/exclude")
            if not target:
                self.report["notes"].append("--local needs a git repository: nothing ignored")
                return
            path = (self.root / target.strip()) if not Path(target.strip()).is_absolute() else Path(target.strip())
        else:
            path = self.root / ".gitignore"
        existing = ""
        if path.is_file():
            with open(path, encoding="utf-8", newline="") as handle:
                existing = handle.read()
        eol = "\r\n" if "\r\n" in existing else "\n"
        have = {l.strip() for l in existing.splitlines()}
        add = [l for l in lines if l not in have and l.rstrip("/") not in have]
        if not add:
            self.report["unchanged"].append(str(path.relative_to(self.root)) if path.is_relative_to(self.root) else str(path))
            return
        self.report["updated"].append(f"{path.name}: +{', '.join(add)}")
        if not self.dry:
            path.parent.mkdir(parents=True, exist_ok=True)
            sep = "" if not existing or existing.endswith("\n") else eol
            with open(path, "w", encoding="utf-8", newline="") as handle:
                handle.write(existing + sep + eol + "# agent rules (kuy-init)" + eol + eol.join(add) + eol)

    def save_manifest(self) -> None:
        if not self.dry:
            self.agents.mkdir(parents=True, exist_ok=True)
            (self.agents / MANIFEST).write_text(json.dumps(self.manifest, indent=1, sort_keys=True), encoding="utf-8")


def run_helpers(root: Path, mode: str, report: dict) -> None:
    scripts = root / ".agents" / "scripts"
    if mode != "skip":
        cmd = [sys.executable, str(scripts / "code-index.py")] + (["--force"] if mode == "force" else [])
        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=root)
        report["notes"].append("code-index: " + (proc.stdout.strip() or proc.stderr.strip()))
    proc = subprocess.run([sys.executable, str(scripts / "wikilinks.py")], capture_output=True, text=True, cwd=root)
    report["notes"].append("wikilinks: " + (f"{len(proc.stdout.split())} hub(s) written" if proc.returncode == 0 else proc.stderr.strip()))


def install(args) -> dict:
    root = Path(args.root).resolve()
    info = detect(root)
    inst = Installer(root, args.dry_run)
    source = BUNDLED_RULES if args.source == "bundled" else Path(args.source).resolve()
    if not source.is_dir():
        sys.exit(f"source folder not found: {source}")
    only = {n for n in (META_RULES if args.only == "meta" else args.only.split(",")) if n} if args.only else None
    for rule in sorted(source.glob("*.md")):
        if only and rule.name[:2] not in only:
            continue
        text = rule.read_text(encoding="utf-8")
        if args.source == "bundled":
            clash = [p for p in (inst.agents / "rules").glob("*.md") if p.name[:2] == rule.name[:2] and p.name != rule.name]
            if clash:
                continue  # a drafted rule with the same number already covers this topic
            text = text.replace("{{STACK}}", stack_text(info)).replace("{{LAYOUT}}", layout_text(info))
        inst.put(f"rules/{rule.name}", text)
    for name in SCRIPTS:
        inst.put(f"scripts/{name}", (SKILL / "scripts" / name).read_text(encoding="utf-8"))
    inst.agents_md()
    if not args.no_ignore:
        inst.ignore(args.local, info)
    inst.save_manifest()
    if not args.dry_run:
        mode = args.code_analysis
        run_helpers(root, mode, inst.report)
    inst.report["mode"] = info["mode"]
    return inst.report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("detect")
    d.add_argument("--root", default=".")
    i = sub.add_parser("install")
    i.add_argument("--root", default=".")
    i.add_argument("--source", default="bundled")
    i.add_argument("--only", default="", help="'meta' or comma-separated rule numbers, e.g. 08,09 (default: all)")
    i.add_argument("--dry-run", action="store_true")
    i.add_argument("--local", action="store_true")
    i.add_argument("--no-ignore", action="store_true")
    i.add_argument("--code-analysis", choices=["auto", "force", "skip"], default="auto")
    args = parser.parse_args()
    out = detect(Path(args.root).resolve()) if args.cmd == "detect" else install(args)
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
