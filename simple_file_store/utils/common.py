import hashlib


def calculate_file_hash(file_path):
    sha1 = hashlib.sha1()
    chunk_size = 8192

    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            sha1.update(chunk)

    return sha1.hexdigest()
