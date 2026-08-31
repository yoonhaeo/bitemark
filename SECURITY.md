# Security and release policy

## Never commit

- pretrained or fine-tuned model weights
- calibration tables or validation-selected thresholds
- patient images, meshes, labels, reports, or identifiers
- private filesystem paths, tokens, credentials, or service URLs
- cached predictions or intermediate tooth/landmark files

The `.gitignore` blocks common weight and data formats, but contributors must also review every staged diff before pushing.

## Public parameter policy

The public YAML file contains seeded random placeholders only. It carries `needs_to_be_finetuned: true`, and the runtime rejects it unless a user explicitly enables the synthetic demonstration flag. Replacing the flag with `false` is not sufficient for deployment. Private validation and release review are still required.

## Reporting an accidental disclosure

If a private artifact is committed, rotate any exposed credentials, remove the artifact from Git history, invalidate published releases, and contact the repository owner immediately.
