import io

try:
    import h5py
except ImportError:
    h5py = None

IMPORT_MISSING_MESSAGE = "h5 assertion requires unavailable optional dependency h5py"


def _assert_h5py():
    if h5py is None:
        raise Exception(IMPORT_MISSING_MESSAGE)


def assert_has_h5_attribute(output_bytes, key, value):
    """Asserts the specified HDF5 output has a given key-value pair as HDF5
    attribute"""
    _assert_h5py()
    output_temp = io.BytesIO(output_bytes)
    local_attrs = h5py.File(output_temp, 'r').attrs
    assert key in local_attrs and str(local_attrs[key]) == value, (
        "Not a HDF5 file or H5 attributes do not match:\n\t%s\n\n\t(%s : %s)" % (local_attrs.items(), key, value))


def assert_has_h5_keys(output_bytes, keys):
    """ Asserts the specified HDF5 output has the given keys."""
    _assert_h5py()
    keys = [k.strip() for k in keys.strip().split(',')]
    h5_keys = sorted(keys)
    output_temp = io.BytesIO(output_bytes)
    local_keys = []
    def append_keys(key):
        local_keys.append(key)
        return None
    h5py.File(output_temp, 'r').visit(append_keys)
    missing = 0
    for key in h5_keys:
        if key not in local_keys:
            missing += 1
    assert missing == 0, "Not a HDF5 file or H5 keys missing:\n\t%s\n\t%s" % (local_keys, h5_keys)
