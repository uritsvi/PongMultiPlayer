import base64
import pickle

def pickle_dumps_base64(obj):

    return base64.b64encode(pickle.dumps(obj)).decode('utf-8').encode()


def pickle_loads_base64(data):
    decoded = base64.b64decode(data)
    obj = pickle.loads(decoded)
    return obj