import json
import os
import hashlib
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from InventoryKeys import InventoryA, InventoryB, InventoryC, InventoryD

# 🍆 Inventory class map
inventory_classes = {
    'A': InventoryA,
    'B': InventoryB,
    'C': InventoryC,
    'D': InventoryD
}

# 🍆 Core RSA and Hashing Functions
def hash_message(message):
    return int(hashlib.md5(message.replace(" ", "").encode()).hexdigest(), 16)

def generate_public_key(p, q, e):
    n = p * q
    phi = (p - 1) * q - (p - 1)
    return (e, n)

def generate_private_key(p,q,e):
    n = p * q
    phi = (p - 1) * q - (p - 1)
    d = pow(e, -1, phi)
    return (d,n)

def sign(m_hash, d, n):
    return pow(m_hash, d, n)

def verify(m_hash, s, e, n):
    alt_m = pow(s, e, n)
    print(f"📝 Original message hash:     {m_hash}")
    print(f"🔁 Recovered hash from sig:   {alt_m}")
    return alt_m == m_hash

# 🍆 Blockchain and PoA Consensus
CHAIN_FILE = "blockchainzzz.json"

def load_chain():
    if os.path.exists(CHAIN_FILE):
        with open(CHAIN_FILE, "r") as f:
            return json.load(f)
    return []

def save_chain(chain):
    with open(CHAIN_FILE, "w") as f:
        json.dump(chain, f, indent=4)

def create_block(inventory_id,message, signature, public_key):
    chain = load_chain()
    previous_hash = hashlib.md5(json.dumps(chain[-1], sort_keys=True).encode()).hexdigest() if chain else "0"

    # In the new approach, there's no need to split the message into parts
    # because the message is just a serialized string now.
    item_parts = message.split(";")  # This will return a list of values, not key-value pairs.

    # Construct the block without needing to create a dictionary from the message
    block = {
        "index": len(chain) + 1,
        "timestamp": str(datetime.utcnow()),
        "inventory_id": inventory_id,
        "transaction": {
            "ItemID": item_parts[0],
            "Quantity": item_parts[1],
            "Price": item_parts[2],
            "Location": item_parts[3]
        },
        "signature": signature,
        "public_key": list(public_key),
        "previous_hash": previous_hash
    }

    chain.append(block)
    save_chain(chain)
    return block

def store_transaction(inventory_id, item_data):
    file_name = f"Inventory{inventory_id}_database.json"
    existing = []
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            existing = json.load(f)
    existing.append(item_data)
    with open(file_name, "w") as f:
        json.dump(existing, f, indent=4)

# 🍆 Tkinter UI Submit Logic
def submit_transaction():
    inventory_id = inventory_var.get()
    item_id = item_id_entry.get()
    quantity = quantity_entry.get()
    price = price_entry.get()
    location = location_var.get()

    if not inventory_id or not item_id or not quantity or not price or not location:
        messagebox.showwarning("Missing Input", "Please fill in all fields.")
        return

    message = f"{item_id};{quantity};{price};{location}"
    m_hash = hash_message(message)

    inv = inventory_classes[inventory_id]
    public_key= generate_public_key(inv.p, inv.q, inv.e)
    private_key = generate_private_key(inv.p,inv.q, inv.e)
    signature = sign(m_hash, private_key[0], private_key[1])

    # 🍆 Validators: All other inventories verify the signature
    validators = [inv_id for inv_id in inventory_classes if inv_id != inventory_id]
    for validator_id in validators:
        validator = inventory_classes[validator_id]
        validator_public_key = generate_public_key(validator.p, validator.q, validator.e)
        if not verify(m_hash, signature, public_key[0], public_key[1]):
            messagebox.showerror("PoA Rejected", f"❌ Transaction rejected by validator {validator_id}.")
            return
        pass

    item_data = {
        "ItemID": item_id,
        "Quantity": quantity,
        "Price": price,
        "Location": location
    }

    for inv_id in inventory_classes:
        store_transaction(inv_id, item_data)

    block = create_block(inventory_id, message, signature, public_key)
    messagebox.showinfo("Success", f"✅ Transaction accepted by PoA.\nBlock #{block['index']}")

# 🍆 GUI Setup
root = tk.Tk()
root.title("Inventory Blockchain - PoA")

# Inventory selection
tk.Label(root, text="Select Inventory:").grid(row=0, column=0, padx=10, pady=5)
inventory_var = tk.StringVar()
inventory_dropdown = ttk.Combobox(root, textvariable=inventory_var, values=list(inventory_classes.keys()))
inventory_dropdown.grid(row=0, column=1, padx=10, pady=5)

# Item ID
tk.Label(root, text="Item ID:").grid(row=1, column=0, padx=10, pady=5)
item_id_entry = tk.Entry(root)
item_id_entry.grid(row=1, column=1, padx=10, pady=5)

# Quantity
tk.Label(root, text="Quantity:").grid(row=2, column=0, padx=10, pady=5)
quantity_entry = tk.Entry(root)
quantity_entry.grid(row=2, column=1, padx=10, pady=5)

# Price
tk.Label(root, text="Price:").grid(row=3, column=0, padx=10, pady=5)
price_entry = tk.Entry(root)
price_entry.grid(row=3, column=1, padx=10, pady=5)

# Location
tk.Label(root, text="Location:").grid(row=4, column=0, padx=10, pady=5)
location_var = tk.StringVar()
location_dropdown = ttk.Combobox(root, textvariable=location_var, values=["A", "B", "C", "D"])
location_dropdown.grid(row=4, column=1, padx=10, pady=5)

# Submit button
submit_button = tk.Button(root, text="Submit Transaction", command=submit_transaction)
submit_button.grid(row=5, column=0, columnspan=2, pady=15)

root.mainloop()
