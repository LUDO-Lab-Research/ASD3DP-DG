# ASD3DP-DG

ASD3DP-DG extends [ASD3DP](https://github.com/LUDO-Lab-Research/ASD3DP) to three printer-build domains, labeled A, B, and C. It provides four-channel 3D-printer audio and session and clip annotations for anomalous sound detection under domain shift. This is a DCASE Task 2-style research dataset, not an official DCASE-organized release.

The collection contains 78 sessions, 40.05 hours of continuous audio, and 11,861 selected 10-second intervals. Four microphone channels provide 47,444 mono clip views. The channels are rear, left, front, and right. Printer A/B/C are build labels; Belt A/B are component names.

The [public dataset guide](docs/wiki/index.md) describes collection, file groups, and annotations. The [dataset on Google Drive](https://drive.google.com/drive/folders/1dABXcAjs-b6dA5qjiMSdtwvO69cFOt2g) provides 78 full-session and 78 selected-clip audio archives, annotations, evidence, and SHA-256 checksums. See [Downloads](docs/wiki/download.md) before extracting files.

The [three-factor joint-shift benchmark](docs/wiki/joint-benchmark.md) reports
the completed J1–J3 printer, speed, and microphone-pair assignments. Its
[verified per-file scores and checkpoints](benchmarks/joint_shifts_20260924/results/README.md)
are linked to the fixed selections and independent result checks. Earlier
printer-only rotations are retained separately.

## Citation

```bibtex
@misc{kim2026asd3dpdg,
  title        = {{ASD3DP-DG}: A Controlled Multi-Printer Dataset for Anomalous Sound Detection under Domain Shift},
  author       = {Kim, JeongSik and Sung, JongWoo and Bae, HyeonJun and Kim, BoRyeon and Lee, JiAn},
  year         = {2026},
  publisher    = {LUDO Lab},
  url          = {https://github.com/LUDO-Lab-Research/ASD3DP-DG}
}
```

For the original [ASD3DP dataset](https://github.com/LUDO-Lab-Research/ASD3DP), use its separate citation:

```bibtex
@misc{kim2026asd3dp,
  title        = {{ASD3DP}: Session- and Clip-Level Annotation Bundle for a Real-World Four-Channel 3D-Printer Anomalous Sound Dataset},
  author       = {Kim, JeongSik and Sung, JongWoo and Bae, HyeonJun and Kim, BoRyeon and Lee, JiAn},
  year         = {2026},
  doi          = {10.5281/zenodo.21313911},
  url          = {https://doi.org/10.5281/zenodo.21313911}
}
```
