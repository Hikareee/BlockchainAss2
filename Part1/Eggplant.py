# 🍆 Inventory Blockchain with PoA and Tkinter UI
import json
import os
import hashlib
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from InventoryKeys import InventoryA, InventoryB, InventoryC, InventoryD

# 👵️ Map Inventory IDs to their key classes
inventory_classes = {
    'A': InventoryA,
    'B': InventoryB,
    'C': InventoryC,
    'D': InventoryD
}

# 🍆 Hash the serialized transaction message
def hash_message(message):
    return int(hashlib.md5(message.replace(" ", "").encode()).hexdigest(), 16)

# 🍆 Generate RSA key pairs manually
def generate_key(p, q, e):
    n = p * q
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    return (e, n), (d, n)

# 🍆 Sign message using private key
def sign(m_hash, d, n):
    return pow(m_hash, d, n)

# 🍆 Verify signature using public key
def verify(m_hash, s, e, n):
    alt_m = pow(s, e, n)
    print(f"📜 Original message hash:     {m_hash}")
    print(f"🔁 Recovered hash from sig:   {alt_m}")
    return alt_m == m_hash

# 🍆 JSON file to simulate blockchain
CHAIN_FILE = "blockchainE.json"

def load_chain():
    if os.path.exists(CHAIN_FILE):
        with open(CHAIN_FILE, "r") as f:
            return json.load(f)
    return []

def save_chain(chain):
    with open(CHAIN_FILE, "w") as f:
        json.dump(chain, f, indent=4)

# 🍆 Create a new block
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

# 🍆 Simulated PoA consensus where all inventory IDs vote to accept or reject
# 👵️ In a real network, authorities sign blocks. Here, we simulate unanimous approval.
def poa_consensus(message):
    votes = []
    for inv_class in inventory_classes.values():
        pub, priv = generate_key(inv_class.p, inv_class.q, inv_class.e)
        h = hash_message(message)
        sig = sign(h, priv[0], priv[1])
        votes.append(verify(h, sig, pub[0], pub[1]))
    return all(votes)

# 🍆 Tkinter GUI logic to collect input and perform signing

def submit_transaction():
    inventory_id = inventory_var.get()
    item_id = item_id_entry.get()
    quantity = quantity_entry.get()
    price = price_entry.get()

    if not inventory_id or not item_id or not quantity or not price:
        messagebox.showwarning("Missing Input", "Please fill all fields.")
        return

    # 🍆 Serialize message
    message = f"{item_id} {quantity} {price}"
    m_hash = hash_message(message)

    inv = inventory_classes[inventory_id]
    public_key, private_key = generate_key(inv.p, inv.q, inv.e)
    signature = sign(m_hash, private_key[0], private_key[1])

    # 🍆 Run PoA consensus before accepting block
    if poa_consensus(message):
        block = create_block(inventory_id, message, signature, public_key)
        messagebox.showinfo("Success", f"🍆 Transaction accepted by PoA. Block #{block['index']}")

    else:
        messagebox.showerror("Rejected", "❌ Transaction not approved by consensus.")

# 🍆 GUI Setup
root = tk.Tk()
root.title("🍆 Inventory Blockchain - PoA")

# Inventory Dropdown
tk.Label(root, text="Select Inventory:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
inventory_var = tk.StringVar()
inventory_dropdown = ttk.Combobox(root, textvariable=inventory_var, values=list(inventory_classes.keys()))
inventory_dropdown.grid(row=0, column=1, padx=10, pady=5)

# ItemID Entry
tk.Label(root, text="Item ID:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
item_id_entry = tk.Entry(root)
item_id_entry.grid(row=1, column=1, padx=10, pady=5)

# Quantity Entry
tk.Label(root, text="Quantity:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
quantity_entry = tk.Entry(root)
quantity_entry.grid(row=2, column=1, padx=10, pady=5)

# Price Entry
tk.Label(root, text="Price:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
price_entry = tk.Entry(root)
price_entry.grid(row=3, column=1, padx=10, pady=5)

# Submit Button
submit_button = tk.Button(root, text="Submit Transaction", command=submit_transaction)
submit_button.grid(row=4, column=0, columnspan=2, pady=20)

root.mainloop()