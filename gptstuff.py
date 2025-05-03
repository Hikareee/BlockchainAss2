# Imports
import hashlib
import math

# Part 1: Key setup
class InventoryA:
    p = 1210613765735147311106936311866593978079938707
    q = 1247842850282035753615951347964437248190231863
    e = 815459040813953176289801

# Part 2: Signing
def sign(p, q, e):
    # Input and serialize
    m_plainText = input("Enter message: ").strip()
    m_serialized = m_plainText.replace(" ", "")  # remove spaces

    print(f"\nOriginal message: {m_plainText}")
    print(f"Serialized message (no spaces): {m_serialized}")

    # Hash the message
    m_hash_hex = hashlib.md5(m_serialized.encode()).hexdigest()
    m_hash = int(m_hash_hex, 16)

    print(f"Message hash (hex): {m_hash_hex}")
    print(f"Message hash (int): {m_hash}")

    # Calculate n and phi(n)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Verify e
    if not (1 < e < phi_n and math.gcd(e, phi_n) == 1):
        raise ValueError("e does not satisfy the conditions with phi(n)")

    # Calculate private key d
    d = pow(e, -1, phi_n)

    print(f"Calculated d: {d}")

    # Sign the message
    s = pow(m_hash, d, n)

    print(f"Signature (s): {s}")
    print(f"Public modulus (n): {n}")
    print(f"Public exponent (e): {e}\n")

    return m_hash, s, e, n

# Part 3: Verification
def verify(m_hash, s, e, n):
    print("--- Verifying Signature ---")
    alt_m = pow(s, e, n)
    print(f"Recovered hash (int): {alt_m}")
    print(f"Original message hash (int): {m_hash}")

    if alt_m == m_hash:
        print("✅ Signature is VALID!")
        return True
    else:
        print("❌ Signature is INVALID!")
        return False

# Utility for InventoryA
def inventoryA_signing():
    return sign(InventoryA.p, InventoryA.q, InventoryA.e)

def inventoryA_verify(m, s, e, n):
    return verify(m, s, e, n)

# Main runner
if __name__ == "__main__":
    m, s, e, n = inventoryA_signing()
    inventoryA_verify(m, s, e, n)
