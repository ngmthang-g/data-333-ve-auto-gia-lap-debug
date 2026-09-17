#!/usr/bin/env python3
"""Hydrate the canonical DATA-333 database for the frozen Auto Debug snapshot.

This repository is a frozen knowledge base, like DATA-2222.  The semantic
materialization is stored losslessly in materialized_payload/xzchunk_*.
For a supplied Debug directory/ZIP, this script first verifies the important
source artifacts against the frozen snapshot and FAILS CLOSED on a mismatch;
it never silently applies old DATA-333 knowledge to a changed donor build.

The canonical payload is a base64-encoded tar.xz split only to make repository
transport/audit simple.  Hydration restores the normal browseable database/*
CSV/JSON files and verifies the payload hash and expected dataset count.
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

PAYLOAD_SHA256 = "d11f7d5ef265540cccf6bfc169b04a6314b664f931cd64dbe43e2af698a2eded"
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
    """Verify the frozen donor identity without copying secret/plaintext files."""
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


def read_payload(repo: Path) -> bytes:
    chunk_dir = repo / "materialized_payload"
    chunks = sorted(chunk_dir.glob("xzchunk_*"))
    if not chunks:
        raise SystemExit("No materialized_payload/xzchunk_* files found")
    encoded = b"".join(p.read_bytes().strip() for p in chunks)
    try:
        payload = base64.b64decode(encoded, validate=True)
    except Exception as exc:
        raise SystemExit(f"Canonical payload base64 is invalid: {exc}") from exc
    actual = sha256_bytes(payload)
    if actual != PAYLOAD_SHA256:
        raise SystemExit(f"Canonical payload SHA-256 mismatch: {actual} != {PAYLOAD_SHA256}")
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
            raise SystemExit(
                f"Expected {EXPECTED_DATASET_FILES} canonical dataset files, got {len(files)}"
            )
        # Preserve hand-written database documentation; replace only materialized
        # paths present in the payload.
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
    ap.add_argument(
        "--payload-only",
        action="store_true",
        help="Hydrate the already-verified canonical payload without a local source copy",
    )
    args = ap.parse_args()
    repo = Path(args.repo_root).resolve()
    if args.source:
        verify_source(Path(args.source).resolve())
    elif not args.payload_only:
        raise SystemExit("Pass --source <Debug dir/zip> or --payload-only")
    payload = read_payload(repo)
    hydrate(repo, payload)


if __name__ == "__main__":
    main()
