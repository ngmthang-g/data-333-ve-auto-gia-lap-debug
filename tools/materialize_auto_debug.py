#!/usr/bin/env python3
"""Validate DATA-333 canonical database and frozen donor fingerprints.

The full machine-readable database is committed as normal CSV/JSON files. A
small tar.xz payload exists only as a transport/bootstrap artifact for the
GitHub connector; CI expands it and commits the real database files.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,zipfile
from pathlib import Path

EXPECTED_SOURCE_SHA256={
'Auto_ThanLong_Kteam_0789998118.exe':'e1e4f555da3d4891ab0db674ee345bad67c2414632b7d1684151e7a9243134aa',
'Auto_ThanLong_obfusca.exe':'e2ba163c86852e81e60fe6c4694e031a2a7bf1b8838ddef799135736ad764e11',
'Auto_ThanLong_Kteam_0789998118.pdb':'5795d8e41d2504d732919dfd74d135a364ec6fc7cbbc47cdfd71021b2780ad84',
'KAutoHelper.dll':'55fb7f522ab98227c0c6e00009c8090bc99e6a84ebe1d79427d930fd7900ae05',
}
EXPECTED_SUMMARY={'file_count':1450,'total_bytes':146978306,'png_count':1393,'png_unique_sha256':1180,'png_duplicate_groups':178,'png_duplicate_extra_files':213,'pdb_identifier_count':783,'main_type_count':57,'main_method_count':1070,'main_field_count':429,'helper_type_count':40,'helper_method_count':224}
REQUIRED_CURATED={
'database/features/CORE_METHOD_RVA_INDEX.csv','database/dotnet/DEVICE_STATE_CATALOG.csv','database/control/CONTROL_CALL_CHAINS.csv','database/features/ACTIVITY_EVIDENCE_MATRIX.csv','database/features/FEATURE_STATE_JOIN.csv','database/assets/ASSET_ROLE_CATALOG.csv','database/TOOL_DATA_INDEX.md','database/SUBSYSTEM_SOURCE_MAP.md','database/SEMANTIC_JOIN_MAP.md','research/AUTO_RUNTIME_PROOF_QUEUE.md','analysis/07_FEATURE_STATE_AND_PROTECTED_BODY_MAP.md','analysis/08_VISUAL_ASSET_SEMANTICS.md'}
REQUIRED_ROWS={
'database/dotnet/METHOD_CATALOG_0001_0600.csv':600,
'database/dotnet/METHOD_CATALOG_0601_1200.csv':600,
'database/dotnet/METHOD_CATALOG_1201_1294.csv':94,
'database/control/KAUTOHELPER_CALL_GRAPH.csv':822,
'database/control/KAUTOHELPER_API.csv':224,
'database/features/FEATURE_METHOD_MAP.csv':290,
'database/features/FEATURE_ASSET_MAP.csv':1028,
'database/assets/IMAGE_TEMPLATE_INDEX_0001_0700.csv':700,
'database/assets/IMAGE_TEMPLATE_INDEX_0701_1393.csv':693,
'database/snapshot/ARTIFACT_MANIFEST_0001_0750.csv':750,
'database/snapshot/ARTIFACT_MANIFEST_0751_1450.csv':700,
'database/dotnet/PDB_IDENTIFIERS.csv':783,
'database/dotnet/EXTERNAL_MEMBERREFS.csv':852,
'database/dotnet/FIELD_CATALOG.csv':893,
}

def sha256_file(p:Path):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()

def verify_source(source:Path):
 found={}
 if source.is_dir():
  for n in EXPECTED_SOURCE_SHA256:
   ms=list(source.rglob(n))
   if not ms:raise SystemExit(f'missing frozen donor file: {n}')
   found[n]=sha256_file(ms[0])
 elif source.is_file() and source.suffix.lower()=='.zip':
  with zipfile.ZipFile(source) as z:
   by={Path(n).name:n for n in z.namelist() if not n.endswith('/')}
   for n in EXPECTED_SOURCE_SHA256:
    if n not in by:raise SystemExit(f'missing frozen donor file in ZIP: {n}')
    found[n]=hashlib.sha256(z.read(by[n])).hexdigest()
 else:raise SystemExit(f'unsupported source: {source}')
 bad={n:{'expected':e,'actual':found.get(n)} for n,e in EXPECTED_SOURCE_SHA256.items() if found.get(n)!=e}
 if bad:raise SystemExit('frozen source mismatch:\n'+json.dumps(bad,indent=2))
 print('Frozen donor fingerprints verified.')

def rows(p:Path):
 if p.suffix=='.jsonl':return sum(bool(x.strip()) for x in p.read_text(encoding='utf-8-sig').splitlines())
 if p.suffix=='.csv':
  with p.open(encoding='utf-8-sig',newline='',errors='replace') as f:return max(sum(1 for _ in csv.reader(f))-1,0)
 return None

def refresh_manifest(repo:Path):
 db=repo/'database';out=db/'TOOL_DATA_MATERIALIZATION_MANIFEST.csv';items=[]
 for p in sorted(db.rglob('*')):
  if not p.is_file() or p==out or p.suffix.lower() not in {'.csv','.json','.jsonl'}:continue
  n=rows(p) if p.suffix.lower() in {'.csv','.jsonl'} else ''
  items.append({'RepoPath':p.relative_to(repo).as_posix(),'Bytes':p.stat().st_size,'Rows':n if n is not None else '','SHA256':sha256_file(p)})
 with out.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['RepoPath','Bytes','Rows','SHA256']);w.writeheader();w.writerows(items)
 print(f'Refreshed manifest: {len(items)} machine-readable datasets.')

def validate(repo:Path):
 errors=[]
 for rel in sorted(REQUIRED_CURATED):
  if not (repo/rel).is_file():errors.append(f'missing curated surface: {rel}')
 for rel,n in REQUIRED_ROWS.items():
  p=repo/rel
  if not p.is_file():errors.append(f'missing high-volume dataset: {rel}')
  else:
   got=rows(p)
   if got!=n:errors.append(f'row mismatch {rel}: {got} != {n}')
 sp=repo/'database/snapshot/SNAPSHOT_SUMMARY.json'
 try:s=json.loads(sp.read_text(encoding='utf-8-sig'))
 except Exception as e:s={};errors.append(f'invalid snapshot summary: {e}')
 for k,v in EXPECTED_SUMMARY.items():
  if s.get(k)!=v:errors.append(f'snapshot {k}: {s.get(k)!r} != {v!r}')
 mp=repo/'database/TOOL_DATA_MATERIALIZATION_MANIFEST.csv'
 if not mp.is_file():errors.append('missing materialization manifest')
 else:
  with mp.open(encoding='utf-8-sig',newline='') as f:
   for r in csv.DictReader(f):
    p=repo/r['RepoPath']
    if not p.is_file():errors.append(f"manifest missing file: {r['RepoPath']}");continue
    if int(r['Bytes'])!=p.stat().st_size:errors.append(f"manifest byte mismatch: {r['RepoPath']}")
    if r.get('SHA256') and r['SHA256']!=sha256_file(p):errors.append(f"manifest hash mismatch: {r['RepoPath']}")
    if (r.get('Rows') or '').strip() and int(r['Rows'])!=rows(p):errors.append(f"manifest row mismatch: {r['RepoPath']}")
 ids=set();fp=repo/'database/FACTS.jsonl'
 for i,line in enumerate(fp.read_text(encoding='utf-8-sig').splitlines(),1):
  if not line.strip():continue
  try:o=json.loads(line)
  except Exception as e:errors.append(f'FACTS line {i}: {e}');continue
  fid=o.get('id')
  if not fid:errors.append(f'FACTS line {i}: missing id')
  elif fid in ids:errors.append(f'duplicate fact id: {fid}')
  ids.add(fid)
 if errors:raise SystemExit('DATA-333 validation failed:\n- '+'\n- '.join(errors))
 machine=[p for p in (repo/'database').rglob('*') if p.is_file() and p.suffix.lower() in {'.csv','.json','.jsonl'}]
 print(f'DATA-333 validated: {len(machine)} machine-readable files, {len(ids)} facts, frozen snapshot OK.')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',default='.');ap.add_argument('--source');ap.add_argument('--refresh-manifest',action='store_true');ap.add_argument('--validate-only',action='store_true');a=ap.parse_args();repo=Path(a.repo_root).resolve()
 if a.source:verify_source(Path(a.source).resolve())
 if a.refresh_manifest:refresh_manifest(repo)
 validate(repo)
if __name__=='__main__':main()
