import json
import os
import hashlib
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from InventoryKeys import InventoryA, InventoryB, InventoryC, InventoryD

# 🍆 Inventory class mapping
inventory_classes = {
    'A': InventoryA,
    'B': InventoryB,
    'C': InventoryC,
    'D': InventoryD
}

# 🍆 JSON file path mapping
inventory_db_files = {
    'A': 'InventoryA.json',
    'B': 'InventoryB.json',
    'C': 'InventoryC.json',
    'D': 'InventoryD.json'
}

# 🍆 Blockchain path
CHAIN_FILE = "blockchainZ.json"

# 🍆 Hashing function
def hash_message(message):
    return int(hashlib.md5(message.replace(" ", "").encode()).hexdigest(), 16)

# 🍆 RSA key generation
def generate_key(p, q, e):
    n = p * q
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    return (e, n), (d, n)

# 🍆 Signing
def sign(m_hash, d, n):
    return pow(m_hash, d, n)

# 🍆 Verification
def verify(m_hash, s, e, n):
    alt_m = pow(s, e, n)
    print(f"✅ Verifying... Original Hash: {m_hash} | From Signature: {alt_m}")
    return alt_m == m_hash

# 🍆 Blockchain loader/saver
def load_chain():
    if os.path.exists(CHAIN_FILE):
        with open(CHAIN_FILE, "r") as f:
            return json.load(f)
    return []

def save_chain(chain):
    with open(CHAIN_FILE, "w") as f:
        json.dump(chain, f, indent=4)

# 🍆 PoA mock
def perform_poa_consensus():
    print("🧠 PoA Authorities have accepted the transaction.")
    return True

# 🍆 Append to all inventory JSON files
def update_inventory_databases(record):
    for inv_id, file_name in inventory_db_files.items():
        data = []
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                try:
                    data = json.load(f)
                except:
                    data = []
        data.append(record)
        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)

# 🍆 Create blockchain block
def create_block(inventory_id, transaction_data, signature, public_key):
    chain = load_chain()
    previous_hash = hashlib.md5(json.dumps(chain[-1], sort_keys=True).encode()).hexdigest() if chain else "0"
    block = {
        "index": len(chain) + 1,
        "timestamp": str(datetime.utcnow()),
        "inventory_id": inventory_id,
        "transaction": transaction_data,
        "signature": signature,
        "public_key": public_key,
        "previous_hash": previous_hash
    }
    chain.append(block)
    save_chain(chain)
    return block

# 🍆 Transaction Handler
def submit_transaction():
    inventory_id = inventory_var.get()
    item_id = item_id_entry.get().strip()
    quantity = quantity_entry.get().strip()
    price = price_entry.get().strip()
    location = location_var.get()

    if not (inventory_id and item_id and quantity and price and location):
        messagebox.showwarning("Missing Input", "Please fill in all fields.")
        return

    # 🍆 Create transaction data
    transaction_data = {
        "ItemID": item_id,
        "Quantity": quantity,
        "Price": price,
        "Location": location,
    }

    # 🍆 Hash and sign
    serialized_msg = f"{item_id} {quantity} {price} {location}"
    inv = inventory_classes[inventory_id]
    m_hash = hash_message(serialized_msg)
    public_key, private_key = generate_key(inv.p, inv.q, inv.e)
    signature = sign(m_hash, private_key[0], private_key[1])

    # 🍆 Verify and PoA
    if verify(m_hash, signature, public_key[0], public_key[1]) and perform_poa_consensus():
        update_inventory_databases(transaction_data)
        block = create_block(inventory_id, transaction_data, signature, public_key)
        messagebox.showinfo("Success", f"✅ Transaction accepted by PoA.\nBlock #{block['index']} added.")
    else:
        messagebox.showerror("Failed", "❌ Signature invalid or PoA rejected.")

# 🍆 GUI Setup
root = tk.Tk()
root.title("Inventory Blockchain System 🧱")

# 🍆 Inventory Dropdown
tk.Label(root, text="Select Inventory:").grid(row=0, column=0, padx=10, pady=5)
inventory_var = tk.StringVar()
inventory_dropdown = ttk.Combobox(root, textvariable=inventory_var, values=list(inventory_classes.keys()))
inventory_dropdown.grid(row=0, column=1, padx=10, pady=5)

# 🍆 ItemID
tk.Label(root, text="Item ID:").grid(row=1, column=0, padx=10, pady=5)
item_id_entry = tk.Entry(root)
item_id_entry.grid(row=1, column=1, padx=10, pady=5)

# 🍆 Quantity
tk.Label(root, text="Quantity:").grid(row=2, column=0, padx=10, pady=5)
quantity_entry = tk.Entry(root)
quantity_entry.grid(row=2, column=1, padx=10, pady=5)

# 🍆 Price
tk.Label(root, text="Price:").grid(row=3, column=0, padx=10, pady=5)
price_entry = tk.Entry(root)
price_entry.grid(row=3, column=1, padx=10, pady=5)

# 🍆 Location Dropdown
tk.Label(root, text="Location:").grid(row=4, column=0, padx=10, pady=5)
location_var = tk.StringVar()
location_dropdown = ttk.Combobox(root, textvariable=location_var, values=['A', 'B', 'C', 'D'])
location_dropdown.grid(row=4, column=1, padx=10, pady=5)

# 🍆 Submit Button
submit_button = tk.Button(root, text="Submit Transaction", command=submit_transaction)
submit_button.grid(row=5, column=0, columnspan=2, pady=20)

root.mainloop()
