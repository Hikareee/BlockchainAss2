import json
import math

# Provided values from 'List of Keys'
p = 2089
q = 1044
e = 65537  # example RSA public key exponent

def modinv(a, m):
    return pow(a, -1, m)

def setup_keys():
    # Simplified version, generate d from e
    n = p * q
    phi = (p - 1) * (q - 1)
    d = modinv(e, phi)

    # Simulate key setup for 3 inventory nodes
    keys = {
        "public_key": {"e": e, "n": n},
        "private_key": {"d": d, "n": n},
        "node_keys": {
            "node1": {"id": "node1", "secret": 101},
            "node2": {"id": "node2", "secret": 202},
            "node3": {"id": "node3", "secret": 303}
        }
    }

    with open('data/keys.json', 'w') as f:
        json.dump(keys, f, indent=4)

if __name__ == "__main__":
    setup_keys()