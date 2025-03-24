import hashlib


hash_object_sha256 = hashlib.sha256()
hash_object_md5    = hashlib.md5()

hash_object_sha256.update("bruh".encode("utf-8"))
hash_object_md5.update(b"steveslist")

# SHA256 hash of "steveslist"
print("SHA256", hash_object_sha256.hexdigest())

# MD5 hash of "steveslist"
print("MD5", hash_object_md5.hexdigest())