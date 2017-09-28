from . import secure_storage


class InvalidPassword(ValueError): pass


def initialize(storage_path, password):
    data = {}
    secure_storage.save(storage_path, data, password)


def set(storage_path, password, key, subkey, value):
    try:
        data = secure_storage.load(storage_path, password)
    except secure_storage.MalformedData:
        raise InvalidPassword(password)

    if key not in data:
        data[key] = {}

    data[key][subkey] = value

    secure_storage.save(storage_path, data, password)


def get(storage_path, password, key, subkey=None):
    try:
        data = secure_storage.load(storage_path, password)
    except secure_storage.MalformedData:
        raise InvalidPassword(password)

    if subkey:
        return data.get(key, {}).get(subkey)

    return data.get(key)


def get_keys(storage_path, password):
    try:
        data = secure_storage.load(storage_path, password)
    except secure_storage.MalformedData:
        raise InvalidPassword(password)
    return data.keys()


def remove(storage_path, password, key, subkey=None):
    try:
        data = secure_storage.load(storage_path, password)
    except secure_storage.MalformedData:
        raise InvalidPassword(password)

    if key not in data:
        return

    if subkey and subkey in data[key]:
        del data[key][subkey]
    else:
        del data[key]

    secure_storage.save(storage_path, data, password)

