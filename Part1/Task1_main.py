from Task_1_RSA_Manual import hash_message, generate_key, sign, verify

from Eggplant import InventoryA
from EggplantV2 import InventoryB
from EggplantV3 import InventoryC
from EggplantV4 import InventoryD

inventory_classes = {
    'A': InventoryA,
    'B': InventoryB,
    'C': InventoryC,
    'D': InventoryD
}

def main():
    inventory_id = input("Enter Inventory ID (A/B/C/D): ").strip().upper()
    if inventory_id not in inventory_classes:
        print("Invalid inventory ID")
        return

    msg = input("Enter the transaction message: ")
    m_hash = hash_message(msg)

    inv = inventory_classes[inventory_id]
    public_key, private_key = generate_key(inv.p, inv.q, inv.e)

    signature = sign(m_hash, private_key[0], private_key[1])
    print(f"\n🔐 Signature: {signature}")

    is_valid = verify(m_hash, signature, public_key[0], public_key[1])
    print("✅ Signature is valid!" if is_valid else "❌ Signature is invalid.")

if __name__ == "__main__":
    main()
