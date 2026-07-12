---
name: dicom-surface
description: Work on the dicom-surface Python CLI and DICOM-to-mesh pipeline. Use for any implementation, debugging, review, testing, packaging, or documentation task in the kaufmann-dev/dicom-surface repository.
---

# DICOM Surface

Implement the requested change using the repository's existing conventions.

- Keep test data synthetic. Never add patient DICOM files, identifiers, or
  derived meshes.
- Treat mesh validity as distinct from anatomical or clinical correctness.
- Keep shared pipeline behavior shared instead of duplicating it per command.
- Add focused regression coverage for behavior changes.
- Run the nearest test with `uv run pytest -q tests/test_<area>.py`; run
  `uv run pytest -q` for cross-cutting changes.
- Update existing documentation when public behavior or constraints change.
