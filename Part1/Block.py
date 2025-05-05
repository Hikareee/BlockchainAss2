import time
import hashlib

class Block:
    def __init__(self, index, previous_hash, transaction_data, signature, public_key):
        self.index = index
        self.timestamp = time.time()
        self.transaction_data = transaction_data
        self.signature = signature
        self.public_key = public_key
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_content = f"{self.index}{self.timestamp}{self.transaction_data}{self.signature}{self.public_key}{self.previous_hash}"
        return hashlib.md5(block_content.encode()).hexdigest()

    def __repr__(self):
        return f"Block(Index={self.index}, Hash={self.hash[:10]}..., PrevHash={self.previous_hash[:10]}...)"
