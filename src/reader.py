import struct
import zlib
import json
import os

class SCFReader:
    def __init__(self, filename):
        self.filename = filename
        self.metadata = {}
        self.columns = {}
        self.row_count = 0
        self._load_metadata()

    def _load_metadata(self):
        file_size = os.path.getsize(self.filename)
        with open(self.filename, 'rb') as f:
            # Read Footer: last 12 bytes [Offset(8) + Magic(4)]
            f.seek(file_size - 12)
            meta_offset = struct.unpack('<Q', f.read(8))[0]
            magic = f.read(4)
            
            if magic != b"SCF1":
                raise ValueError("Not a valid SCF file!")
            
            # Read JSON metadata
            f.seek(meta_offset)
            meta_len = (file_size - 12) - meta_offset
            meta_json = f.read(meta_len).decode('utf-8')
            
            self.metadata = json.loads(meta_json)
            self.row_count = self.metadata['row_count']
            self.columns = {c['name']: c for c in self.metadata['columns']}

    def read_columns(self, column_names=None):
        if column_names is None:
            column_names = list(self.columns.keys())

        results = {}
        with open(self.filename, 'rb') as f:
            for name in column_names:
                if name not in self.columns: continue
                col = self.columns[name]
                f.seek(col['offset'])
                raw_bytes = zlib.decompress(f.read(col['compressed_size']))
                results[name] = self._deserialize_column(raw_bytes, col['type'])
        return results

    def _deserialize_column(self, buffer, data_type):
        data = []
        if data_type == 'int32':
            for val in struct.iter_unpack('<i', buffer): data.append(val[0])
        elif data_type == 'float64':
            for val in struct.iter_unpack('<d', buffer): data.append(val[0])
        elif data_type == 'string':
            offset = 0
            while offset < len(buffer):
                s_len = struct.unpack_from('<I', buffer, offset)[0]
                offset += 4
                data.append(buffer[offset:offset+s_len].decode('utf-8'))
                offset += s_len
        return data