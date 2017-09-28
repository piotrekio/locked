import hashlib
import json
import os.path

import Crypto.Cipher.AES


__all__ = ['MalformedData', 'save', 'load']


class MalformedData(ValueError): pass
class StorageDoesNotExist(OSError): pass


def save(path, data, password):
    with open(path, 'wb') as f:
        serialized_data = serialize(data)
        encrypted_data = encrypt(serialized_data, password)
        f.write(encrypted_data)


def load(path, password):
    if not os.path.exists(path):
        raise StorageDoesNotExist(path)

    with open(path, 'rb') as f:
        serialized_data = decrypt(f.read(), password)
        data = deserialize(serialized_data)
        return data


def serialize(data):
    return json.dumps(data)


def deserialize(data):
    return json.loads(data)


def encrypt(data, password):
    hashed_password = hash_password(password)
    initialization_vector = generate_initialization_vector()
    padded_data = with_padding(data)
    encrypted_data = Crypto.Cipher.AES.new(
        hashed_password,
        Crypto.Cipher.AES.MODE_CBC,
        IV=initialization_vector
    ).encrypt(
        hashed_password + padded_data
    )
    return initialization_vector + encrypted_data


def decrypt(data, password):
    raw_decrypted_data = decrypt_raw(data, password)

    decrypted_data = remove_check_string(raw_decrypted_data, password)

    return decrypted_data


def decrypt_raw(data, password):
    initialization_vector, encrypted_data = data[:16], data[16:]

    raw_decrypted_data = Crypto.Cipher.AES.new(
        hash_password(password),
        Crypto.Cipher.AES.MODE_CBC,
        IV=initialization_vector
    ).decrypt(
        encrypted_data
    )

    return raw_decrypted_data


def remove_check_string(raw_decrypted_data, password):
    hashed_password = hash_password(password)
    if raw_decrypted_data.startswith(hashed_password):
        try:
            return without_padding(raw_decrypted_data[len(hashed_password):])
        except UnicodeDecodeError:
            raise MalformedData()

    raise MalformedData()


def generate_initialization_vector():
    return open('/dev/urandom', 'rb').read(16)


def with_padding(string):
    length = len(string)
    return string.zfill(16 * length // 16 + 16 - length % 16).encode()


def without_padding(string):
    return string.lstrip(b'0')


def hash_password(password):
    return hashlib.sha256(password.encode()).digest()

