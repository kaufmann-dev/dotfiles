---
name: dicom-surface
description: Use the dicom-surface CLI to turn DICOM image series into STL, PLY, or OBJ meshes. Use only when the user explicitly invokes this skill, explicitly asks to use dicom-surface, or explicitly requests a surface mesh from DICOM data.
---

# DICOM Surface

Run `dicom-surface COMMAND --help` when options beyond these common workflows
are needed.

## Convert a scan

Inspect the available series, then convert the recommended one:

```sh
dicom-surface list <dicom-directory>
dicom-surface convert <dicom-directory> -o <output.stl>
```

The output extension selects STL, PLY, or OBJ. To choose another series, use
its displayed row ID, complete SeriesInstanceUID, or description:

```sh
dicom-surface convert <dicom-directory> --series <selector> \
  --preset <preset> -o <output.stl>
```

Run `dicom-surface presets` when choosing a tissue preset. The default `bone`
preset is for CT; use `--preset auto` for MR, CBCT, ultrasound, or other
uncalibrated intensities.

## Advanced conversion options (rarely needed)

Use these only when the user needs to tune a processing stage:

- Segmentation: `--threshold <value|auto>`, `--median-mm <mm>`,
  `--closing-mm <mm>`, `--opening-mm <mm>`, and
  `--min-island-mm3 <volume>`. Morphology values are kernel extents, not
  radii.
- Component retention: `--all-islands` keeps every island that survives the
  minimum-volume filter; `--all-components` keeps every extracted surface
  shell.
- Surface grid: `--resample-mm <mm>` uses an isotropic grid; `0` keeps the
  native grid. Coarser grids can erase thin structures.
- Finishing: `--smooth-iters <count>`, `--smooth-force <value>`,
  `--simplify-error-mm <mm>`, and `--post-smooth-iters <count>`. A simplify
  error of `0` disables simplification; other values are estimated QEM limits,
  not certified Hausdorff bounds.
- Boundary handling: `--no-cap` leaves anatomy open where it reaches the scan
  boundary instead of adding a flat cap.
- Automation: `--json <report.json>` writes results and provenance;
  `--quiet` suppresses normal progress output.

## Validate or repair a mesh

```sh
dicom-surface validate <mesh.stl>
dicom-surface repair <mesh.stl> -o <repaired.stl>
```

Always write repairs to a separate file. Validation measures mesh quality; it
does not prove anatomical correctness.

## Merge two scans

List both directories and select the intended series before merging:

```sh
dicom-surface merge <directory-a> <directory-b> \
  --series-a <selector> --series-b <selector> -o <output.stl>
```

Merge only scans of the same person and overlapping anatomy. Never add
`--force` unless the user explicitly accepts bypassing identity, modality, or
registration safety checks.

When both series are in one directory, omit `<directory-b>` and select them
with `--series-a` and `--series-b`.