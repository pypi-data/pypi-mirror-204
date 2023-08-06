import os

def checkIfDirExistElseCreate(filepath):
    if not os.path.exists(os.path.dirname(filepath)):
        os.mkdir(os.path.dirname(filepath))

def trimForwardBackwardSlashFromStartOfDir(str_path):
        while str_path.startswith('\\') or str_path.startswith('/'):
            str_path = str_path[1:]
        return str_path

def bytes_to_uint(bytes_obj:bytes) -> int:
    """Convert a big-endian sequence of bytes to an unsigned integer."""
    return int.from_bytes(bytes_obj, byteorder="big", signed=False)
