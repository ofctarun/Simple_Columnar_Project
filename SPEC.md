# Simple Columnar Format (SCF) Specification v1.1

## Overview
The Simple Columnar Format (SCF) is a binary storage format designed for efficient analytical queries. It employs a footer-based metadata approach to allow for single-pass writing and efficient random access (column pruning).

## File Layout
The file is structured as follows:

| Section | Size | Description |
| :--- | :--- | :--- |
| **Magic Number** | 4 Bytes | The ASCII string 'SCF1' |
| **Data Blocks** | Variable | Contiguous blocks of zlib-compressed column data |
| **Metadata (JSON)**| Variable | UTF-8 encoded JSON string containing schema and offsets |
| **Meta Offset** | 8 Bytes | Little-endian 64-bit integer (Q) pointing to the start of Metadata |
| **Magic Footer** | 4 Bytes | The ASCII string 'SCF1' |



## Metadata Structure
The metadata JSON object contains:
- `row_count`: (Integer) Total number of rows in the dataset.
- `columns`: (Array) A list of column descriptors:
    - `name`: (String) The column header.
    - `type`: (String) One of `int32`, `float64`, or `string`.
    - `offset`: (Integer) The absolute byte position in the file where the compressed block begins.
    - `compressed_size`: (Integer) The size of the block on disk.
    - `uncompressed_size`: (Integer) The size of the block after decompression.

## Data Encoding & Compression
- **Compression**: Each column block is compressed independently using the **zlib** algorithm.
- **int32**: Signed 4-byte integers in little-endian format.
- **float64**: 8-byte double-precision floats in little-endian format.
- **string**: Encoded as a 4-byte unsigned length prefix (N), followed by N bytes of UTF-8 encoded text.