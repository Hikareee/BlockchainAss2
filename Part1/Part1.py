import json
import os
import hashlib
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime


# 🍆 Inventory class to store keys
class Inventory:
    def __init__(self, p, q, e):
        self.p = int(p)
        self.q = int(q)
        self.e = int(e)

# 🍆 Load inventory keys from individual files
def load_inventory_keys():
    inventory_classes = {}
    inventory_files = {
        'A': 'Part1/inventory_a_keys.txt',
        'B': 'Part1/inventory_b_keys.txt',
        'C': 'Part1/inventory_c_keys.txt',
        'D': 'Part1/inventory_d_keys.txt'
    }
    
    for inv_id, file_path in inventory_files.items():
        try:
            with open(file_path, "r") as f:
                keys = {}
                for line in f:
                    line = line.strip()
                    if line:
                        key, value = line.split('=')
                        keys[key] = value
                
                # Log the keys being read
                log_text.insert(tk.END, f"\n📖 Reading keys for Inventory {inv_id}:\n")
                log_text.insert(tk.END, f"   p: {keys.get('p', 'Not found')}\n")
                log_text.insert(tk.END, f"   q: {keys.get('q', 'Not found')}\n")
                log_text.insert(tk.END, f"   e: {keys.get('e', 'Not found')}\n")
                
                if not all(k in keys for k in ['p', 'q', 'e']):
                    log_text.insert(tk.END, f"⚠️ Warning: Missing keys for Inventory {inv_id}\n")
                    continue
                    
                inventory_classes[inv_id] = Inventory(
                    keys['p'],
                    keys['q'],
                    keys['e']
                )
                log_text.insert(tk.END, f"✅ Successfully loaded keys for Inventory {inv_id}\n")
        except FileNotFoundError:
            log_text.insert(tk.END, f"⚠️ Error: Could not find keys file for Inventory {inv_id}\n")
        except Exception as e:
            log_text.insert(tk.END, f"⚠️ Error loading keys for Inventory {inv_id}: {str(e)}\n")
    
    if not inventory_classes:
        log_text.insert(tk.END, "❌ Error: No inventory keys were loaded successfully!\n")
    else:
        log_text.insert(tk.END, f"\n✨ Successfully loaded {len(inventory_classes)} inventory keys\n")
    
    return inventory_classes

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

