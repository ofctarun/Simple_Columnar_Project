import struct
import zlib
import json

class SCFWriter:
    def __init__(self, filename):
        self.filename = filename
        self.magic = b"SCF1"

    def _serialize_column(self, data, data_type):
        buffer = b""
        if data_type == 'int32':
            for val in data:
                buffer += struct.pack('<i', int(val))
        elif data_type == 'float64':
            for val in data:
                buffer += struct.pack('<d', float(val))
        elif data_type == 'string':
            for val in data:
                encoded = str(val).encode('utf-8')
                buffer += struct.pack('<I', len(encoded))
                buffer += encoded
        
        uncompressed_size = len(buffer)
        compressed_data = zlib.compress(buffer)
        return compressed_data, uncompressed_size

    def write(self, df_dict):
        col_names = list(df_dict.keys())
        row_count = len(df_dict[col_names[0]])
        metadata_cols = []
        
        with open(self.filename, 'wb') as f:
            # 1. Write Magic Number
            f.write(self.magic)
            
            # 2. Write Data Blocks and track offsets
            for name in col_names:
                sample = df_dict[name][0]
                if isinstance(sample, int): dtype = 'int32'
                elif isinstance(sample, float): dtype = 'float64'
                else: dtype = 'string'
                
                comp_data, uncomp_size = self._serialize_column(df_dict[name], dtype)
                
                start_offset = f.tell()
                f.write(comp_data)
                
                metadata_cols.append({
                    "name": name,
                    "type": dtype,
                    "offset": start_offset,
                    "compressed_size": len(comp_data),
                    "uncompressed_size": uncomp_size
                })

            # 3. Write Metadata (Footer)
            meta_json = json.dumps({"row_count": row_count, "columns": metadata_cols}).encode('utf-8')
            meta_offset = f.tell()
            f.write(meta_json)
            
            # 4. Write Footer: [MetaOffset (8 bytes)][Magic (4 bytes)]
            f.write(struct.pack('<Q', meta_offset))
            f.write(self.magic)