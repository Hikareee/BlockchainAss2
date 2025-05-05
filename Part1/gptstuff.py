import json
import os
import hashlib
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from InventoryKeys import InventoryA, InventoryB, InventoryC, InventoryD


# Inventory class map
inventory_classes = {
    'A': InventoryA,
    'B': InventoryB,
    'C': InventoryC,
    'D': InventoryD
}

# Core RSA and Hashing Functions
def hash_message(message):
    return int(hashlib.md5(message.replace(" ", "").encode()).hexdigest(), 16)

def generate_key(p, q, e):
    n = p * q
    phi = (p - 1) * q - (p - 1)
    d = pow(e, -1, phi)
    return (e, n), (d, n)

def sign(m_hash, d, n):
    return pow(m_hash, d, n)

def verify(m_hash, s, e, n):
    alt_m = pow(s, e, n)

    print(f"📝 Original message hash:     {m_hash}")
    print(f"🔁 Recovered hash from sig:   {alt_m}")

    if alt_m == m_hash:
        print("✅ Signature is valid")
        return True
    else:
        print("❌ Signature is invalid")
        return False

# Blockchain and PoA Consensus
CHAIN_FILE = "blockchain.json"

def load_chain():
    if os.path.exists(CHAIN_FILE):
        with open(CHAIN_FILE, "r") as f:
            return json.load(f)
    return []

def save_chain(chain):
    with open(CHAIN_FILE, "w") as f:
        json.dump(chain, f, indent=4)

def create_block(inventory_id, message, signature, public_key):
    chain = load_chain()
    previous_hash = hashlib.md5(json.dumps(chain[-1], sort_keys=True).encode()).hexdigest() if chain else "0"
    block = {
        "index": len(chain) + 1,
        "timestamp": str(datetime.utcnow()),
        "inventory_id": inventory_id,
        "message": message,
        "signature": signature,
        "public_key": public_key,
        "previous_hash": previous_hash
    }
    chain.append(block)
    save_chain(chain)
    return block

# Tkinter UI
def submit_transaction():
    inventory_id = inventory_var.get()
    message = message_entry.get()

    if not inventory_id or not message:
        messagebox.showwarning("Missing Input", "Please provide both Inventory and Message.")
        return

    inv = inventory_classes[inventory_id]
    m_hash = hash_message(message)
    public_key, private_key = generate_key(inv.p, inv.q, inv.e)
    signature = sign(m_hash, private_key[0], private_key[1])
    is_valid = verify(m_hash, signature, public_key[0], public_key[1])

    if is_valid:
        block = create_block(inventory_id, message, signature, public_key)
        messagebox.showinfo("Success", f"✅ Transaction signed and added to blockchain.\nBlock #{block['index']}")
    else:
        messagebox.showerror("Failed", "❌ Signature invalid. Block not added.")

# GUI Setup
root = tk.Tk()
root.title("Inventory Blockchain - PoA")

tk.Label(root, text="Select Inventory:").grid(row=0, column=0, padx=10, pady=10)
inventory_var = tk.StringVar()
inventory_dropdown = ttk.Combobox(root, textvariable=inventory_var, values=list(inventory_classes.keys()))
inventory_dropdown.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Transaction Message:").grid(row=1, column=0, padx=10, pady=10)
message_entry = tk.Entry(root, width=50)
message_entry.grid(row=1, column=1, padx=10, pady=10)

submit_button = tk.Button(root, text="Submit Transaction", command=submit_transaction)
submit_button.grid(row=2, column=0, columnspan=2, pady=20)

root.mainloop()
