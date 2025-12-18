Below is the complete, formatted content for your README.md. You can copy this directly into your file.

Simple Columnar File Format (SCF)
=================================

Project Overview
----------------

This project implements a custom binary columnar file format from scratch, designed for high-performance analytical data access. Unlike traditional row-based formats (like CSV), this format stores data column-by-column, allowing for **Selective Column Reading** (Column Pruning) and efficient compression.

This project satisfies the requirements for the "Build a Simple Columnar File Format from Scratch" task.

Features
--------

*   **Binary Layout**: Implements a custom header-based binary specification.
    
*   **Columnar Storage**: Each column's data is stored in a contiguous block.
    
*   **Compression**: Every data block is compressed using the zlib algorithm to save disk space.
    
*   **Efficient Seeking**: Uses metadata offsets to jump directly to specific columns without reading the entire file.
    
*   **Type Support**: Handles 32-bit integers, 64-bit floating points, and variable-length UTF-8 strings.
    

Project Structure
-----------------

Plaintext

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   simple-columnar-format/  ├── src/  │   ├── writer.py    # Logic for serializing and compressing data  │   ├── reader.py    # Logic for parsing and selective reading  │   └── __init__.py  ├── converter.py     # CLI tool for CSV <-> SCF conversion  ├── SPEC.md          # Formal binary format specification  ├── README.md        # Project documentation and usage  └── test.csv         # Sample input data   `

Installation
------------

The project uses the Python standard library. No external dependencies are required.

*   **Python Version**: 3.6+ recommended.
    

Usage
-----

### 1\. Convert CSV to Custom Format (csv\_to\_custom)

To convert a standard CSV file into the .scf format:

Bash

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python converter.py to_custom test.csv output.scf   `

### 2\. Convert Custom Format back to CSV (custom\_to\_csv)

To reconstruct the original data from the binary file:

Bash

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python converter.py to_csv output.scf back_to_original.csv   `

### 3\. Selective Column Reading

The reader is designed to allow developers to load only the columns they need. This is a core feature for performance optimization in data engineering:

Python

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   from src.reader import SCFReader  reader = SCFReader("output.scf")  # This only reads the 'name' column, skipping 'id' and 'score' on disk  data = reader.read_columns(["name"])  print(data)   `

Performance Note
----------------

By using byte offsets stored in the header, the reader performs an f.seek() operation to jump straight to the requested data. In large-scale systems, this is significantly faster than parsing a full CSV file because it minimizes disk I/O.