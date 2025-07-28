import json
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from math import gcd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# RSA Parameters for PKG and Procurement Officer
pkg_p = 1004162036461488639338597000466705179253226703
pkg_q = 950133741151267522116252385927940618264103623
pkg_e = 973028207197278907211

po_p = 1080954735722463992988394149602856332100628417
po_q = 1158106283320086444890911863299879973542293243
po_e = 106506253943651610547613

def modinv(a, m):
    if gcd(a, m) != 1:
        raise Exception("Modular inverse does not exist")
    return pow(a, -1, m)

pkg_n = pkg_p * pkg_q
pkg_phi = (pkg_p - 1) * (pkg_q - 1)
pkg_d = modinv(pkg_e, pkg_phi)

po_n = po_p * po_q
po_phi = (po_p - 1) * (po_q - 1)
po_d = modinv(po_e, po_phi)

# Node info: IDs and random nonces r_i
inventory_data = {
    "A": {"ID": 126, "random": 621},
    "B": {"ID": 127, "random": 721},
    "C": {"ID": 128, "random": 821},
    "D": {"ID": 129, "random": 921},
}

def hash_message(value):
    return value % pkg_n  # Simplified hash

# Compute g_i = ID_i^d mod n for each node (simulating PKG distribution)
g_values = {k: pow(v["ID"], pkg_d, pkg_n) for k, v in inventory_data.items()}

#t_1 = r_1^(e) mod n
def generate_t_values():
    return {k: pow(v["random"], pkg_e, pkg_n) for k, v in inventory_data.items()}

#t = t_1 * t_2 * t_3 mod n
def compute_t(t_values):
    t = 1
    for val in t_values.values():
        t = (t * val) % pkg_n
    return t

def generate_partial_signature_Harn(node_id, msg_hash):
    """s_i = g_i * r_i^h mod n"""
    g_i = g_values[node_id]
    r_i = inventory_data[node_id]["random"]
    r_pow_h = pow(r_i, msg_hash, pkg_n)
    return (g_i * r_pow_h) % pkg_n


def aggregate_signatures_Harn(sigs):
    s = 1
    for sig in sigs:
        s = (s * sig) % pkg_n
    return s

# RSA enc/dec
def rsa_encrypt(m, e, n):
    return pow(m, e, n)

def rsa_decrypt(c, d, n):
    return pow(c, d, n)

def consensus(partial_signatures, h):
    """
    Validates all partial signatures to ensure they are correct.

    Args:
        partial_signatures (list): List of partial signatures from all nodes.
        h (int): The hash value computed from t and the message.

    Returns:
        bool: True if all partial signatures are valid, False otherwise.
    """
    output.insert(END, "\n🔍 Starting consensus validation for all partial signatures...\n")
    all_valid = True

    for idx, (node_id, sig) in enumerate(zip(inventory_data.keys(), partial_signatures)):
        g_i = g_values[node_id]
        r_i = inventory_data[node_id]["random"]
        expected_sig = (g_i * pow(r_i, h, pkg_n)) % pkg_n

        output.insert(END, f"Validator {node_id} (Signature {idx + 1}):\n")
        output.insert(END, f"   Partial Signature: {sig}\n")
        output.insert(END, f"   Expected Signature: {expected_sig}\n")

        if sig != expected_sig:
            output.insert(END, f"❌ Validator {node_id} validation FAILED.\n")
            all_valid = False
        else:
            output.insert(END, f"✅ Validator {node_id} validation PASSED.\n")

    if all_valid:
        output.insert(END, "\n✨ Consensus mechanism successful.\n")
        return True
    else:
        output.insert(END, "\n❌ Consensus mechanism failed.\n")
        return False

