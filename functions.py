import hashlib
def hash_file(filename):
    """Generate a hash for the contents of a file."""
    hasher = hashlib.md5()
    with open(filename, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def is_same_file(current_filename, previous_file_hash):
    """Check if the current file is the same as the previous file by comparing hashes."""
    current_file_hash = hash_file(current_filename)
    return current_file_hash == previous_file_hash, current_file_hash
    #return current_file_hash == previous_file_hash, current_file_hash