from Crypto.Hash import keccak

k = keccak.new(digest_bits=256)
id = k.update(b'deposit(uint256,uint256,bytes)').hexdigest()
method_id = id[:8]
print(id)
print(method_id)