def consensus(original_hash, recovered_hashes):
    log_text.insert(tk.END, "\n🔍 Starting consensus validation...\n")
    all_valid = True

    for idx, recovered_hash in enumerate(recovered_hashes):
        log_text.insert(tk.END, f"🔍 Authority Validator:\n")
        log_text.insert(tk.END, f"   Original Hash:    {original_hash}\n")
        log_text.insert(tk.END, f"   Recovered Hash:   {recovered_hash}\n")

        if recovered_hash != original_hash:
            log_text.insert(tk.END, f"❌ Authority Validator validation FAILED.\n")
            all_valid = False
        else:
            log_text.insert(tk.END, f"✅ Authority Validator validation PASSED.\n")

    if all_valid:
        log_text.insert(tk.END, "\n✨ Consensus mechanism success.\n")
        print("Consensus mechanism success")
    else:
        log_text.insert(tk.END, "\n❌ Consensus mechanism failed.\n")
        print("Consensus mechanism failed")

    return all_valid

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
    # Clear previous log
    log_text.delete(1.0, tk.END)
    location = location_var.get()  # Updated variable name
    item_id = item_id_entry.get()
    quantity = quantity_entry.get()
    price = price_entry.get()

    if not location or not item_id or not quantity or not price:
        messagebox.showwarning("Missing Input", "Please fill in all fields or else it won't work.")
        return

    log_text.insert(tk.END, f"🔍 Starting transaction process...\n")
    log_text.insert(tk.END, f"📝 Selected Location: {location}\n")
    log_text.insert(tk.END, f"📂 Reading keys from inventory_{location.lower()}_keys.txt\n")
    
    message = f"{item_id};{quantity};{price};{location}"
    m_hash = hash_message(message)
    log_text.insert(tk.END, f"🔐 Original Message Hash: {m_hash}\n")

    # Get the signing inventory's keys
    inv = inventory_classes[location]
    log_text.insert(tk.END, f"🔑 Generating keys for {location}...\n")
    public_key = generate_public_key(inv.p, inv.q, inv.e)
    private_key = generate_private_key(inv.p, inv.q, inv.e)
    log_text.insert(tk.END, f"🔑 Public key: (e={public_key[0]}, n={public_key[1]})\n")
    
    signature = sign(m_hash, private_key[0], private_key[1])
    log_text.insert(tk.END, f"✍️ Signature generated with hash and keys: {signature}\n")

    # 🍆 Validators: All other inventories verify the signature
    log_text.insert(tk.END, "\n🔍 Starting verification process...\n")
    # Get all validators (all inventories except the signing one)
    validators = ['A', 'B', 'C', 'D']
    validators.remove(location)
    log_text.insert(tk.END, f"👥 Validators for this transaction: {', '.join(validators)}\n")
    
    all_valid = True
    
    for validator_id in validators:
        log_text.insert(tk.END, f"\n🔍 Validator {validator_id} checking signature...\n")
        log_text.insert(tk.END, f"📂 Reading keys from inventory_{validator_id.lower()}_keys.txt\n")
        
        if validator_id not in inventory_classes:
            log_text.insert(tk.END, f"❌ Error: Validator {validator_id} keys not found!\n")
            all_valid = False
            break
            
        validator = inventory_classes[validator_id]
        validator_public_key = generate_public_key(validator.p, validator.q, validator.e)
        
        # Calculate recovered hash
        recovered_hash = pow(signature, public_key[0], public_key[1])
        is_valid = verify(m_hash, signature, public_key[0], public_key[1])
        
        log_text.insert(tk.END, f"📊 Hash Comparison:\n")
        log_text.insert(tk.END, f"   Original Hash:    {m_hash}\n")
        log_text.insert(tk.END, f"   Recovered Hash:   {recovered_hash}\n")
        log_text.insert(tk.END, f"✅ Validator {validator_id} verification: {'PASSED' if is_valid else 'FAILED'}\n")
        
        if not is_valid:
            all_valid = False
            break

    if not all_valid:
        log_text.insert(tk.END, "\n❌ Transaction rejected by validators.\n")
        messagebox.showerror("PoA Rejected", f"❌ Transaction rejected by validators.")
        return

    item_data = {
        "ItemID": item_id,
        "Quantity": quantity,
        "Price": price,
        "Location": location
    }
    concensus = consensus(m_hash, [recovered_hash for _ in validators])
    log_text.insert(tk.END, "\n💾 Storing transaction in all inventories...\n")
    for inv_id in ['A', 'B', 'C', 'D']:  # Store in all inventories
        store_transaction(inv_id, item_data)
        log_text.insert(tk.END, f"✅ Stored in {inv_id}\n")
    if concensus == True:
        block = create_block(location, message, signature, public_key)  # Updated parameter
        log_text.insert(tk.END, f"\n✨ Transaction complete! Block #{block['index']} created.\n")
        messagebox.showinfo("Success", f"✅ Transaction accepted by PoA.\nBlock #{block['index']}")

# 🍆 GUI Setup
root = tk.Tk()
root.title("Inventory Blockchain - PoA")

# Create main frame
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Input fields frame
input_frame = ttk.LabelFrame(main_frame, text="Transaction Details", padding="5")
input_frame.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

# Log frame
log_frame = ttk.LabelFrame(main_frame, text="Process Log", padding="5")
log_frame.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

# Log text widget
log_text = scrolledtext.ScrolledText(log_frame, width=60, height=30)
log_text.grid(row=0, column=0, padx=5, pady=5)

# Load inventory keys first
log_text.insert(tk.END, "🔍 Loading inventory keys...\n")
inventory_classes = load_inventory_keys()

# Item ID
ttk.Label(input_frame, text="Item ID:").grid(row=1, column=0, padx=5, pady=5)
item_id_entry = ttk.Entry(input_frame)
item_id_entry.grid(row=1, column=1, padx=5, pady=5)

# Quantity
ttk.Label(input_frame, text="Quantity:").grid(row=2, column=0, padx=5, pady=5)
quantity_entry = ttk.Entry(input_frame)
quantity_entry.grid(row=2, column=1, padx=5, pady=5)

# Price
ttk.Label(input_frame, text="Price:").grid(row=3, column=0, padx=5, pady=5)
price_entry = ttk.Entry(input_frame)
price_entry.grid(row=3, column=1, padx=5, pady=5)

# Location
ttk.Label(input_frame, text="Location:").grid(row=4, column=0, padx=5, pady=5)
location_var = tk.StringVar()
location_dropdown = ttk.Combobox(input_frame, textvariable=location_var, values=["A", "B", "C", "D"])
location_dropdown.grid(row=4, column=1, padx=5, pady=5)

# Submit button
submit_button = ttk.Button(input_frame, text="Submit Transaction", command=submit_transaction)
submit_button.grid(row=5, column=0, columnspan=2, pady=10)

# Configure grid weights
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(0, weight=1)

root.mainloop()
