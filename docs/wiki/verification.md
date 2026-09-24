# Verification

Verify each downloaded archive group against its published SHA-256 checksum before extraction. For split archives, gather every numbered part of a group and start extraction from the first part. The download page will provide exact filenames, checksums, and extraction commands once the public package is available.

| Stage | Check |
|---|---|
| Archive | File size and SHA-256 for every part; successful extraction |
| Source audio | Four-channel format, 48 kHz PCM, source manifest hashes |
| Clip plan | Ten-second grid, source-frame boundaries, selection reasons |
| Mono audio | Four channel files per selected clip; 480,000 frames per file |
| Annotations | Clip/session joins, time origin, row grain, and schema membership |
| Public labels | Printer values A/B/C across paths and annotation values |

A checksum verifies file bytes, while annotation review establishes the meaning and admissibility of a label. Both are required for a usable research dataset. See [Time coordinates](timebase.md) before comparing session, WAV, and clip-relative intervals.
