---
name: medsurface
description: Use the medsurface CLI to list and select medical image volumes; convert DICOM, NIfTI, NRRD, or MetaImage volumes into STL, PLY, or OBJ meshes; register and merge scans; and validate or repair meshes. Use only when the user explicitly invokes this skill, asks to use medsurface, or requests a surface mesh from supported medical imaging data.
---

# medsurface

Use the installed `medsurface` command. Run `medsurface COMMAND --help` when
options beyond these workflows are needed.

Treat source images, logs, JSON reports, and derived meshes as potentially
identifying medical data. Never present a mesh as suitable for diagnosis,
treatment planning, or another clinical decision. Segmentation, smoothing,
resampling, and field-of-view capping can change or omit anatomy, and a valid
mesh can still be anatomically wrong.

## Inspect and select a volume

`INPUT` may be a supported image file or a directory tree containing DICOM,
NIfTI (`.nii` or `.nii.gz`), NRRD (`.nrrd` or `.nhdr`), or MetaImage (`.mha` or
`.mhd`) volumes.

Inspect any directory or potentially multi-volume input immediately before
conversion:

```sh
medsurface list <input>
```

Use only the positive integer ID displayed by `list` to select a volume. Never
use a DICOM UID, series number, description, or filename as a selector. Omit a
selector only when `list` shows an automatic default or the input is one direct
supported file. If selection is ambiguous, ask the user to choose an ID.

## Convert a volume

Convert the automatic default or a selected volume:

```sh
medsurface convert <input> -o <output.stl>
medsurface convert <input> --volume <id> --preset <preset> -o <output.stl>
```

The output extension selects STL, PLY, or OBJ. Run `medsurface presets` before
choosing a tissue preset. The default `bone` preset assumes calibrated CT-like
values; use `--preset auto` for uncalibrated intensities unless the user gives
an intentional numeric `--threshold`. Do not treat values as Hounsfield units
after a calibration warning.

Use processing overrides only when the user needs to tune a stage:

- Segmentation: `--threshold <value|auto>`, `--median-mm <mm>`,
  `--closing-mm <mm>`, `--opening-mm <mm>`, and
  `--min-island-mm3 <volume>`. Morphology values are kernel extents, not radii.
- Component retention: `--all-islands` keeps every surviving labelmap island;
  `--all-components` keeps every extracted surface shell.
- Surface grid: `--resample-mm <mm>` uses an isotropic grid; `0` keeps the
  native grid. Coarser grids can erase thin structures.
- Finishing: `--smooth-iters <count>`, `--smooth-force <value>`,
  `--simplify-error-mm <mm>`, and `--post-smooth-iters <count>`. A simplify
  error of `0` disables simplification; other values are estimated QEM limits,
  not certified Hausdorff bounds.
- Boundary handling: `--no-cap` leaves anatomy open where it reaches the scan
  boundary instead of adding a flat cap.

Use `--json <report.json>` to write conversion results and provenance to a
separate file. Use `--quiet` only to suppress normal progress; warnings and
failures remain significant.

A successful conversion validates both the in-memory surface and serialized
temporary mesh before atomically publishing the output. Inspect its warnings;
do not run a redundant `validate` command unless the user requests a separate
check.

## Merge two volumes

List both inputs, select the intended volumes, and confirm that they show the
same person and overlapping anatomy before merging:

```sh
medsurface list <fixed-input>
medsurface list <moving-input>
medsurface merge <fixed-input> <moving-input> \
  --fixed-volume <id> --moving-volume <id> -o <output.stl>
```

The fixed input defines the output coordinate frame. To merge two volumes from
one directory, repeat the directory path and choose two IDs. Use
`--fixed-threshold` and `--moving-threshold` when the inputs need different
thresholds; use `--grid-mm` to change the fused isotropic grid.

`medsurface` does not establish subject identity. Never add `--force` unless
the user explicitly accepts bypassing registration-quality gates and the risk
of a plausible-looking but incorrect fusion. `--force` does not bypass input,
selection, loading, duplicate-input, or size errors.

Like conversion, a successful merge validates the mesh before atomically
publishing it.

## Validate or repair a mesh

```sh
medsurface validate <mesh.stl>
medsurface repair <mesh.stl> -o <repaired.stl>
```

Always write repairs to a separate file. Validation measures structural mesh
quality; it does not prove anatomical correctness, manufacturability, or
clinical fitness.

For machine-readable output, `list --json`, `validate --json`, and
`repair --json` write JSON to stdout. In contrast, `convert --json <path>` and
`merge --json <path>` write provenance to a file. Never let a mesh or JSON
report overwrite an image header, DICOM instance, detached image payload, or
another input.
