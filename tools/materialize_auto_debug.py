#!/usr/bin/env python3
"""Hydrate the frozen DATA-333 database for the supplied Auto Debug snapshot.

The canonical database is stored losslessly in materialized_payload/xzchunk_*.
Transport chunks may contain wrapping or redundant trailing base64 padding. Each
chunk is normalized, decoded independently, binary-concatenated, and the final
payload must match PAYLOAD_SHA256 before extraction.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import shutil
import tarfile
import tempfile
import zipfile
from pathlib import Path

PAYLOAD_SHA256 = "0a69de4fd158bc52645a28ba017056abe29462d3494f5707b6b4006992080149"
EXPECTED_DATASET_FILES = 38
EXPECTED_SOURCE_SHA256 = {
    "Auto_ThanLong_Kteam_0789998118.exe": "e1e4f555da3d4891ab0db674ee345bad67c2414632b7d1684151e7a9243134aa",
    "Auto_ThanLong_obfusca.exe": "e2ba163c86852e81e60fe6c4694e031a2a7bf1b8838ddef799135736ad764e11",
    "Auto_ThanLong_Kteam_0789998118.pdb": "5795d8e41d2504d732919dfd74d135a364ec6fc7cbbc47cdfd71021b2780ad84",
    "KAutoHelper.dll": "55fb7f522ab98227c0c6e00009c8090bc99e6a84ebe1d79427d930fd7900ae05",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def verify_source(source: Path) -> None:
    found: dict[str, str] = {}
    if source.is_dir():
        for name in EXPECTED_SOURCE_SHA256:
            matches = list(source.rglob(name))
            if not matches:
                raise SystemExit(f"Frozen source verification failed: missing {name}")
            found[name] = sha256_file(matches[0])
    elif source.is_file() and source.suffix.lower() == ".zip":
        with zipfile.ZipFile(source) as zf:
            by_basename = {Path(n).name: n for n in zf.namelist() if not n.endswith("/")}
            for name in EXPECTED_SOURCE_SHA256:
                member = by_basename.get(name)
                if not member:
                    raise SystemExit(f"Frozen source verification failed: missing {name} in ZIP")
                found[name] = sha256_bytes(zf.read(member))
    else:
        raise SystemExit(f"Unsupported source: {source}")

    bad = {
        name: {"expected": expected, "actual": found.get(name, "")}
        for name, expected in EXPECTED_SOURCE_SHA256.items()
        if found.get(name) != expected
    }
    if bad:
        raise SystemExit(
            "Frozen source hash mismatch. Refusing to apply DATA-333 from another build:\n"
            + json.dumps(bad, indent=2)
        )
    print("Frozen source fingerprints verified.")


def decode_chunk(path: Path) -> bytes:
    encoded = b"".join(path.read_bytes().split())
    core = encoded.rstrip(b"=")
    normalized = core + (b"=" * ((-len(core)) % 4))
    try:
        return base64.b64decode(normalized, validate=True)
    except Exception as exc:
        raise SystemExit(f"Canonical payload chunk {path.name} is invalid base64: {exc}") from exc


def read_payload(repo: Path) -> bytes:
    chunks = sorted((repo / "materialized_payload").glob("xzchunk_*"))
    if not chunks:
        raise SystemExit("No materialized_payload/xzchunk_* files found")
    payload = b"".join(decode_chunk(chunk) for chunk in chunks)
    actual = sha256_bytes(payload)
    if actual != PAYLOAD_SHA256:
        raise SystemExit(f"Canonical payload SHA-256 mismatch: {actual} != {PAYLOAD_SHA256}")
    print(f"Canonical payload verified from {len(chunks)} encoded chunks.")
    return payload


def hydrate(repo: Path, payload: bytes) -> None:
    database = repo / "database"
    with tempfile.TemporaryDirectory(prefix="data333_payload_") as td:
        archive = Path(td) / "database.tar.xz"
        archive.write_bytes(payload)
        with tarfile.open(archive, "r:xz") as tf:
            members = tf.getmembers()
            for member in members:
                parts = Path(member.name).parts
                if not parts or parts[0] != "database" or ".." in parts:
                    raise SystemExit(f"Unsafe/unexpected payload member: {member.name}")
            staged = Path(td) / "extract"
            staged.mkdir()
            tf.extractall(staged, filter="data")
        staged_db = staged / "database"
        files = [p for p in staged_db.rglob("*") if p.is_file()]
        if len(files) != EXPECTED_DATASET_FILES:
            raise SystemExit(f"Expected {EXPECTED_DATASET_FILES} canonical dataset files, got {len(files)}")
        for src in files:
            rel = src.relative_to(staged_db)
            dst = database / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    print(f"Hydrated {EXPECTED_DATASET_FILES} canonical DATA-333 dataset files.")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--source", help="Frozen Debug directory or ZIP; verified before hydration")
    ap.add_argument("--payload-only", action="store_true", help="Hydrate canonical payload without local source copy")
    args = ap.parse_args()
    repo = Path(args.repo_root).resolve()
    if args.source:
        verify_source(Path(args.source).resolve())
    elif not args.payload_only:
        raise SystemExit("Pass --source <Debug dir/zip> or --payload-only")
    hydrate(repo, read_payload(repo))


if __name__ == "__main__":
    main()
