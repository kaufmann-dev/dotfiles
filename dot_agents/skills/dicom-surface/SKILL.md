---
name: dicom-surface
description: Use the dicom-surface CLI to turn DICOM image series into STL, PLY, or OBJ meshes. Use only when the user explicitly invokes this skill or when the user explicitly requests a mesh from a DICOM series.
---

# DICOM Surface

Run `dicom-surface COMMAND --help` when options beyond these common workflows
are needed.

## Convert a scan

Inspect the available series and presets first:

```sh
dicom-surface list <dicom-directory>
dicom-surface presets
```

Use the recommended series unless the user chooses another. Select another
series by its displayed row ID, complete SeriesInstanceUID, or description:

```sh
dicom-surface convert <dicom-directory> --series <selector> \
  --preset <preset> -o <output.stl>
```

Omit `--series` or `--preset` to use the defaults. The output extension
selects STL, PLY, or OBJ.

## Advanced conversion options

Override only the stages the user wants to control:

- Segmentation: `--threshold <value|auto>`, `--median-mm <mm>`,
  `--closing-mm <mm>`, `--opening-mm <mm>`, and
  `--min-island-mm3 <volume>`.
- Component retention: `--all-islands` keeps every segmented island;
  `--all-components` keeps every extracted surface shell.
- Surface grid: `--resample-mm <mm>` uses an isotropic grid; `0` keeps the
  native grid. Coarser grids can erase thin structures.
- Finishing: `--smooth-iters <count>`, `--smooth-force <value>`,
  `--simplify-error-mm <mm>`, and `--post-smooth-iters <count>`. A simplify
  error of `0` disables simplification.
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
