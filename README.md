# Bitemark

**Bitemark** is a sanitized reference implementation of the multimodal workflow used for the ODIN 2026 Bite2Text task. It shows how intraoral photographs (IOPs) and intraoral scans (IOSs) are routed to item-specific diagnostic modules and assembled into a deterministic orthodontic report.

> [!WARNING]
> This repository does **not** contain pretrained weights, training data, private calibration results, or deployment parameters. All numeric rule parameters in `configs/public_placeholder.yaml` are randomly generated placeholders marked `needs_to_be_finetuned: true`. They are not clinically meaningful and must not be used for diagnosis or challenge submission.
> The model weights& parameters will only be disclosed upon private request.

## Pipeline

```text
IOP photographs
  -> global five-view assignment
  -> upper/lower crowding heads
  -> frontal FDI masks -> dental midline

Upper/lower IOS meshes
  -> tooth instances + FDI labels + landmarks
  -> surface geometry -> molar, canine, anterior and transverse findings
  -> dual-arch point cloud -> overjet head
  -> shared FDI cloud -> Spee and Wilson heads
  -> FDI presence -> missing teeth

All item predictions
  -> fixed vocabulary and sentence order
  -> diagnostic-imaging-report.json
```

The design deliberately keeps model inference behind interfaces. A private deployment supplies trained implementations of the view classifier, 2D tooth segmenter, 3D tooth/landmark extractor, crowding classifiers, and point-cloud classifiers. The public package only contains routing, schemas, placeholder rules, and deterministic report assembly.

## Repository layout

```text
configs/public_placeholder.yaml  Random, non-deployable example parameters
docs/ARCHITECTURE.md             Item-to-input and item-to-method mapping
examples/synthetic_features.json Synthetic, non-patient demonstration input
models/README.md                 Expected private artifact slots
src/bitemark/                    Public orchestration package
tests/                           Tests using synthetic features only
```

## Install and run the synthetic example

```bash
python -m pip install -e .
bitemark \
  --features examples/synthetic_features.json \
  --config configs/public_placeholder.yaml \
  --output output/diagnostic-imaging-report.json \
  --allow-unfitted-placeholder
```

Without `--allow-unfitted-placeholder`, the application refuses to run with the public configuration. This guard is intentional.

## Supplying private models

Implement the protocols in `bitemark.backends` inside a private package and keep all artifacts outside Git. The expected model roles are documented in `models/README.md`. Do not commit private weights, model conversion outputs, calibration tables, patient data, or dataset paths.

## Status

This is a research code skeleton. It needs task-specific training, calibration, validation, and container integration before use:

**NEEDS TO BE FINETUNED.**

## License

Apache License 2.0. See `LICENSE`.
