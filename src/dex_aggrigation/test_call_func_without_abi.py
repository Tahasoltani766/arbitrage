from Crypto.Hash import keccak

k = keccak.new(digest_bits=256)
id = k.update(b'burn(uint256)').hexdigest()
method_id = id[:8]
print(id)
print(method_id)
#mint(address,uint256)