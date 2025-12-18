# Simple Columnar Format (SCF) Specification v1.0

## File Layout
| Section | Size | Description |
| :--- | :--- | :--- |
| Magic Number | 4 Bytes | Always 'SCF1' |
| Meta Size | 4 Bytes | Little-endian integer (size of JSON metadata) |
| Metadata | Variable | UTF-8 JSON string containing schema and offsets |
| Data Blocks | Variable | Contiguous zlib-compressed column data |

## Metadata Structure
The metadata is a JSON object:
- `row_count`: Total number of rows.
- `columns`: A list of objects containing:
    - `name`: Column name.
    - `type`: 'int32', 'float64', or 'string'.
    - `offset`: Byte position where this column starts.
    - `compressed_size`: Size of the block on disk.
    - `uncompressed_size`: Size after decompression.

## Data Encoding
- **int32**: 4-byte little-endian integers.
- **float64**: 8-byte little-endian doubles.
- **string**: A "Length-Prefix" approach. 4 bytes for length (N), followed by N bytes of UTF-8 text.