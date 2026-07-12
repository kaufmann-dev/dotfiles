---
name: dicom-surface
description: Use the dicom-surface CLI to turn DICOM image series into STL, PLY, or OBJ meshes. Use when listing or selecting DICOM series, choosing segmentation presets or thresholds, converting scans, merging scans, validating meshes, or repairing meshes.
---

# DICOM Surface

Run `dicom-surface COMMAND --help` when options beyond these common workflows
are needed.

## Convert a scan

Inspect the available series first:

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

Omit `--series` or `--preset` to use the defaults. Use `--threshold <value>`
only when an explicit intensity threshold is intended. The output extension
selects STL, PLY, or OBJ.

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

Keep DICOM data local and private. Do not present generated meshes as suitable
for diagnosis, treatment planning, or other clinical decisions.