def run_query():
    item_id = entry.get()
    output.delete("1.0", END)

    INVENTORY_PATH = os.path.join(BASE_DIR, "inventory.json")
    with open(INVENTORY_PATH, "r") as f:
        data = json.load(f)

    item = next((x for x in data if x["itemID"] == item_id), None)

    if not item:
        output.insert(END, f"Item ID {item_id} not found!\n")
        return
    output.insert(END, f"👨🏻‍💻 Procurment Officer \n")
    quantity = item["quantity"]
    output.insert(END, f"🍆 Queried Item ID: {item_id}\n")
    # Display g values
    output.insert(END, f"\n🖥 PKG Forwards the query\n")
    output.insert(END, f"\n🗄 Inventories search the record and harn multi sign\n")
    for k, v in g_values.items():
        output.insert(END, f"Inventory {k} g_{k} = {v}\n")
    output.insert(END, "\n")
    # Display t_i values
    t_values = generate_t_values()
    for k, v in t_values.items():
        output.insert(END, f"Inventory {k} t_{k} = {v}\n")

    # Step 1: Compute t = product of t_i
    t = compute_t(t_values)
    output.insert(END, f"\n🍆 Combined t = {t}\n")

    # Step 2: Hash(t, message)
    h = hash_message(t + quantity)  # hash(t, m)
    output.insert(END, f"Hash(t, quantity) = {h}\n\n")

    # Step 3: Each node generates s_i
    partial_sigs = []
    for k in inventory_data:
        s_i = generate_partial_signature_Harn(k, h)
        partial_sigs.append(s_i)
        output.insert(END, f"{k} partial signature s_{k} = {s_i}\n")

    # Step 4: Combine s_i into full s
    final_signature = aggregate_signatures_Harn(partial_sigs)
    output.insert(END, f"\n🍆 Aggregated Signature: {final_signature}\n")
    output.insert(END, f"\n🗄 Inventory sends search result and all the public parameters to PKG\n" )
    output.insert(END, f"\n🖥 PKG initiates concensus mechanism\n")
    concensus_result = consensus(partial_sigs, h)
    if not concensus_result:
        output.insert(END, "❌ Consensus failed. Exiting...\n")
        return
    output.insert(END, "✅ Consensus passed.\n")
    output.insert(END, "\n🖥 PKG initiates Encryption Process\n")
    # Step 5: Encrypt only the quantity
    output.insert(END, f"\n🔒 Encryption Process:\n")
    output.insert(END, f"Original Quantity: {quantity}\n")
    encrypted_quantity = rsa_encrypt(quantity, po_e, po_n)
    output.insert(END, f"Encrypted Quantity: {encrypted_quantity}\n")
    output.insert(END, "\n🖥 PKG sends the encrypted quantity and signature to Procurement Officer\n")
    output.insert(END, "\n👨🏻‍💻 Procurement Officer receives the encrypted quantity\n")
    output.insert(END, "\n👨🏻‍💻 Procurement Officer initiates Decryption Process\n")

    # Step 6: Decrypt the quantity
    output.insert(END, f"\n🔓 Decryption Process:\n")
    decrypted_quantity = rsa_decrypt(encrypted_quantity, po_d, po_n)
    output.insert(END, f"Decrypted Quantity: {decrypted_quantity}\n")

    # Step 7: Verify the signature using PKG public key
    ids_product = 1
    for k in inventory_data:
        ids_product = (ids_product * pow(inventory_data[k]["ID"], 1, pkg_n)) % pkg_n

    left = pow(final_signature, pkg_e, pkg_n)
    right = (ids_product * pow(t, h, pkg_n)) % pkg_n

    output.insert(END, "\n👨🏻‍💻 Procurement Officer Initiates Signature Verification Process:\n")
    output.insert(END, f"\n🧮 Signature Verification:\n")
    output.insert(END, f"Left side (s^e mod n) = {left}\n")
    output.insert(END, f"Right side ((i_1 * i_2 * i_3) * t^h mod n) = {right}\n")

    if left == right:
        output.insert(END, "✅ Signature is VALID\n")
    else:
        output.insert(END, "❌ Signature is INVALID\n")

    # Final verification summary
    output.insert(END, f"\n📊 Final Results:\n")
    output.insert(END, f"Decrypted Quantity: {decrypted_quantity}\n")
    output.insert(END, f"Signature Valid: {'✅' if left == right else '❌'}\n")
    output.insert(END, f"👨🏻‍💻 Procurement Officer Recives Quantity Query Result ✅\n")

# GUI
root = Tk()
root.title("Inventory Query System 🍆")

Label(root, text="Enter Item ID:").pack(pady=5)
entry = Entry(root)
entry.pack(pady=5)

Button(root, text="Submit Query", command=run_query).pack(pady=5)

output = ScrolledText(root, width=85, height=30)
output.pack(padx=10, pady=10)

root.mainloop()
