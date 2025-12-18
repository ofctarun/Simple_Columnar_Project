import struct
import zlib
import json

class SCFWriter:
    def __init__(self, filename):
        self.filename = filename
        self.magic = b"SCF1"
        self.columns = []
        self.row_count = 0

    def _serialize_column(self, data, data_type):
        """Converts a list of data into a compressed binary block."""
        buffer = b""
        
        if data_type == 'int32':
            # 'i' is for 32-bit integer, '<' for little-endian
            for val in data:
                buffer += struct.pack('<i', int(val))
        
        elif data_type == 'float64':
            # 'd' is for 64-bit double
            for val in data:
                buffer += struct.pack('<d', float(val))
        
        elif data_type == 'string':
            # Length-prefixed strings: [Length (4b)] + [UTF-8 Bytes]
            for val in data:
                encoded = str(val).encode('utf-8')
                buffer += struct.pack('<I', len(encoded))
                buffer += encoded
        
        uncompressed_size = len(buffer)
        compressed_data = zlib.compress(buffer)
        return compressed_data, uncompressed_size

    def write(self, df_dict):
        """df_dict is a dictionary {col_name: [values]}"""
        col_names = list(df_dict.keys())
        self.row_count = len(df_dict[col_names[0]])
        
        # Determine types (simple heuristic)
        processed_blocks = []
        metadata_cols = []
        
        # Temporary pointer to track where blocks will start
        # We will calculate exact offsets after we know the header size
        for name in col_names:
            sample = df_dict[name][0]
            if isinstance(sample, int): dtype = 'int32'
            elif isinstance(sample, float): dtype = 'float64'
            else: dtype = 'string'
            
            comp_data, uncomp_size = self._serialize_column(df_dict[name], dtype)
            processed_blocks.append(comp_data)
            metadata_cols.append({
                "name": name,
                "type": dtype,
                "compressed_size": len(comp_data),
                "uncompressed_size": uncomp_size,
                "offset": 0 # Placeholder
            })

        # Calculate offsets
        # Header = Magic(4) + MetaSize(4) + MetaJSON(N)
        # We'll calculate the JSON size first
        temp_meta = {"row_count": self.row_count, "columns": metadata_cols}
        meta_json = json.dumps(temp_meta).encode('utf-8')
        header_size = 4 + 4 + len(meta_json)
        
        current_offset = header_size
        for i in range(len(metadata_cols)):
            metadata_cols[i]['offset'] = current_offset
            current_offset += metadata_cols[i]['compressed_size']

        # Final Write
        with open(self.filename, 'wb') as f:
            f.write(self.magic)
            f.write(struct.pack('<I', len(meta_json)))
            f.write(meta_json)
            for block in processed_blocks:
                f.write(block)