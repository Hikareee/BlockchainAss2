#Imports 
import hashlib
import math

# Part 1 Key setup
class InventoryA:
    p = 1210613765735147311106936311866593978079938707
    q = 1247842850282035753615951347964437248190231863
    e = 815459040813953176289801

class InventoryB:
    p = 787435686772982288169641922308628444877260947
    q = 1325305233886096053310340418467385397239375379
    e = 692450682143089563609787

class InventoryC:
    p = 1014247300991039444864201518275018240361205111
    q = 904030450302158058469475048755214591704639633
    e = 1158749422015035388438057

class InventoryD:
    p = 1287737200891425621338551020762858710281638317
    q = 1330909125725073469794953234151525201084537607
    e = 33981230465225879849295979

# Part 2 Signing
def sign(p, q, e):
    #First Serialize the record 
    m_plainText = input("Enter message: ")
    m_serialized = m_plainText.replace(" ", "")

    #Hash the message
    m_hash = hashlib.md5(m_serialized.encode()).hexdigest()

    #Convert the hash to an integer
    m_hash = int(m_hash, 16)

    #Calculate n
    n = p * q

    #Calculate phi
    phi_n = (p - 1) * (q - 1)

    #Use the provided e (do not regenerate)
    if math.gcd(e, phi_n) != 1:
        raise ValueError("Provided e is not relatively prime to phi(n)")

    d = pow(e, -1, phi_n)

    #Sign the message
    s = pow(m_hash, d, n)

    return m_hash, s, e, n

# Part 3 Verification
def verify(m_hash, s, e, n):
    alt_m = pow(s, e, n)
    if alt_m == m_hash:
        print("Signature is valid")
        return True
    else:
        print("Signature is invalid")
        return False
    
def inventoryA_signing():
    m, s, e, n = sign(InventoryA.p, InventoryA.q, InventoryA.e)
    return(m, s, e, n)

def inventoryA_verify(m,s,e,n):
    validity = verify(m,s,e,n)
    return validity

m,s,e,n = inventoryA_signing()
inventoryA_verify(m,s,e,n)
