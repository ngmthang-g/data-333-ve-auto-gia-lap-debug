#!/usr/bin/env python3
"""Validate the frozen DATA-333 database and, optionally, its donor snapshot.

DATA-333 uses the committed machine-readable `database/` tree as the canonical
surface. The materialization manifest pins generated file paths, byte sizes and
row counts. Curated join/index tables are validated separately. If --source is
provided, four high-value donor binaries are SHA-256 verified before the data is
accepted for that snapshot.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import zipfile
from pathlib import Path

EXPECTED_SOURCE_SHA256 = {
    "Auto_ThanLong_Kteam_0789998118.exe": "e1e4f555da3d4891ab0db674ee345bad67c2414632b7d1684151e7a9243134aa",
    "Auto_ThanLong_obfusca.exe": "e2ba163c86852e81e60fe6c4694e031a2a7bf1b8838ddef799135736ad764e11",
    "Auto_ThanLong_Kteam_0789998118.pdb": "5795d8e41d2504d732919dfd74d135a364ec6fc7cbbc47cdfd71021b2780ad84",
    "KAutoHelper.dll": "55fb7f522ab98227c0c6e00009c8090bc99e6a84ebe1d79427d930fd7900ae05",
}

REQUIRED_CURATED = {
    "database/features/CORE_METHOD_RVA_INDEX.csv",
    "database/dotnet/DEVICE_STATE_CATALOG.csv",
    "database/control/CONTROL_CALL_CHAINS.csv",
    "database/features/ACTIVITY_EVIDENCE_MATRIX.csv",
    "database/features/FEATURE_STATE_JOIN.csv",
    "database/assets/ASSET_ROLE_CATALOG.csv",
    "database/TOOL_DATA_INDEX.md",
    "database/SUBSYSTEM_SOURCE_MAP.md",
    "database/SEMANTIC_JOIN_MAP.md",
    "research/AUTO_RUNTIME_PROOF_QUEUE.md",
    "analysis/07_FEATURE_STATE_AND_PROTECTED_BODY_MAP.md",
    "analysis/08_VISUAL_ASSET_SEMANTICS.md",
}

EXPECTED_SUMMARY = {
    "file_count": 1450,
    "total_bytes": 146978306,
    "png_count": 1393,
    "png_unique_sha256": 1180,
    "png_duplicate_groups": 178,
    "png_duplicate_extra_files": 213,
    "pdb_identifier_count": 783,
    "main_type_count": 57,
    "main_method_count": 1070,
    "main_field_count": 429,
    "helper_type_count": 40,
    "helper_method_count": 224,
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
            "Frozen source hash mismatch. Refusing to apply DATA-333 to another build:\n"
            + json.dumps(bad, indent=2)
        )
    print("Frozen source fingerprints verified.")


def count_rows(path: Path) -> int:
    if path.suffix.lower() == ".jsonl":
        return sum(1 for line in path.open("r", encoding="utf-8-sig") if line.strip())
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            return max(sum(1 for _ in csv.reader(f)) - 1, 0)
    raise ValueError(f"row counting unsupported for {path}")


def validate_database(repo: Path) -> None:
    manifest = repo / "database/TOOL_DATA_MATERIALIZATION_MANIFEST.csv"
    if not manifest.is_file():
        raise SystemExit("Missing database/TOOL_DATA_MATERIALIZATION_MANIFEST.csv")

    errors: list[str] = []
    generated = 0
    with manifest.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            generated += 1
            rel = row["RepoPath"]
            path = repo / rel
            if not path.is_file():
                errors.append(f"missing generated dataset: {rel}")
                continue
            expected_bytes = int(row["Bytes"])
            actual_bytes = path.stat().st_size
            if actual_bytes != expected_bytes:
                errors.append(f"byte mismatch {rel}: {actual_bytes} != {expected_bytes}")
            expected_rows = (row.get("Rows") or "").strip()
            if expected_rows:
                actual_rows = count_rows(path)
                if actual_rows != int(expected_rows):
                    errors.append(f"row mismatch {rel}: {actual_rows} != {expected_rows}")

    for rel in sorted(REQUIRED_CURATED):
        if not (repo / rel).is_file():
            errors.append(f"missing curated lookup surface: {rel}")

    facts_path = repo / "database/FACTS.jsonl"
    fact_ids: set[str] = set()
    for lineno, line in enumerate(facts_path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"FACTS.jsonl line {lineno} invalid JSON: {exc}")
            continue
        fid = obj.get("id")
        if not fid:
            errors.append(f"FACTS.jsonl line {lineno} missing id")
        elif fid in fact_ids:
            errors.append(f"duplicate fact id: {fid}")
        fact_ids.add(fid)

    summary_path = repo / "database/snapshot/SNAPSHOT_SUMMARY.json"
    try:
        summary = json.loads(summary_path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        errors.append(f"invalid SNAPSHOT_SUMMARY.json: {exc}")
        summary = {}
    for key, expected in EXPECTED_SUMMARY.items():
        if summary.get(key) != expected:
            errors.append(f"snapshot {key}: {summary.get(key)!r} != {expected!r}")

    # Cross-surface minimums catch accidental truncation even if a manifest is edited.
    minimum_rows = {
        "database/dotnet/METHOD_CATALOG_0001_0600.csv": 600,
        "database/dotnet/METHOD_CATALOG_0601_1200.csv": 600,
        "database/dotnet/METHOD_CATALOG_1201_1294.csv": 94,
        "database/control/KAUTOHELPER_CALL_GRAPH.csv": 822,
        "database/features/FEATURE_METHOD_MAP.csv": 595,
        "database/features/FEATURE_ASSET_MAP.csv": 1143,
        "database/assets/IMAGE_TEMPLATE_INDEX_0001_0700.csv": 700,
        "database/assets/IMAGE_TEMPLATE_INDEX_0701_1393.csv": 693,
        "database/snapshot/ARTIFACT_MANIFEST_0001_0750.csv": 750,
        "database/snapshot/ARTIFACT_MANIFEST_0751_1450.csv": 700,
    }
    for rel, expected in minimum_rows.items():
        path = repo / rel
        if not path.is_file():
            errors.append(f"missing required high-volume surface: {rel}")
        elif count_rows(path) != expected:
            errors.append(f"required row count mismatch {rel}: {count_rows(path)} != {expected}")

    if errors:
        raise SystemExit("DATA-333 validation failed:\n- " + "\n- ".join(errors))

    machine = [
        p for p in (repo / "database").rglob("*")
        if p.is_file() and p.suffix.lower() in {".csv", ".json", ".jsonl"}
    ]
    print(
        f"DATA-333 validated: {generated} generated manifest datasets, "
        f"{len(REQUIRED_CURATED)} curated required surfaces, "
        f"{len(machine)} machine-readable database files, {len(fact_ids)} facts."
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--source", help="Optional frozen Debug directory or ZIP to fingerprint-check")
    ap.add_argument("--validate-only", action="store_true", help="Validate committed canonical database")
    # Backward-compatible alias while older docs/commands are updated.
    ap.add_argument("--payload-only", action="store_true", help=argparse.SUPPRESS)
    args = ap.parse_args()
    repo = Path(args.repo_root).resolve()
    if args.source:
        verify_source(Path(args.source).resolve())
    validate_database(repo)


if __name__ == "__main__":
    main()
