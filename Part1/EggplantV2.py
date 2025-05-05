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

# 🍆 Hashing Function
def hash_message(message):
    return int(hashlib.md5(message.replace(" ", "").encode()).hexdigest(), 16)

# 🍆 RSA Key Generation
def generate_key(p, q, e):
    n = p * q
    phi = (p - 1) * q - (p - 1)
    d = pow(e, -1, phi)
    return (e, n), (d, n)

# 🍆 RSA Signing
def sign(m_hash, d, n):
    return pow(m_hash, d, n)

# 🍆 RSA Verification
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

# 🍆 Blockchain handling
CHAIN_FILE = "blockchainPP.json"

def load_chain():
    if os.path.exists(CHAIN_FILE):
        with open(CHAIN_FILE, "r") as f:
            return json.load(f)
    return []

def save_chain(chain):
    with open(CHAIN_FILE, "w") as f:
        json.dump(chain, f, indent=4)

# 🍆 Block creation with PoA
def create_block(inventory_id, data, signature, public_key):
    chain = load_chain()
    previous_hash = hashlib.md5(json.dumps(chain[-1], sort_keys=True).encode()).hexdigest() if chain else "0"
    block = {
        "index": len(chain) + 1,
        "timestamp": str(datetime.utcnow()),
        "inventory_id": inventory_id,
        "data": data,
        "signature": signature,
        "public_key": public_key,
        "previous_hash": previous_hash
    }
    chain.append(block)
    save_chain(chain)
    return block

# 🍆 PoA Consensus mock (accepts every block for simplicity)
def perform_poa_consensus():
    # In real PoA, multiple authorities would verify, here it's mocked
    print("🧠 PoA Consensus reached: Authorities approved the block.")
    return True

# 🍆 Submit Transaction Handler
def submit_transaction():
    inventory_id = inventory_var.get()
    item_id = item_id_entry.get().strip()
    quantity = quantity_entry.get().strip()
    price = price_entry.get().strip()
    location = location_var.get()

    # 🍆 Check inputs
    if not (inventory_id and item_id and quantity and price and location):
        messagebox.showwarning("Missing Input", "Please fill in all fields.")
        return

    # 🍆 Combine message from input fields
    serialized_msg = f"{item_id} {quantity} {price} {location}"
    print(f"📦 Serialized Message: {serialized_msg}")

    # 🍆 Get inventory keys
    inv = inventory_classes[inventory_id]
    m_hash = hash_message(serialized_msg)
    public_key, private_key = generate_key(inv.p, inv.q, inv.e)
    signature = sign(m_hash, private_key[0], private_key[1])
    is_valid = verify(m_hash, signature, public_key[0], public_key[1])

    # 🍆 Perform PoA and create block
    if is_valid and perform_poa_consensus():
        block = create_block(inventory_id, serialized_msg, signature, public_key)
        messagebox.showinfo("Success", f"✅ Transaction accepted by PoA.\nBlock #{block['index']}")
    else:
        messagebox.showerror("Failed", "❌ Signature invalid or PoA rejected block.")

# 🍆 GUI Setup
root = tk.Tk()
root.title("Inventory Blockchain - PoA 🍆")

# 🍆 Inventory Dropdown
tk.Label(root, text="Select Inventory:").grid(row=0, column=0, padx=10, pady=5)
inventory_var = tk.StringVar()
inventory_dropdown = ttk.Combobox(root, textvariable=inventory_var, values=list(inventory_classes.keys()))
inventory_dropdown.grid(row=0, column=1, padx=10, pady=5)

# 🍆 ItemID Entry
tk.Label(root, text="Item ID:").grid(row=1, column=0, padx=10, pady=5)
item_id_entry = tk.Entry(root, width=30)
item_id_entry.grid(row=1, column=1, padx=10, pady=5)

# 🍆 Quantity Entry
tk.Label(root, text="Quantity:").grid(row=2, column=0, padx=10, pady=5)
quantity_entry = tk.Entry(root, width=30)
quantity_entry.grid(row=2, column=1, padx=10, pady=5)

# 🍆 Price Entry
tk.Label(root, text="Price:").grid(row=3, column=0, padx=10, pady=5)
price_entry = tk.Entry(root, width=30)
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
