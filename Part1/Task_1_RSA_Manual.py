#Imports 
import hashlib
import math
import Eggplant , EggplantV2, EggplantV3, EggplantV4


# Part 1 hash
def hash_message(m_plainText):
    #First Serialize the record 
    m_serialized = m_plainText.replace(" ", "")

    #Hash the message
    m_hash = hashlib.md5(m_serialized.encode()).hexdigest()

    #Convert the hash to an integer
    m_hash = int(m_hash, 16)
    return m_hash

def generate_key(p,q,e):
    #Calculate n
    n = p * q

    #Calculate phi
    phi_n = (p - 1) * (q - 1)

    #Use the provided e (do not regenerate)
    if math.gcd(e, phi_n) != 1:
        raise ValueError("Provided e is not relatively prime to phi(n)")

    d = pow(e, -1, phi_n)

    return (e,n), (d,n)

def sign(m_hash,d,n):
    #Sign the message
    s = pow(m_hash, d, n)

    return s

# Part 3 Verification
def verify(m_hash, s, e, n):
    alt_m = pow(s, e, n)
    if alt_m == m_hash:
        print("Signature is valid")
        return True
    else:
        print("Signature is invalid")
        return False
    
