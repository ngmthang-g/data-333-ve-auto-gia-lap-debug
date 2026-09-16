#!/usr/bin/env python3
"""Materialize safe DATA-333 indexes from a Debug directory or ZIP.

The generator intentionally does NOT copy plaintext file contents. It emits
hashes, file/image metadata, sensitive-text schemas, and identifier-like
binary/PDB strings suitable for static indexing.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import struct
import subprocess
import tempfile
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

SENSITIVE_NAMES = {
    "code.txt",
    "KEYTAB.txt",
    "TONGHOP_KEYTAB.txt",
    "TAIKHOAN_DANGNHAP_AUTO.txt",
    "(MEmu).txt",
}

IDENT_RE = re.compile(r"^[A-Za-z_<>][A-Za-z0-9_<>.`+\-]{3,100}$")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def png_size(path: Path) -> tuple[int | None, int | None]:
    try:
        with path.open("rb") as f:
            sig = f.read(24)
        if len(sig) >= 24 and sig[:8] == b"\x89PNG\r\n\x1a\n" and sig[12:16] == b"IHDR":
            return struct.unpack(">II", sig[16:24])
    except OSError:
        pass
    return None, None


def text_schema(path: Path) -> dict[str, object]:
    raw = path.read_text(errors="replace")
    lines = raw.splitlines()
    nonempty = [x for x in lines if x]
    pipe_counts = [len(x.split("|")) for x in nonempty if "|" in x]
    return {
        "path": path.as_posix(),
        "bytes": path.stat().st_size,
        "lines": len(lines),
        "nonempty_lines": len(nonempty),
        "pipe_field_counts": ",".join(map(str, sorted(set(pipe_counts)))) if pipe_counts else "",
        "max_line_length": max((len(x) for x in lines), default=0),
        "sha256": sha256(path),
    }


def run_strings(path: Path) -> set[str]:
    exe = shutil.which("strings")
    if not exe:
        return set()
    out: set[str] = set()
    for args in ([exe, "-n", "4", str(path)], [exe, "-el", "-n", "4", str(path)]):
        try:
            p = subprocess.run(args, check=False, capture_output=True, text=True, errors="ignore")
        except OSError:
            continue
        for line in p.stdout.splitlines():
            line = line.strip()
            if IDENT_RE.fullmatch(line):
                out.add(line)
    return out


def resolve_source(source: Path, tempdir: Path) -> Path:
    if source.is_dir():
        return source
    if source.is_file() and source.suffix.lower() == ".zip":
        with zipfile.ZipFile(source) as zf:
            zf.extractall(tempdir)
        candidates = [p for p in tempdir.rglob("Debug") if p.is_dir()]
        if candidates:
            return sorted(candidates, key=lambda p: len(p.parts))[0]
        return tempdir
    raise SystemExit(f"Unsupported source: {source}")


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, help="Debug directory or ZIP containing Debug/")
    ap.add_argument("--repo-root", default=".")
    args = ap.parse_args()

    source = Path(args.source).resolve()
    repo = Path(args.repo_root).resolve()
    out = repo / "database" / "generated"
    out.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="data333_") as td:
        root = resolve_source(source, Path(td))
        files = sorted(p for p in root.rglob("*") if p.is_file())

        manifest: list[dict[str, object]] = []
        images: list[dict[str, object]] = []
        schemas: list[dict[str, object]] = []
        ext_counts: Counter[str] = Counter()
        folder_counts: Counter[str] = Counter()
        folder_bytes: Counter[str] = Counter()

        for p in files:
            rel = p.relative_to(root).as_posix()
            ext = p.suffix.lower()
            top = Path(rel).parts[0] if len(Path(rel).parts) > 1 else "<root>"
            size = p.stat().st_size
            digest = sha256(p)
            ext_counts[ext or "<none>"] += 1
            folder_counts[top] += 1
            folder_bytes[top] += size
            manifest.append({
                "path": rel,
                "size": size,
                "extension": ext,
                "top_group": top,
                "sha256": digest,
                "sensitive_name": "yes" if p.name in SENSITIVE_NAMES else "no",
            })
            if ext == ".png":
                width, height = png_size(p)
                images.append({
                    "path": rel,
                    "folder": top,
                    "filename": p.name,
                    "width": width or "",
                    "height": height or "",
                    "size": size,
                    "sha256": digest,
                })
            if p.name in SENSITIVE_NAMES:
                s = text_schema(p)
                s["path"] = rel
                schemas.append(s)

        write_csv(
            out / "ARTIFACT_MANIFEST.csv",
            manifest,
            ["path", "size", "extension", "top_group", "sha256", "sensitive_name"],
        )
        write_csv(
            out / "IMAGE_TEMPLATE_CATALOG.csv",
            images,
            ["path", "folder", "filename", "width", "height", "size", "sha256"],
        )
        write_csv(
            out / "SENSITIVE_TEXT_SCHEMAS.csv",
            schemas,
            ["path", "bytes", "lines", "nonempty_lines", "pipe_field_counts", "max_line_length", "sha256"],
        )

        symbol_files = [
            p for p in files
            if p.suffix.lower() in {".pdb", ".exe", ".dll"}
            and p.name in {
                "Auto_ThanLong_Kteam_0789998118.pdb",
                "Auto_ThanLong_obfusca.exe",
                "KAutoHelper.dll",
            }
        ]
        symbols: dict[str, list[str]] = {}
        for p in symbol_files:
            symbols[p.name] = sorted(run_strings(p))
        (out / "IDENTIFIERS.json").write_text(
            json.dumps(symbols, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        summary = {
            "source_name": source.name,
            "debug_root": root.name,
            "file_count": len(files),
            "total_bytes": sum(p.stat().st_size for p in files),
            "extension_counts": dict(sorted(ext_counts.items())),
            "top_group_counts": dict(folder_counts.most_common()),
            "top_group_bytes": dict(folder_bytes.most_common()),
            "png_count": len(images),
            "sensitive_text_files_indexed_without_contents": len(schemas),
        }
        (out / "SNAPSHOT_SUMMARY.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
