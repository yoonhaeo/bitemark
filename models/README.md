# Private model artifact slots

No weights are distributed in this repository.

A private deployment must provide trained implementations for these roles:

1. five-class IOP view-position classifier
2. upper-arch crowding classifier
3. lower-arch crowding classifier
4. FDI-aware 2D tooth-instance segmenter
5. IOS tooth-instance and landmark extractor
6. overjet point-cloud classifier
7. Curve of Spee point-cloud classifier
8. Curve of Wilson point-cloud classifier

Keep artifacts in a private model registry or a Git-ignored local directory. Common model extensions are blocked by the repository `.gitignore`.

**NEEDS TO BE FINETUNED. No public checkpoint is provided.**
