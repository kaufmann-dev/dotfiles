---
name: dicom-surface
description: Develop, debug, review, and verify the dicom-surface Python CLI and its DICOM-to-mesh pipeline. Use when working in the kaufmann-dev/dicom-surface repository on series discovery, segmentation, surface extraction or finishing, registration and merge safety, validation or repair, Typer/Rich CLI behavior, tests, packaging, or related documentation.
---

# DICOM Surface

Work from the repository root and confirm `pyproject.toml` declares
`name = "dicom-surface"`. Keep changes grounded in the repository's current
contracts rather than generic medical-imaging assumptions.

## Gather context

1. Read `README.md` for the public command and safety contract.
2. Read only the relevant sections of `docs/technical-reference.md` for
   implementation behavior and `docs/user-guide.md` for user-facing behavior.
3. Search `docs/bugs/` for related regressions before changing an established
   path.
4. Read [references/project-map.md](references/project-map.md) to locate module
   ownership and focused tests.

## Protect project invariants

- Treat the program as non-clinical. Never claim diagnostic or anatomical
  correctness from mesh validity.
- Use generated synthetic DICOM and mesh fixtures for tests. Never add real
  patient data, derived meshes, identifiers, or paths containing patient
  details.
- Keep parser construction lightweight. Import MeshLib, SimpleITK,
  registration, validation, and processing code inside the command that needs
  it so help and usage errors remain fast.
- Preserve the separation between human and JSON output. Keep JSON destinations
  free of Rich formatting, progress text, warnings, and ANSI sequences.
- Preserve physical units and coordinate conventions explicitly: SimpleITK
  arrays are z/y/x, mesh input is transposed to x/y/z, and published vertices
  use DICOM patient LPS millimetres.
- Keep `convert` and `merge` on shared segmentation and surface-finishing
  paths. Avoid duplicated behavior that can drift.
- Require the complete validation contract for generated output. Keep
  temporary-file validation and atomic publication; never replace a destination
  with an invalid serialized mesh.
- Keep merge identity checks, registration gates, and `--force` boundaries
  explicit. Do not weaken a safety refusal merely to make a fixture pass.
- Keep CLI messages concise and free of tracebacks for expected input,
  selection, modality, file, and safety failures. Let unexpected programming
  errors remain observable.

## Implement changes

1. Change the lowest owning layer identified in the project map.
2. Add or update the nearest regression test with the implementation. Prefer
   geometric assertions and contract assertions over snapshots of incidental
   formatting.
3. Update existing public or technical documentation when behavior, flags,
   limitations, safety semantics, dependencies, or architecture change.
4. Update `uv.lock` with uv when changing dependencies. Preserve the uv version
   pinned in `pyproject.toml` and CI unless the task explicitly upgrades it.

## Verify changes

Run the smallest relevant check first:

```sh
uv run pytest -q tests/test_<area>.py
```

Run the full synthetic suite when a change crosses module boundaries, affects a
shared contract, or is ready for handoff:

```sh
uv run pytest -q
```

For CLI parser or import-boundary changes, also exercise the relevant help or
malformed invocation through `uv run dicom-surface`; keep the assertions in
`tests/test_cli.py`. For dependency setup, use `uv sync --locked`. For packaging
changes, finish with `uv build` after tests.

Do not require real scans for routine verification. If a behavior cannot be
validated with the synthetic suite, state the remaining real-data limitation
instead of weakening the automated checks.
