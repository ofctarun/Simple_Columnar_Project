# Simple Columnar File Format (SCF)

## Project Overview

This project implements a custom **binary columnar file format** from scratch, designed for high‑performance analytical data access. Unlike traditional row‑based formats such as CSV, this format stores data **column by column**, enabling efficient **column pruning**, reduced disk I/O, and better compression.

The implementation fulfills the requirements of the **"Build a Simple Columnar File Format from Scratch"** task and demonstrates core concepts used in modern analytical storage engines.

---

## Key Features

- **Custom Binary Layout**  
  A well‑defined header‑based binary specification for metadata and data blocks.

- **Columnar Storage Model**  
  Each column is stored as a contiguous compressed block on disk.

- **Compression**  
  All column data blocks are compressed using the `zlib` algorithm to reduce file size.

- **Efficient Random Access**  
  Metadata includes byte offsets, allowing direct `seek()` access to individual columns without scanning the entire file.

- **Data Type Support**  
  - 32‑bit integers (`int32`)  
  - 64‑bit floating‑point numbers (`float64`)  
  - Variable‑length UTF‑8 encoded strings

---

## Project Structure

```
.
├── src/
│   ├── reader.py        # SCFReader for selective column reading
│   ├── writer.py        # Binary writer for SCF format
│   └── utils.py         # Encoding, decoding, and compression helpers
├── converter.py         # CLI tool for CSV ↔ SCF conversion
├── test.csv             # Sample input CSV
├── output.scf           # Generated columnar file
└── README.md
```

---

## Installation

This project relies entirely on the **Python standard library**.

- **Python Version**: 3.6 or higher
- **External Dependencies**: None

No additional installation steps are required.

---

## Usage

### 1. Convert CSV to SCF Format

Convert a standard CSV file into the custom `.scf` columnar format:

```bash
python converter.py to_custom test.csv output.scf
```

---

### 2. Convert SCF Back to CSV

Reconstruct the original CSV data from an SCF file:

```bash
python converter.py to_csv output.scf back_to_original.csv
```

---

### 3. Selective Column Reading (Column Pruning)

One of the main advantages of SCF is the ability to read **only required columns** directly from disk.

```python
from src.reader import SCFReader

reader = SCFReader("output.scf")

# Reads only the 'name' column, skipping others on disk
data = reader.read_columns(["name"])

print(data)
```

This approach avoids unnecessary disk reads and decompression, improving performance for analytical workloads.

---

## Performance Notes

The SCF reader uses column metadata stored in the file header to perform direct `f.seek()` operations. This enables:

- Minimal disk I/O
- Faster query execution for large datasets
- Efficient analytical access patterns

Compared to CSV parsing, this design scales significantly better for read‑heavy and column‑oriented workloads.

---

## Learning Outcomes

This project demonstrates:

- Binary file format design
- Columnar data storage principles
- Compression techniques
- Efficient file seeking and offset‑based access
- Foundations of modern data warehouse file formats (e.g., Parquet, ORC)

---

## License

This project is provided for educational purposes. You are free to use, modify, and extend it as needed.

