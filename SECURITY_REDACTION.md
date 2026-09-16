# Security and redaction notes

## Sensitive-looking plaintext files in the supplied Debug bundle

The snapshot contains small plaintext files whose shapes strongly resemble account/license/key data. This repository must not copy their raw values.

Observed schemas only:

| Path | Observed shape | Handling |
|---|---|---|
| `code.txt` | 14 lines; each roughly 24 alphanumeric characters | treat as possible activation/license material; redact raw values |
| `luufile/KEYTAB.txt` | one 36-character GUID-like value | redact |
| `luufile/TONGHOP_KEYTAB.txt` | 6 lines containing GUID-like values | redact |
| `luufile/TAIKHOAN_DANGNHAP_AUTO.txt` | one pipe-delimited record with 2 fields | treat as credentials/session data; redact |
| `(MEmu).txt` | one pipe-delimited record with 4 fields | treat as account/emulator config; redact |

## Why Themida does not solve this

`Auto_ThanLong_Kteam_0789998118.exe` is protected/packed, but protection of executable code does not protect adjacent plaintext configuration/credential files. A rebuilt tool should move secrets out of ordinary text files.

## Recommended persistence split

### Non-secret config

Safe to persist as versioned JSON/YAML/SQLite:

- feature toggles;
- map/spot policy;
- item policy IDs/categories;
- thresholds;
- schedule;
- per-device display/controller preferences.

### Secret material

Store outside the repository and outside plaintext runtime folders:

- account passwords;
- access/refresh tokens;
- license keys;
- external API keys.

Use OS-protected credential storage or an encrypted secret store with explicit access boundaries.

## Logging rule

Logs should identify a device/account by stable redacted IDs, not by password/token/key contents. HTTP request/response logging must redact authorization headers and token fields.

## Repository rule

Generated materialization scripts should record:

- path;
- size;
- hash;
- schema/field count;

for sensitive text artifacts, but never emit their contents.

## Additional privacy leak

The PDB includes absolute developer source paths. Preserve only the project/module meaning in public documentation unless the exact path is needed for provenance; avoid treating workstation path details as functional application state.
