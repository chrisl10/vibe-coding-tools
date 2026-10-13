#!/usr/bin/env python3
"""Detect the ecosystems (stacks) in a repository for an Audit My Code run.

Walks a repository without following symlinks, skips dependency and build
folders, reads manifest files, and prints JSON. The `stacks` array matches the
`intake.json.stacks` shape of the Audit My Code contract (section 4):

    [{"id": "nextjs", "version": "15.5.2", "paths": ["apps/web"]}, ...]

Stack ids: node-server, python, go, rust, ruby, php, java-kotlin, dotnet,
react, nextjs, svelte, sveltekit, other.

Standard library only (Python 3.9 or newer; uses tomllib on 3.11 or newer and
a regex fallback otherwise). Read-only: never writes into the scanned repo.

Usage:
    python3 detect_ecosystems.py [ROOT] [--exclude DIR ...] [--stacks-only]
                                 [--compact] [--max-file-bytes N]

Exit codes: 0 success, 2 bad arguments or unreadable root.

Designed and built by Legion Code Inc. Licensed under AGPL-3.0-or-later.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath

try:  # Python 3.11+
    import tomllib  # type: ignore[import-not-found]
except ModuleNotFoundError:  # pragma: no cover - exercised only on old Pythons
    tomllib = None  # type: ignore[assignment]

SCHEMA_VERSION = "1.0"

DEFAULT_SKIP_DIRS = {
    # required by the contract brief
    "node_modules", "vendor", ".git", "dist", "build", "target",
    # common dependency, cache, and generated folders
    ".hg", ".svn", ".venv", "venv", "__pycache__", ".tox", ".nox",
    ".mypy_cache", ".pytest_cache", ".ruff_cache", ".next", ".nuxt",
    ".svelte-kit", ".turbo", ".parcel-cache", ".cache", "coverage",
    ".terraform", ".gradle", ".idea", ".vscode", "Pods", "bower_components",
    "obj", ".dart_tool", ".expo", "out", ".output", ".vercel", ".serverless",
}

STACK_ORDER = [
    "nextjs", "react", "sveltekit", "svelte", "node-server", "python", "go",
    "rust", "ruby", "php", "java-kotlin", "dotnet", "other",
]

# Contract section 2 routing. The orchestrator decides; this is a hint.
ROUTING = {
    "nextjs": ["nextjs-security-wasp-drone", "react-security-wasp-drone"],
    "react": ["react-security-wasp-drone"],
    "svelte": ["sveltekit-security-wasp-drone"],
    "sveltekit": ["sveltekit-security-wasp-drone"],
}
POLYGLOT_IDS = {"node-server", "python", "go", "rust", "ruby", "php",
                "java-kotlin", "dotnet", "other"}

NODE_SERVER_FRAMEWORKS = {
    "express": "express", "fastify": "fastify", "@nestjs/core": "nestjs",
    "hono": "hono", "koa": "koa", "@hapi/hapi": "hapi", "restify": "restify",
    "@adonisjs/core": "adonisjs", "elysia": "elysia", "@trpc/server": "trpc",
    "apollo-server": "apollo-server", "@apollo/server": "apollo-server",
    "graphql-yoga": "graphql-yoga", "sails": "sails", "loopback": "loopback",
    "@loopback/core": "loopback", "@feathersjs/feathers": "feathers",
    "socket.io": "socket.io", "ws": "ws", "micro": "micro", "h3": "h3",
    "polka": "polka", "@remix-run/node": "remix", "@remix-run/express": "remix",
}
NODE_SERVER_HINT_DEPS = {
    "pg", "mysql", "mysql2", "mongoose", "mongodb", "prisma", "@prisma/client",
    "sequelize", "typeorm", "knex", "drizzle-orm", "redis", "ioredis",
    "bullmq", "jsonwebtoken", "passport", "bcrypt", "bcryptjs", "dotenv",
    "nodemailer", "aws-sdk", "@aws-sdk/client-s3", "stripe", "better-sqlite3",
}
FRONTEND_ONLY_DEPS = {
    "vue", "nuxt", "@angular/core", "solid-js", "preact", "astro", "@remix-run/react",
    "gatsby", "vite", "@vitejs/plugin-react", "react-dom", "react-native", "expo",
}

PY_FRAMEWORKS = {
    "django": "django", "djangorestframework": "django-rest-framework",
    "django-ninja": "django-ninja", "fastapi": "fastapi", "flask": "flask",
    "starlette": "starlette", "litestar": "litestar", "sanic": "sanic",
    "tornado": "tornado", "aiohttp": "aiohttp", "pyramid": "pyramid",
    "bottle": "bottle", "falcon": "falcon", "quart": "quart", "celery": "celery",
    "sqlalchemy": "sqlalchemy", "pydantic": "pydantic", "jinja2": "jinja2",
}
GO_FRAMEWORKS = {
    "github.com/gin-gonic/gin": "gin", "github.com/labstack/echo": "echo",
    "github.com/gofiber/fiber": "fiber", "github.com/go-chi/chi": "chi",
    "github.com/gorilla/mux": "gorilla-mux", "github.com/beego/beego": "beego",
    "github.com/valyala/fasthttp": "fasthttp", "google.golang.org/grpc": "grpc",
    "gorm.io/gorm": "gorm", "github.com/jmoiron/sqlx": "sqlx",
}
RUST_FRAMEWORKS = {
    "axum": "axum", "actix-web": "actix-web", "rocket": "rocket", "warp": "warp",
    "poem": "poem", "salvo": "salvo", "tide": "tide", "tonic": "tonic",
    "sqlx": "sqlx", "diesel": "diesel", "sea-orm": "sea-orm", "tokio": "tokio",
    "tower-http": "tower-http",
}
RUBY_FRAMEWORKS = {
    "rails": "rails", "sinatra": "sinatra", "hanami": "hanami", "grape": "grape",
    "roda": "roda", "devise": "devise", "pundit": "pundit", "cancancan": "cancancan",
}
PHP_FRAMEWORKS = {
    "laravel/framework": "laravel", "laravel/lumen-framework": "lumen",
    "symfony/framework-bundle": "symfony", "symfony/http-kernel": "symfony",
    "slim/slim": "slim", "cakephp/cakephp": "cakephp", "yiisoft/yii2": "yii2",
    "codeigniter4/framework": "codeigniter", "laminas/laminas-mvc": "laminas",
    "drupal/core": "drupal", "johnpbloch/wordpress": "wordpress",
    "roots/wordpress": "wordpress", "twig/twig": "twig",
}
JVM_FRAMEWORKS = {
    "org.springframework.boot": "spring-boot", "spring-boot-starter": "spring-boot",
    "io.quarkus": "quarkus", "io.micronaut": "micronaut", "io.ktor": "ktor",
    "io.vertx": "vertx", "io.dropwizard": "dropwizard", "io.javalin": "javalin",
    "org.springframework.security": "spring-security",
    "spring-boot-starter-security": "spring-security",
}
DOTNET_PACKAGES = {
    "Microsoft.AspNetCore": "aspnetcore", "Microsoft.EntityFrameworkCore": "efcore",
    "Newtonsoft.Json": "newtonsoft-json", "Dapper": "dapper",
    "Microsoft.Identity.Web": "microsoft-identity-web",
}
OTHER_MANIFESTS = {
    "mix.exs": "elixir", "pubspec.yaml": "dart", "Package.swift": "swift",
    "CMakeLists.txt": "c-cpp", "meson.build": "c-cpp", "build.zig": "zig",
    "stack.yaml": "haskell", "dune-project": "ocaml", "Project.toml": "julia",
    "DESCRIPTION": "r", "cpanfile": "perl", "build.sbt": "scala",
    "deps.edn": "clojure", "project.clj": "clojure",
}
EXT_LANG = {
    ".ts": "TypeScript", ".tsx": "TypeScript", ".mts": "TypeScript", ".cts": "TypeScript",
    ".js": "JavaScript", ".jsx": "JavaScript", ".mjs": "JavaScript", ".cjs": "JavaScript",
    ".svelte": "Svelte", ".vue": "Vue", ".py": "Python", ".go": "Go", ".rs": "Rust",
    ".rb": "Ruby", ".erb": "Ruby", ".php": "PHP", ".java": "Java", ".kt": "Kotlin",
    ".kts": "Kotlin", ".scala": "Scala", ".groovy": "Groovy", ".cs": "C#",
    ".fs": "F#", ".vb": "Visual Basic", ".cshtml": "C#", ".razor": "C#",
    ".swift": "Swift", ".m": "Objective-C", ".c": "C", ".h": "C", ".cc": "C++",
    ".cpp": "C++", ".hpp": "C++", ".ex": "Elixir", ".exs": "Elixir", ".dart": "Dart",
    ".sh": "Shell", ".bash": "Shell", ".ps1": "PowerShell", ".tf": "HCL",
    ".sql": "SQL", ".lua": "Lua", ".pl": "Perl", ".r": "R", ".zig": "Zig",
}
VERSION_TOKEN = re.compile(r"(\d+(?:\.\d+){0,3}(?:[-+][0-9A-Za-z.-]+)?)")


# ----------------------------------------------------------------- helpers

def rel(root: Path, p: Path) -> str:
    try:
        r = p.relative_to(root).as_posix()
    except ValueError:
        r = p.as_posix()
    return r or "."


def clean_version(spec):
    """Return the first concrete version token in a spec, or None."""
    if spec is None:
        return None
    s = str(spec).strip()
    if not s or s in {"*", "latest", "next", "workspace:*"}:
        return None
    s = s.split("||")[0]
    m = VERSION_TOKEN.search(s)
    return m.group(1) if m else None


class Reader:
    def __init__(self, max_bytes: int, warnings: list, root=None):
        self.max_bytes = max_bytes
        self.root = root
        self.warnings = warnings
        self._cache: dict = {}

    def text(self, path: Path):
        key = str(path)
        if key in self._cache:
            return self._cache[key]
        data = None
        try:
            if os.path.islink(path):
                self.warnings.append(f"skipped symlink: {path.name}")
            else:
                st = os.lstat(path)
                real = os.path.realpath(path)
                root_real = os.path.realpath(self.root) if self.root else ""
                if not stat.S_ISREG(st.st_mode):
                    self.warnings.append(f"skipped non-regular file: {path.name}")
                elif root_real and not (real == root_real or real.startswith(root_real + os.sep)):
                    self.warnings.append(f"skipped symlink: {path.name}")
                elif st.st_size > self.max_bytes:
                    self.warnings.append(f"skipped large file (over {self.max_bytes} bytes): {path.name}")
                else:
                    data = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            self.warnings.append(f"unreadable: {path.name}: {exc.__class__.__name__}")
        self._cache[key] = data
        return data

    def json(self, path: Path):
        t = self.text(path)
        if t is None:
            return None
        try:
            return json.loads(t)
        except json.JSONDecodeError:
            # tolerate package.json with comments or trailing commas poorly: give up loudly
            self.warnings.append(f"invalid JSON: {path}")
            return None

    def toml(self, path: Path):
        t = self.text(path)
        if t is None:
            return None
        if tomllib is not None:
            try:
                return tomllib.loads(t)
            except Exception:  # tomllib.TOMLDecodeError, keep stdlib-only and broad
                self.warnings.append(f"invalid TOML: {path}")
                return None
        return None


# ---------------------------------------------------------------- the walk

AGENT_DIRS = {".claude", ".cursor", ".codex", ".windsurf", ".worktrees"}


def _is_linked_worktree(path: str) -> bool:
    """True when `path` holds a .git FILE pointing into another repo's worktrees/.

    Submodules also use a .git file, but theirs points into .git/modules/, so
    they are still scanned.
    """
    gitfile = os.path.join(path, ".git")
    if not os.path.isfile(gitfile):
        return False
    try:
        with open(gitfile, encoding="utf-8", errors="replace") as fh:
            head = fh.read(4096)
    except OSError:
        return False
    return head.startswith("gitdir:") and "/worktrees/" in head.replace("\\", "/")


def walk(root: Path, skip: set, warnings: list, skipped_worktrees: list):
    """Yield (dirpath, dirnames, filenames) without following symlinks."""
    def onerror(err):
        warnings.append(f"walk error: {getattr(err, 'filename', '?')}: {err.__class__.__name__}")

    for dirpath, dirnames, filenames in os.walk(root, topdown=True, onerror=onerror, followlinks=False):
        kept = []
        here = os.path.basename(dirpath)
        for d in dirnames:
            if d in skip:
                continue
            full = os.path.join(dirpath, d)
            if os.path.islink(full):
                continue
            # agent and IDE worktree folders hold full copies of the repo
            if d == "worktrees" and here in AGENT_DIRS:
                skipped_worktrees.append(full)
                continue
            if _is_linked_worktree(full):
                skipped_worktrees.append(full)
                continue
            kept.append(d)
        dirnames[:] = sorted(kept)
        real_files = []
        for fn in filenames:
            if os.path.islink(os.path.join(dirpath, fn)):
                warnings.append(f"skipped symlink: {os.path.relpath(os.path.join(dirpath, fn), root)}")
                continue
            real_files.append(fn)
        yield Path(dirpath), dirnames, sorted(real_files)


# ------------------------------------------------------- lockfile lookups

def find_upwards(start: Path, root: Path, names):
    """Return the first file named in `names` in start or its ancestors, stopping at root."""
    cur = start
    while True:
        for n in names:
            cand = cur / n
            if cand.is_file():
                return cand
        if cur == root or cur.parent == cur:
            return None
        cur = cur.parent


def npm_resolved(reader: Reader, pkg_dir: Path, root: Path, name: str):
    lock = find_upwards(pkg_dir, root, ["package-lock.json", "npm-shrinkwrap.json", "pnpm-lock.yaml", "yarn.lock", "bun.lock"])
    if lock is None:
        return None, None
    src = rel(root, lock)
    if lock.name in {"package-lock.json", "npm-shrinkwrap.json"}:
        data = reader.json(lock) or {}
        pkgs = data.get("packages") or {}
        sub = rel(lock.parent, pkg_dir)
        for key in ([f"{sub}/node_modules/{name}"] if sub != "." else []) + [f"node_modules/{name}"]:
            v = (pkgs.get(key) or {}).get("version")
            if v:
                return v, src
        deps = data.get("dependencies") or {}
        v = (deps.get(name) or {}).get("version")
        return (v, src) if v else (None, None)
    text = reader.text(lock) or ""
    esc = re.escape(name)
    if lock.name == "pnpm-lock.yaml":
        m = re.search(r"^\s+'?/?" + esc + r"@(\d[^:()'\s]*)'?:", text, re.M)
        if m:
            return m.group(1), src
        return None, None
    if lock.name == "bun.lock":
        m = re.search(r'"' + esc + r'@(\d[^"]*)"', text)
        return (m.group(1), src) if m else (None, None)
    # yarn.lock (v1 and berry). Parsed line by line: a regex with nested lazy
    # quantifiers over indented lines is exponential on a crafted lockfile.
    header = re.compile(r'^"?' + esc + r'@[^\n]*:[ \t]*$')
    version = re.compile(r'^[ \t]+version:?[ \t]+"?([^"\s]+)"?')
    in_block = False
    for line in text.split("\n"):
        if in_block:
            if not line[:1] in (" ", "\t"):
                in_block = False  # block ended without a version line; re-check as a header
            else:
                m = version.match(line)
                if m:
                    return m.group(1), src
                continue
        if header.match(line):
            in_block = True
    return None, None


def py_lock_versions(reader: Reader, proj_dir: Path, root: Path):
    out = {}
    lock = find_upwards(proj_dir, root, ["uv.lock", "poetry.lock", "pdm.lock", "Pipfile.lock"])
    if lock is None:
        return out, None
    if lock.name == "Pipfile.lock":
        data = reader.json(lock) or {}
        for section in ("default", "develop"):
            for k, v in (data.get(section) or {}).items():
                ver = clean_version((v or {}).get("version"))
                if ver:
                    out.setdefault(k.lower(), ver)
        return out, rel(root, lock)
    text = reader.text(lock) or ""
    for m in re.finditer(r'\[\[package\]\]\s*\nname\s*=\s*"([^"]+)"\s*\nversion\s*=\s*"([^"]+)"', text):
        out.setdefault(m.group(1).lower(), m.group(2))
    return out, rel(root, lock)


# -------------------------------------------------------------- detectors

def entry(path: str, version=None, version_source=None):
    return {"path": path, "version": version, "version_source": version_source,
            "frameworks": [], "manifests": []}


def add_fw(e, name, spec=None, resolved=None, source=None):
    for f in e["frameworks"]:
        if f["name"] == name:
            if resolved and not f.get("version"):
                f["version"], f["source"] = resolved, source
            return
    e["frameworks"].append({"name": name, "version": resolved or clean_version(spec),
                            "spec": spec, "source": source if resolved else "manifest"})


def detect_node(reader, root, d: Path, pkg_path: Path, found):
    pkg = reader.json(pkg_path)
    if not isinstance(pkg, dict):
        return
    r = rel(root, d)
    deps = {}
    for section in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        sec = pkg.get(section)
        if isinstance(sec, dict):
            for k, v in sec.items():
                deps.setdefault(k, str(v))
    runtime_deps = pkg.get("dependencies") if isinstance(pkg.get("dependencies"), dict) else {}
    manifest = rel(root, pkg_path)

    def fw(e, dep, name):
        resolved, src = npm_resolved(reader, d, root, dep)
        add_fw(e, name, deps.get(dep), resolved, src)
        return e["frameworks"][-1]["version"]

    has_next = "next" in deps
    has_kit = "@sveltejs/kit" in deps
    has_svelte = "svelte" in deps
    has_react = "react" in deps

    if has_next:
        e = entry(r)
        e["manifests"].append(manifest)
        e["version"] = fw(e, "next", "next")
        e["version_source"] = e["frameworks"][0]["source"]
        if has_react:
            fw(e, "react", "react")
        found["nextjs"].append(e)
    elif has_react and not has_kit:
        e = entry(r)
        e["manifests"].append(manifest)
        e["version"] = fw(e, "react", "react")
        e["version_source"] = e["frameworks"][0]["source"]
        for dep, name in (("react-native", "react-native"), ("expo", "expo"), ("vite", "vite"),
                          ("@remix-run/react", "remix"), ("react-router", "react-router"),
                          ("@tanstack/react-start", "tanstack-start"), ("gatsby", "gatsby")):
            if dep in deps:
                fw(e, dep, name)
        found["react"].append(e)

    if has_kit:
        e = entry(r)
        e["manifests"].append(manifest)
        e["version"] = fw(e, "@sveltejs/kit", "sveltekit")
        e["version_source"] = e["frameworks"][0]["source"]
        if has_svelte:
            fw(e, "svelte", "svelte")
        found["sveltekit"].append(e)
    elif has_svelte:
        e = entry(r)
        e["manifests"].append(manifest)
        e["version"] = fw(e, "svelte", "svelte")
        e["version_source"] = e["frameworks"][0]["source"]
        found["svelte"].append(e)

    server_hits = [(dep, name) for dep, name in NODE_SERVER_FRAMEWORKS.items() if dep in deps]
    frontend = has_next or has_kit or has_svelte or has_react or any(x in deps for x in FRONTEND_ONLY_DEPS)
    hint = any(x in runtime_deps for x in NODE_SERVER_HINT_DEPS)
    has_entry = any(k in pkg for k in ("main", "bin", "exports")) or "start" in (pkg.get("scripts") or {})
    is_workspace_root = bool(pkg.get("workspaces")) or (d / "pnpm-workspace.yaml").is_file()
    plain_node = (not frontend and not is_workspace_root and (bool(runtime_deps) or has_entry))
    if server_hits or (not frontend and hint) or plain_node:
        node_ver, src = None, None
        engines = pkg.get("engines") if isinstance(pkg.get("engines"), dict) else {}
        volta = pkg.get("volta") if isinstance(pkg.get("volta"), dict) else {}
        if engines.get("node"):
            node_ver, src = clean_version(engines["node"]), manifest + "#engines.node"
        elif volta.get("node"):
            node_ver, src = clean_version(volta["node"]), manifest + "#volta.node"
        else:
            f = find_upwards(d, root, [".nvmrc", ".node-version"])
            if f is not None:
                node_ver, src = clean_version((reader.text(f) or "").strip().lstrip("v")), rel(root, f)
        e = entry(r, node_ver, src)
        e["manifests"].append(manifest)
        e["runtime"] = "bun" if ("bun" in str(pkg.get("scripts", "")) or (d / "bun.lockb").is_file() or (d / "bun.lock").is_file()) else "node"
        for dep, name in server_hits:
            fw(e, dep, name)
        if not server_hits:
            e["note"] = ("no server framework dependency found; classified as Node code because it "
                         "has runtime dependencies or an entry point")
        found["node-server"].append(e)


def detect_deno(reader, root, d, f, found):
    e = entry(rel(root, d))
    e["manifests"].append(rel(root, f))
    e["runtime"] = "deno"
    text = reader.text(f) or ""
    for dep, name in (("hono", "hono"), ("oak", "oak"), ("fresh", "fresh")):
        if re.search(r"[\"'/@]" + dep + r"[@\"'/]", text):
            add_fw(e, name)
    found["node-server"].append(e)


PY_REQ_LINE = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)\s*(?:\[[^\]]*\])?\s*([<>=!~^].*)?$")


def parse_py_requirement(line: str):
    line = line.split("#", 1)[0].split(";", 1)[0].strip()
    if not line or line.startswith(("-", "git+", "http")):
        return None, None
    m = PY_REQ_LINE.match(line)
    if not m:
        return None, None
    name = m.group(1).lower().replace("_", "-")
    return name, (m.group(2) or "").strip() or None


def detect_python(reader, root, d: Path, files: set, found):
    r = rel(root, d)
    e = entry(r)
    reqs = {}
    py_ver, py_src = None, None
    for fn in sorted(files):
        p = d / fn
        if fn == "pyproject.toml":
            e["manifests"].append(rel(root, p))
            data = reader.toml(p)
            text = reader.text(p) or ""
            if data:
                proj = data.get("project") or {}
                for dep in proj.get("dependencies") or []:
                    n, s = parse_py_requirement(str(dep))
                    if n:
                        reqs.setdefault(n, s)
                for group in (proj.get("optional-dependencies") or {}).values():
                    for dep in group or []:
                        n, s = parse_py_requirement(str(dep))
                        if n:
                            reqs.setdefault(n, s)
                for group in (data.get("dependency-groups") or {}).values():
                    for dep in group or []:
                        if isinstance(dep, str):
                            n, s = parse_py_requirement(dep)
                            if n:
                                reqs.setdefault(n, s)
                poetry = ((data.get("tool") or {}).get("poetry") or {})
                for k, v in (poetry.get("dependencies") or {}).items():
                    spec = v if isinstance(v, str) else (v.get("version") if isinstance(v, dict) else None)
                    if k.lower() == "python":
                        py_ver, py_src = clean_version(spec), rel(root, p) + "#tool.poetry.dependencies.python"
                    else:
                        reqs.setdefault(k.lower().replace("_", "-"), spec)
                if proj.get("requires-python") and not py_ver:
                    py_ver, py_src = clean_version(proj["requires-python"]), rel(root, p) + "#project.requires-python"
            else:
                for m in re.finditer(r'"\s*([A-Za-z0-9][A-Za-z0-9._-]*)\s*(?:\[[^\]]*\])?\s*([<>=!~][^"]*)?"', text):
                    reqs.setdefault(m.group(1).lower().replace("_", "-"), (m.group(2) or None))
                m = re.search(r'requires-python\s*=\s*"([^"]+)"', text)
                if m and not py_ver:
                    py_ver, py_src = clean_version(m.group(1)), rel(root, p) + "#project.requires-python"
        elif re.match(r"^requirements.*\.(txt|in)$", fn) or fn in {"constraints.txt"}:
            e["manifests"].append(rel(root, p))
            for line in (reader.text(p) or "").splitlines():
                n, s = parse_py_requirement(line)
                if n:
                    reqs.setdefault(n, s)
        elif fn in {"setup.py", "setup.cfg", "Pipfile", "environment.yml"}:
            e["manifests"].append(rel(root, p))
            text = reader.text(p) or ""
            for name in PY_FRAMEWORKS:
                m = re.search(r"[\"'\s]" + re.escape(name) + r"\s*(?:\[[^\]]*\])?\s*([<>=!~]=?\s*[0-9][^\"'\s,]*)?", text, re.I)
                if m:
                    reqs.setdefault(name, m.group(1))
        elif fn == "manage.py":
            e["manifests"].append(rel(root, p))
            reqs.setdefault("django", None)
    if not py_ver:
        f = find_upwards(d, root, [".python-version"])
        if f is not None:
            py_ver, py_src = clean_version((reader.text(f) or "").strip()), rel(root, f)
    if not py_ver:
        rt = d / "runtime.txt"
        if rt.is_file():
            py_ver, py_src = clean_version(reader.text(rt)), rel(root, rt)
    e["version"], e["version_source"] = py_ver, py_src
    locked, lock_src = py_lock_versions(reader, d, root)
    for name, fwname in PY_FRAMEWORKS.items():
        if name in reqs:
            add_fw(e, fwname, reqs[name], locked.get(name), lock_src)
    found["python"].append(e)


def detect_go(reader, root, d, gomod: Path, found):
    text = reader.text(gomod) or ""
    e = entry(rel(root, d))
    e["manifests"].append(rel(root, gomod))
    m = re.search(r"^toolchain\s+go(\S+)", text, re.M) or re.search(r"^go\s+(\S+)", text, re.M)
    if m:
        e["version"], e["version_source"] = m.group(1), rel(root, gomod)
    m = re.search(r"^module\s+(\S+)", text, re.M)
    if m:
        e["module"] = m.group(1)
    for mod, name in GO_FRAMEWORKS.items():
        mm = re.search(r"^\s*(?:require\s+)?" + re.escape(mod) + r"(?:/v\d+)?\s+v(\S+)", text, re.M)
        if mm:
            add_fw(e, name, "v" + mm.group(1), mm.group(1), rel(root, gomod))
    found["go"].append(e)


def go_uses_net_http(reader, d: Path, limit=400):
    n = 0
    for dirpath, dirnames, filenames in os.walk(d):
        dirnames[:] = [x for x in dirnames if x not in DEFAULT_SKIP_DIRS]
        for fn in filenames:
            if fn.endswith(".go"):
                n += 1
                t = reader.text(Path(dirpath) / fn) or ""
                if '"net/http"' in t:
                    return True
                if n >= limit:
                    return False
    return False


def detect_rust(reader, root, d, cargo: Path, found):
    data = reader.toml(cargo)
    text = reader.text(cargo) or ""
    is_pkg = (data is not None and "package" in data) or (data is None and re.search(r"^\[package\]", text, re.M))
    if not is_pkg:
        return  # pure workspace root: members are detected on their own
    e = entry(rel(root, d))
    e["manifests"].append(rel(root, cargo))
    pkg = (data or {}).get("package") or {}
    rv = pkg.get("rust-version") if isinstance(pkg.get("rust-version"), str) else None
    if rv:
        e["version"], e["version_source"] = rv, rel(root, cargo) + "#package.rust-version"
    else:
        tc = find_upwards(d, root, ["rust-toolchain.toml", "rust-toolchain"])
        if tc is not None:
            m = re.search(r'channel\s*=\s*"([^"]+)"', reader.text(tc) or "") or re.search(r"^(\S+)", reader.text(tc) or "")
            if m:
                e["version"], e["version_source"] = m.group(1), rel(root, tc)
    deps = {}
    if data:
        for sec in ("dependencies", "dev-dependencies", "build-dependencies"):
            for k, v in (data.get(sec) or {}).items():
                deps[k] = v if isinstance(v, str) else (v.get("version") if isinstance(v, dict) else None)
    else:
        for m in re.finditer(r'^([A-Za-z0-9_-]+)\s*=\s*(?:"([^"]+)"|\{[^}]*version\s*=\s*"([^"]+)")', text, re.M):
            deps[m.group(1)] = m.group(2) or m.group(3)
    lock = find_upwards(d, root, ["Cargo.lock"])
    locked = {}
    if lock is not None:
        for m in re.finditer(r'\[\[package\]\]\s*\nname\s*=\s*"([^"]+)"\s*\nversion\s*=\s*"([^"]+)"', reader.text(lock) or ""):
            locked.setdefault(m.group(1), m.group(2))
    for crate, name in RUST_FRAMEWORKS.items():
        if crate in deps:
            add_fw(e, name, deps[crate], locked.get(crate), rel(root, lock) if lock else None)
    found["rust"].append(e)


def detect_ruby(reader, root, d, gemfile: Path, found):
    text = reader.text(gemfile) or ""
    e = entry(rel(root, d))
    e["manifests"].append(rel(root, gemfile))
    m = re.search(r"^\s*ruby\s+['\"]([^'\"]+)['\"]", text, re.M)
    if m:
        e["version"], e["version_source"] = clean_version(m.group(1)), rel(root, gemfile)
    else:
        f = find_upwards(d, root, [".ruby-version"])
        if f is not None:
            e["version"], e["version_source"] = clean_version(reader.text(f)), rel(root, f)
    lock = d / "Gemfile.lock"
    locked = {}
    if lock.is_file():
        e["manifests"].append(rel(root, lock))
        for mm in re.finditer(r"^    ([A-Za-z0-9_.-]+) \(([^)]+)\)$", reader.text(lock) or "", re.M):
            locked.setdefault(mm.group(1), mm.group(2))
    for gem, name in RUBY_FRAMEWORKS.items():
        mm = re.search(r"^\s*gem\s+['\"]" + re.escape(gem) + r"['\"](?:\s*,\s*['\"]([^'\"]+)['\"])?", text, re.M)
        if mm or gem in locked:
            add_fw(e, name, mm.group(1) if mm else None, locked.get(gem), rel(root, lock) if gem in locked else None)
    found["ruby"].append(e)


def detect_php(reader, root, d, composer: Path, found):
    data = reader.json(composer) or {}
    e = entry(rel(root, d))
    e["manifests"].append(rel(root, composer))
    req = {}
    for sec in ("require", "require-dev"):
        if isinstance(data.get(sec), dict):
            req.update({k.lower(): str(v) for k, v in data[sec].items()})
    if req.get("php"):
        e["version"], e["version_source"] = clean_version(req["php"]), rel(root, composer) + "#require.php"
    lock = d / "composer.lock"
    locked = {}
    if lock.is_file():
        ld = reader.json(lock) or {}
        for sec in ("packages", "packages-dev"):
            for p in ld.get(sec) or []:
                if isinstance(p, dict) and p.get("name"):
                    locked[p["name"].lower()] = str(p.get("version", "")).lstrip("v")
    for pkg, name in PHP_FRAMEWORKS.items():
        if pkg in req or pkg in locked:
            add_fw(e, name, req.get(pkg), locked.get(pkg), rel(root, lock) if pkg in locked else None)
    if not e["frameworks"]:
        e["frameworks"].append({"name": "plain-php", "version": None, "spec": None, "source": "no framework package"})
    found["php"].append(e)


def detect_jvm(reader, root, d, files: set, found):
    e = entry(rel(root, d))
    texts = []
    for fn in ("pom.xml", "build.gradle", "build.gradle.kts", "settings.gradle", "settings.gradle.kts", "gradle/libs.versions.toml"):
        p = d / fn
        if p.is_file():
            e["manifests"].append(rel(root, p))
            texts.append((fn, reader.text(p) or ""))
    joined = "\n".join(t for _, t in texts)
    jv = (re.search(r"<java\.version>\s*([0-9.]+)\s*<", joined)
          or re.search(r"<maven\.compiler\.(?:release|source)>\s*([0-9.]+)\s*<", joined)
          or re.search(r"<release>\s*([0-9.]+)\s*</release>", joined)
          or re.search(r"languageVersion(?:\.set)?\s*(?:=|\()\s*JavaLanguageVersion\.of\(\s*(\d+)", joined)
          or re.search(r"(?:source|target)Compatibility\s*=\s*(?:JavaVersion\.VERSION_)?['\"]?([0-9_.]+)", joined)
          or re.search(r"jvmToolchain\(\s*(\d+)", joined))
    if jv:
        e["version"], e["version_source"] = jv.group(1).replace("_", "."), e["manifests"][0]
    kotlin = bool(re.search(r"kotlin\(|org\.jetbrains\.kotlin|kotlin-stdlib", joined)) or any(fn.endswith(".kts") for fn, _ in texts)
    e["languages"] = ["Kotlin", "Java"] if kotlin else ["Java"]
    sb = (re.search(r"<artifactId>spring-boot-starter-parent</artifactId>\s*<version>([^<]+)</version>", joined)
          or re.search(r"id\s*\(?\s*['\"]org\.springframework\.boot['\"]\s*\)?\s*version\s*['\"]([^'\"]+)['\"]", joined)
          or re.search(r"org\.springframework\.boot:spring-boot-gradle-plugin:([0-9][^'\"\s)]*)", joined)
          or re.search(r"spring-?boot\s*=\s*['\"]([0-9][^'\"]*)['\"]", joined))
    for key, name in JVM_FRAMEWORKS.items():
        if key in joined:
            if name == "spring-boot":
                add_fw(e, name, sb.group(1) if sb else None, sb.group(1) if sb else None, e["manifests"][0] if sb else None)
            else:
                add_fw(e, name)
    found["java-kotlin"].append(e)


def detect_dotnet(reader, root, d, proj: Path, found):
    text = reader.text(proj) or ""
    e = entry(rel(root, d))
    e["manifests"].append(rel(root, proj))
    m = re.search(r"<TargetFrameworks?>\s*([^<]+)<", text)
    if m:
        tfm = m.group(1).split(";")[0].strip()
        mv = re.search(r"net(?:coreapp)?(\d+\.\d+)", tfm)
        e["version"], e["version_source"] = (mv.group(1) if mv else tfm), rel(root, proj)
        e["target_framework"] = m.group(1).strip()
    if re.search(r'Sdk="Microsoft\.NET\.Sdk\.(?:Web|Razor|BlazorWebAssembly)"', text):
        add_fw(e, "aspnetcore", None, e.get("version"), rel(root, proj) if e.get("version") else None)
    central = find_upwards(d, root, ["Directory.Packages.props"])
    central_text = reader.text(central) if central else ""
    for mm in re.finditer(r'<PackageReference\s+Include="([^"]+)"(?:\s+Version="([^"]+)")?', text):
        pkg, ver = mm.group(1), mm.group(2)
        if not ver and central_text:
            cv = re.search(r'<PackageVersion\s+Include="' + re.escape(pkg) + r'"\s+Version="([^"]+)"', central_text)
            ver = cv.group(1) if cv else None
        for prefix, name in DOTNET_PACKAGES.items():
            if pkg == prefix or pkg.startswith(prefix + "."):
                add_fw(e, name, ver, ver, rel(root, proj) if ver else None)
    found["dotnet"].append(e)


# --------------------------------------------------------------- assembly

def collapse(paths):
    """Drop paths nested inside another path of the same stack."""
    ordered = sorted(set(paths), key=lambda p: (p.count("/"), p))
    kept = []
    for p in ordered:
        if p == ".":
            return ["."]
        if any(PurePosixPath(p).is_relative_to(PurePosixPath(k)) for k in kept if k != "."):
            continue
        kept.append(p)
    return sorted(kept)


def pick_version(entries):
    vals = [e["version"] for e in entries if e.get("version")]
    if not vals:
        return None
    counts = Counter(vals)
    top = max(counts.values())
    # most common, ties broken by shallowest path order
    for e in sorted(entries, key=lambda x: (x["path"].count("/"), x["path"])):
        if e.get("version") and counts[e["version"]] == top:
            return e["version"]
    return vals[0]


def detect(root: Path, extra_skip, max_bytes: int):
    warnings: list = []
    reader = Reader(max_bytes, warnings, root)
    skip = set(DEFAULT_SKIP_DIRS) | set(extra_skip or [])
    found = defaultdict(list)
    infra = {"dockerfiles": [], "compose_files": [], "github_workflows": [], "gitlab_ci": [],
             "terraform_dirs": [], "helm_charts": [], "kubernetes_manifests": [], "env_files": []}
    lang_counts: Counter = Counter()
    php_dirs = set()
    composer_dirs = set()
    files_scanned = 0
    go_dirs = []

    skipped_worktrees: list = []
    for d, _dirnames, filenames in walk(root, skip, warnings, skipped_worktrees):
        files = set(filenames)
        files_scanned += len(filenames)
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext in EXT_LANG:
                lang_counts[EXT_LANG[ext]] += 1
            if ext == ".php":
                php_dirs.add(d)
            low = fn.lower()
            if low == "dockerfile" or low.startswith("dockerfile.") or low.endswith(".dockerfile") or low == "containerfile":
                infra["dockerfiles"].append(rel(root, d / fn))
            if re.match(r"^(docker-)?compose(\.[\w-]+)?\.ya?ml$", low):
                infra["compose_files"].append(rel(root, d / fn))
            if low == ".gitlab-ci.yml":
                infra["gitlab_ci"].append(rel(root, d / fn))
            if low.startswith(".env") and low not in {".env.example", ".env.sample", ".env.template", ".envrc"}:
                infra["env_files"].append(rel(root, d / fn))
        if d.name == "workflows" and d.parent.name == ".github":
            infra["github_workflows"] += [rel(root, d / f) for f in filenames if f.endswith((".yml", ".yaml"))]
        if any(f.endswith(".tf") for f in filenames):
            infra["terraform_dirs"].append(rel(root, d))
        if "Chart.yaml" in files:
            infra["helm_charts"].append(rel(root, d))
        for f in filenames:
            if f.endswith((".yaml", ".yml")) and d.name in {"k8s", "kubernetes", "manifests", "deploy"}:
                infra["kubernetes_manifests"].append(rel(root, d / f))

        if "package.json" in files:
            detect_node(reader, root, d, d / "package.json", found)
        for deno in ("deno.json", "deno.jsonc"):
            if deno in files and "package.json" not in files:
                detect_deno(reader, root, d, d / deno, found)
                break
        py_markers = {"pyproject.toml", "setup.py", "setup.cfg", "Pipfile", "manage.py", "environment.yml"}
        if files & py_markers or any(re.match(r"^requirements.*\.(txt|in)$", f) for f in files):
            if not (files == {"pyproject.toml"} and _pyproject_is_tool_only(reader, d / "pyproject.toml")):
                detect_python(reader, root, d, {f for f in files if f in py_markers or f.startswith("requirements") or f == "constraints.txt"}, found)
        if "go.mod" in files:
            detect_go(reader, root, d, d / "go.mod", found)
            go_dirs.append(d)
        if "Cargo.toml" in files:
            detect_rust(reader, root, d, d / "Cargo.toml", found)
        if "Gemfile" in files:
            detect_ruby(reader, root, d, d / "Gemfile", found)
        elif any(f.endswith(".gemspec") for f in files):
            gs = sorted(f for f in files if f.endswith(".gemspec"))[0]
            e = entry(rel(root, d))
            e["manifests"].append(rel(root, d / gs))
            found["ruby"].append(e)
        if "composer.json" in files:
            detect_php(reader, root, d, d / "composer.json", found)
            composer_dirs.add(d)
        if files & {"pom.xml", "build.gradle", "build.gradle.kts"}:
            detect_jvm(reader, root, d, files, found)
        for f in filenames:
            if f.endswith((".csproj", ".fsproj", ".vbproj")):
                detect_dotnet(reader, root, d, d / f, found)
        for f, lang in OTHER_MANIFESTS.items():
            if f in files:
                e = entry(rel(root, d))
                e["manifests"].append(rel(root, d / f))
                e["language"] = lang
                found["other"].append(e)

    # Go: note plain net/http when no framework is listed
    for e in found["go"]:
        if not any(f["name"] in {"gin", "echo", "fiber", "chi", "gorilla-mux", "beego", "fasthttp"} for f in e["frameworks"]):
            if go_uses_net_http(reader, root / e["path"] if e["path"] != "." else root):
                add_fw(e, "net/http")

    # Plain PHP files outside any composer project
    loose = []
    for pd in php_dirs:
        if any(pd == c or c in pd.parents for c in composer_dirs):
            continue
        loose.append(pd)
    if loose:
        tops = set()
        for pd in loose:
            rp = rel(root, pd)
            tops.add(rp.split("/")[0] if rp != "." else ".")
        for t in sorted(tops):
            e = entry(t)
            e["frameworks"].append({"name": "plain-php", "version": None, "spec": None, "source": ".php files without composer.json"})
            e["note"] = "PHP files found without a composer.json; version unknown"
            found["php"].append(e)

    # Elsewhere-unclaimed code: emit other when there are source files but no stack at all
    if not any(found.values()):
        code_langs = [l for l in lang_counts if l not in {"Shell", "PowerShell", "HCL", "SQL"}]
        if code_langs:
            e = entry(".")
            e["note"] = "source files found but no recognized manifest: " + ", ".join(sorted(code_langs))
            found["other"].append(e)

    stacks, details = [], {}
    for sid in STACK_ORDER:
        entries = found.get(sid) or []
        if not entries:
            continue
        uniq = {}
        for e in entries:
            key = e["path"]
            if key in uniq:  # merge, for example two .csproj in one folder
                uniq[key]["manifests"] += [m for m in e["manifests"] if m not in uniq[key]["manifests"]]
                for f in e["frameworks"]:
                    add_fw(uniq[key], f["name"], f.get("spec"), f.get("version") if f.get("source") not in (None, "manifest") else None, f.get("source"))
                if not uniq[key].get("version") and e.get("version"):
                    uniq[key]["version"], uniq[key]["version_source"] = e["version"], e["version_source"]
            else:
                uniq[key] = e
        entries = sorted(uniq.values(), key=lambda x: x["path"])
        details[sid] = entries
        stacks.append({"id": sid, "version": pick_version(entries), "paths": collapse([e["path"] for e in entries])})

    routing = defaultdict(list)
    poly = []
    for s in stacks:
        for drone in ROUTING.get(s["id"], []):
            for p in s["paths"]:
                if p not in routing[drone]:
                    routing[drone].append(p)
        if s["id"] in POLYGLOT_IDS:
            poly.append({"id": s["id"], "paths": s["paths"]})
    routing_out = {k: sorted(v) for k, v in routing.items()}
    if poly:
        routing_out["polyglot-security-wasp-drone"] = poly

    for k in infra:
        infra[k] = sorted(set(infra[k]))
    languages = [l for l, _ in lang_counts.most_common()]
    return {
        "tool": "detect_ecosystems.py",
        "schema": SCHEMA_VERSION,
        "root": str(root),
        "stacks": stacks,
        "languages": languages,
        "language_file_counts": dict(lang_counts.most_common()),
        "details": details,
        "routing": routing_out,
        "infra": infra,
        "coverage": {"files_scanned": files_scanned, "skipped_dir_names": sorted(skip),
                     "max_file_bytes": max_bytes,
                     "symlinks_skipped": len({w for w in warnings if w.startswith("skipped symlink:")}),
                     "skipped_worktrees": sorted(rel(root, Path(p)) for p in skipped_worktrees)},
        "warnings": sorted(set(warnings)),
    }


def _pyproject_is_tool_only(reader, p: Path) -> bool:
    """A pyproject.toml holding only tool config (for example ruff in a JS repo)."""
    data = reader.toml(p)
    text = reader.text(p) or ""
    if data is not None:
        return "project" not in data and "poetry" not in (data.get("tool") or {}) and "build-system" not in data
    return not re.search(r"^\[(project|tool\.poetry|build-system)\]", text, re.M)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Detect ecosystems in a repository and print JSON (Audit My Code intake.json stacks shape).")
    ap.add_argument("root", nargs="?", default=".", help="repository root (default: current directory)")
    ap.add_argument("--exclude", action="append", default=[], metavar="DIR",
                    help="extra directory name to skip (repeatable)")
    ap.add_argument("--stacks-only", action="store_true", help="print only the stacks array")
    ap.add_argument("--compact", action="store_true", help="single-line JSON")
    ap.add_argument("--max-file-bytes", type=int, default=2_000_000,
                    help="skip reading manifest or lock files larger than this (default 2000000)")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    if not root.is_dir():
        print(json.dumps({"error": f"not a directory: {args.root}"}), file=sys.stderr)
        return 2
    result = detect(root, args.exclude, args.max_file_bytes)
    out = result["stacks"] if args.stacks_only else result
    print(json.dumps(out, indent=None if args.compact else 2, sort_keys=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
