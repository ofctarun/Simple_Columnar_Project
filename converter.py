import csv
import sys
import argparse
from src.writer import SCFWriter
from src.reader import SCFReader

def csv_to_custom(csv_path, output_path):
    print(f"Reading {csv_path}...")
    data = {}
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            for col, val in row.items():
                if col not in data: data[col] = []
                # Try to convert to int or float if possible
                try:
                    if '.' in val: data[col].append(float(val))
                    else: data[col].append(int(val))
                except ValueError:
                    data[col].append(val)
    
    writer = SCFWriter(output_path)
    writer.write(data)
    print(f"Successfully converted to {output_path}")

def custom_to_csv(custom_path, csv_output):
    print(f"Reading {custom_path}...")
    reader = SCFReader(custom_path)
    # Read ALL columns for full conversion
    data = reader.read_columns()
    
    cols = list(data.keys())
    num_rows = reader.row_count
    
    with open(csv_output, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(cols)
        for i in range(num_rows):
            writer.writerow([data[c][i] for c in cols])
    print(f"Successfully converted to {csv_output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SCF Converter Tool")
    parser.add_argument("mode", choices=['to_custom', 'to_csv'], help="Conversion mode")
    parser.add_argument("input", help="Input file path")
    parser.add_argument("output", help="Output file path")
    
    args = parser.parse_args()
    
    if args.mode == 'to_custom':
        csv_to_custom(args.input, args.output)
    else:
        custom_to_csv(args.input, args.output)