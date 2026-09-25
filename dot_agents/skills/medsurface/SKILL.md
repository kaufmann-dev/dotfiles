---
name: medsurface
description: Use the medsurface CLI to inspect medical image volumes, strictly convert volume storage formats, extract surface meshes from intensity volumes or labelmaps, remove stair-step ripples from extracted surfaces, fuse matching scans or masks into editable binary labelmaps, and validate or repair meshes. Use when the user asks to process supported DICOM, NIfTI, NRRD, or MetaImage data with medsurface.
---

# medsurface

Use the installed `medsurface` command. Run `medsurface COMMAND --help` before
using options not covered here.

Treat source images, logs, JSON reports, labelmaps, and meshes as potentially
identifying medical data. Never present an output as suitable for diagnosis,
treatment planning, or another clinical decision. Segmentation, registration,
resampling, smoothing, and field-of-view capping can change or omit anatomy; a
structurally valid mesh can still be anatomically wrong.

## Inspect and select volumes

`INPUT` may be a supported image file or a directory tree containing DICOM,
NIfTI (`.nii`, `.nii.gz`), NRRD (`.nrrd`, `.nhdr`), or MetaImage (`.mha`,
`.mhd`) volumes.

Inspect every directory or potentially multi-volume input immediately before
processing it:

```sh
medsurface list INPUT
```

Use only the positive integer ID displayed by `list`. Never use a DICOM UID,
series number, description, or filename as a selector. Omit the selector only
when `list` marks an automatic default or the input is one direct supported
file. If selection remains ambiguous, ask the user to choose an ID.

## Strictly convert a volume

Use `convert` only to change storage format:

```sh
medsurface convert INPUT --volume ID -o OUTPUT.nii.gz
medsurface convert INPUT -o OUTPUT.nrrd --strip-metadata \
  --json conversion.json
```

Atomic outputs are `.nii`, `.nii.gz`, `.nrrd`, and `.mha`. Detached `.nhdr`
and `.mhd` files are input-only. The suffix selects format and compression.

Conversion preserves the loaded voxel values, scalar pixel type, components,
dimensions, spacing, origin, and direction. It does not threshold, cast,
resample, normalize, or reorient. Metadata preservation is best effort;
`--strip-metadata` removes source metadata while retaining required format
headers. The command writes a temporary sibling, reads it back, verifies the
core image contract, and only then atomically replaces the destination.

Do not use `convert` to create a mesh. Use `extract` for that.

## Extract an intensity surface

Use `extract` to segment one intensity volume and publish STL, PLY, or OBJ:

```sh
medsurface presets
medsurface extract INPUT --volume ID --preset bone -o MODEL.stl
medsurface extract INPUT --threshold auto -o MODEL.ply --json extract.json
```

The default `bone` preset assumes calibrated CT-like values. Use `--preset
auto` for uncalibrated intensities unless the user provides an intentional
numeric `--threshold`. Do not treat stored values as Hounsfield units after a
calibration warning.

Use processing overrides only when requested or needed:

- Segment with `--threshold`, `--median-mm`, `--closing-mm`, `--opening-mm`,
  `--min-island-mm3`, and `--all-islands`. Morphology values are kernel extents,
  not radii.
- Select extracted shells with `--components all|largest`.
- Set the surface grid with `--resample-mm`; `0` retains the native grid.
- Finish with `--mask-smooth-mm`, `--mesh-smooth-iters`,
  `--simplify-error-mm`, and `--post-mesh-smooth-iters`.
- Remove broad slice-terrace ripples with `--destep auto|all|band`; see
  "Remove stair-step ripples".
- Use `--no-cap` only when an open field-of-view boundary is intentional.

Extraction validates both the in-memory mesh and the serialized temporary mesh
before atomic publication. Inspect every warning. Do not run redundant
validation unless the user requests a separate check.

## Extract an external labelmap

Use `labelmap extract` for a direct NIfTI, NRRD, or MetaImage segmentation:

```sh
medsurface labelmap extract MASK.nii.gz -o MODEL.stl
```

Every finite, discrete, non-negative, nonzero value becomes one foreground
class. Fractional probability maps and empty labelmaps are rejected. Labelmap
extraction has its own surface defaults and accepts the surface-grid,
smoothing, simplification, `--destep`, component, capping, size, JSON, and quiet controls
shown by `medsurface labelmap extract --help`.

## Remove stair-step ripples

CT and MR slice terraces can survive extraction as broad, shallow ripples on
smooth anatomy such as a skull vault. Both `extract` and `labelmap extract`
accept an optional final fairing stage. It is off unless `--destep` is given:

