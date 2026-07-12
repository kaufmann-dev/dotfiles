# DICOM Surface project map

Use this map to find the narrowest implementation and regression-test surface.
Confirm details in the current source before editing because the repository is
the final authority.

## Module ownership

- `src/dicom_surface/cli.py`: Typer commands, Rich output, exit codes, JSON
  routing, lazy imports, and progress orchestration.
- `src/dicom_surface/progress_renderer.py`: independent interactive progress
  process used around native calls that can hold the interpreter lock.
- `src/dicom_surface/series.py`: DICOM header discovery, orientation splitting,
  slice ordering, ranking, warnings, and selectors.
- `src/dicom_surface/volume.py`: SimpleITK pixel loading, calibrated-HU checks,
  input warnings, and field-of-view boundary detection.
- `src/dicom_surface/presets.py` and `defaults.py`: public presets and lightweight
  defaults safe to import while building the CLI parser.
- `src/dicom_surface/geometry.py`: millimetre-to-voxel kernel math and physical
  volume helpers.
- `src/dicom_surface/segment.py`: thresholding, morphology, island filtering,
  padding, antialiasing, and resampling.
- `src/dicom_surface/pipeline.py`: single-series conversion, threshold
  resolution, the shared mask builder, shared surface finishing, provenance,
  warnings, and result contracts.
- `src/dicom_surface/surface.py`: MeshLib extraction, coordinate transforms,
  smoothing and simplification safeguards, topology checks, mesh I/O, atomic
  validated writes, and bounds.
- `src/dicom_surface/registration.py`: FFT translation, point-to-plane ICP,
  overlap metrics, and shared-field Dice.
- `src/dicom_surface/merge.py`: patient comparison, compatibility and
  registration gates, fused grids, and two-series result contracts.
- `src/dicom_surface/validate.py`: MeshLib import and the complete mesh-quality
  report.
- `src/dicom_surface/repair.py`: non-destructive MeshLib repair followed by
  validation.

## Focused verification

- Run `tests/test_cli.py` for command parsing, lightweight imports, output
  routing, progress, error handling, and exit status.
- Run `tests/test_series.py` for discovery, geometry grouping, ranking,
  selection, and DICOM warnings.
- Run `tests/test_geometry.py` for physical-unit and kernel-radius calculations.
- Run `tests/test_segment.py` for thresholds, morphology, islands, padding, and
  resampling primitives.
- Run `tests/test_pipeline.py` for presets, threshold resolution, conversion
  orchestration, and validation behavior.
- Run `tests/test_surface.py` for extraction, transforms, finishing safeguards,
  topology, serialization, atomic writes, and mesh validation.
- Run `tests/test_merge.py` for registration, overlap gates, identity checks,
  force behavior, and merge orchestration.
- Run `tests/test_repair.py` for non-destructive repair, validation, progress,
  and JSON behavior.

Reuse fixtures from `tests/conftest.py` and DICOM builders from the existing
tests. Keep tests deterministic; registration samples use a fixed seed and
geometry assertions should use explicit physical tolerances.

## Documentation ownership

- Update `README.md` for installation, command summaries, common workflows, or
  top-level safety behavior.
- Update `docs/user-guide.md` for user choices, warnings, input limitations,
  privacy, and validation interpretation.
- Update `docs/technical-reference.md` for architecture, algorithms, units,
  thresholds, compatibility, metrics, dependencies, and verification.
- Consult `docs/bugs/` for regression history. Add a new bug record only when
  the task explicitly asks for one.
