import hashlib

def get_hash(image_path):
    with open(image_path, "rb") as f:
        hash = hashlib.sha256(f.read()).hexdigest()
    return hash