```sh
medsurface labelmap extract MASK.nii.gz -o MODEL.stl --destep auto
medsurface extract INPUT --volume ID -o MODEL.stl --destep band \
  --destep-axis z --destep-full-mm -555 --destep-frozen-mm -600
```

Choose the region:

- `auto` is the default choice. It freezes tightly curved detail such as
  teeth, orbital and nasal rims, and bone edges, keeps about 10 mm around large
  detail such as the face frozen, and fairs broad surfaces such as the vault.
  Tiny isolated bumps are faired with their surroundings.
- `band` ramps from never moving at `--destep-frozen-mm` to fully faired at
  `--destep-full-mm` along `--destep-axis` (default `z`), in model millimetres.
  Their order selects the faired side. Read `bbox_min` and `bbox_max` from
  `medsurface validate MODEL.stl --json` to place the ramp between the ripples
  and detail that must stay unchanged. Use it when `auto` protects too much or
  too little.
- `all` fairs every vertex and also rounds teeth and edges. Use it only when
  the user explicitly accepts that.

`--destep-iters` (default 600) sets the fairing reach and `--destep-max-mm`
(default 1) caps each vertex's displacement. The band options require
`--destep band`, and every tuning option requires `--destep`. Reach is
measured in triangles, so finer meshes need more iterations; too many
iterations slowly inflate the surface and trigger a warning when over 10% of
vertices reach the cap. Lower the iterations when that warning appears.

Fairing deliberately changes the faired anatomy: it flattens shallow features
such as sutures along with the ripples. Report the logged faired and frozen
percentages, displacement, and volume change. The JSON report records them
under `provenance.surface_finishing.destep`. Folding or self-intersecting
fairing is reverted locally; if no clean result exists, the unfaired surface is
kept with a warning. Judge ripples with smooth shading and low-angle light;
soft lighting and decimated previews hide them.

## Fuse volumes into a binary labelmap

List both inputs, select the intended volumes, and confirm that they show the
same subject and overlapping non-deforming anatomy:

```sh
medsurface list FIXED
medsurface list MOVING
medsurface fuse FIXED MOVING \
  --fixed-volume FIXED_ID --moving-volume MOVING_ID \
  --preset bone --grid-mm 0.8 -o FUSED.nrrd --json fusion.json
medsurface labelmap extract FUSED.nrrd -o FUSED.stl
```

The fixed input defines the physical coordinate system. Intensity fusion
segments and cleans each input independently, rigidly registers moving
foreground to fixed foreground, resamples both masks onto an axis-aligned
isotropic grid, and publishes scalar `uint8` values `0` and `1`. Use
`--fixed-threshold` and `--moving-threshold` when the scans need different
thresholds. A finer `--grid-mm` preserves more detail at cubic memory cost.

Fusion outputs are `.nii`, `.nii.gz`, `.nrrd`, or `.mha` only. Fusion never
writes a mesh and exposes no surface-smoothing, simplification, capping, or
component controls. Inspect or edit the binary result, then pass it explicitly
to `labelmap extract`.

## Fuse external labelmaps

Register and union two direct masks that represent matching rigid structures:

```sh
medsurface labelmap fuse FIXED_MASK.nii.gz MOVING_MASK.mha \
  --grid-mm 0.8 -o FUSED.mha --json fusion.json
medsurface labelmap extract FUSED.mha -o FUSED.stl
```

Every positive source label is equivalent foreground; source label identities
and collisions are not preserved. Fusion output does not copy source metadata
or intensity-preset surface settings.

`medsurface` cannot establish subject identity. Never add `--force` unless the
user explicitly accepts bypassing registration-quality gates and the risk of a
plausible but incorrect fusion. `--force` does not bypass malformed
registration results, duplicate inputs, selection ambiguity, loading failures,
or voxel limits.

Do not invoke removed `merge`, `labelmap merge`, or `labelmap convert` commands.

## Validate or repair a mesh

```sh
medsurface validate MODEL.stl
medsurface repair MODEL.stl -o REPAIRED.stl
```

Always write repairs to a separate file. Validation measures structural mesh
quality, not anatomical correctness, manufacturability, or clinical fitness.

`list --json`, `validate --json`, and `repair --json` write JSON to stdout.
Conversion, extraction, and fusion use `--json FILE` for a separate report.
`--quiet` suppresses normal progress but not warnings or failures. Never let a
primary output or JSON report alias another, or overwrite an image header,
DICOM instance, detached payload, or other input.
