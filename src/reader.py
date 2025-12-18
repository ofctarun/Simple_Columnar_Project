import struct
import zlib
import json

class SCFReader:
    def __init__(self, filename):
        self.filename = filename
        self._load_metadata()

    def _load_metadata(self):
        with open(self.filename, 'rb') as f:
            magic = f.read(4)
            if magic != b"SCF1":
                raise ValueError("Not a valid SCF file!")
            
            meta_size = struct.unpack('<I', f.read(4))[0]
            meta_json = f.read(meta_size).decode('utf-8')
            self.metadata = json.loads(meta_json)
            self.row_count = self.metadata['row_count']
            self.columns = {c['name']: c for c in self.metadata['columns']}

    def read_columns(self, column_names=None):
        """Reads specific columns. If None, reads all."""
        if column_names is None:
            column_names = list(self.columns.keys())

        results = {}
        with open(self.filename, 'rb') as f:
            for name in column_names:
                col_meta = self.columns[name]
                
                # SEEK directly to the column's starting position
                f.seek(col_meta['offset'])
                
                # Read only the compressed block for THIS column
                compressed_data = f.read(col_meta['compressed_size'])
                raw_data = zlib.decompress(compressed_data)
                
                results[name] = self._deserialize_column(raw_data, col_meta['type'])
        return results

    def _deserialize_column(self, buffer, data_type):
        data = []
        offset = 0
        
        if data_type == 'int32':
            while offset < len(buffer):
                data.append(struct.unpack_it('<i', buffer[offset:offset+4])[0])
                offset += 4
        
        elif data_type == 'float64':
            while offset < len(buffer):
                data.append(struct.unpack_it('<d', buffer[offset:offset+8])[0])
                offset += 8
                
        elif data_type == 'string':
            while offset < len(buffer):
                str_len = struct.unpack_it('<I', buffer[offset:offset+4])[0]
                offset += 4
                data.append(buffer[offset:offset+str_len].decode('utf-8'))
                offset += str_len
                
        return data

# Note: struct.unpack_it is used for efficiency in loops