import hashlib
import ecdsa
import base58
from eth_keys import keys
import os


def generate_btc_address():
    # Generate private key (32 random bytes)
    private_key = os.urandom(32)
    
    # Derive public key using ECDSA (secp256k1)
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    public_key = b'\x04' + vk.to_string()  # Uncompressed public key
    
    # SHA-256 + RIPEMD-160 hashing
    sha256 = hashlib.sha256(public_key).digest()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256)
    pubkey_hash = ripemd160.digest()
    
    # Add Bitcoin network byte (0x00 for mainnet)
    network_byte = b'\x00'
    extended_hash = network_byte + pubkey_hash
    
    # Calculate checksum (double SHA-256)
    checksum = hashlib.sha256(hashlib.sha256(extended_hash).digest()).digest()[:4]
    
    # Final binary address
    binary_address = extended_hash + checksum
    
    # Encode in Base58
    btc_address = base58.b58encode(binary_address).decode('utf-8')
    
    return btc_address, private_key.hex()


def generate_eth_address():
    # Generate private key
    private_key_bytes = os.urandom(32)
    private_key = keys.PrivateKey(private_key_bytes)
    
    # Derive public key
    public_key = private_key.public_key
    
    # Ethereum address is the last 20 bytes of Keccak-256 hash of public key
    eth_address = public_key.to_checksum_address()
    
    return eth_address, private_key_bytes.hex()


def generate_bnb_address():
    # Same as Bitcoin, but with 'bnb' prefix and different hashing
    btc_address, private_key = generate_btc_address()
    
    # Convert to BNB format (starts with 'bnb1...')
    # (In reality, Binance uses bech32 encoding, but this is a simplified version)
    bnb_address = "bnb1" + base58.b58encode_check(b'\x00' + hashlib.new('ripemd160', hashlib.sha256(btc_address.encode()).digest()).digest()).decode('utf-8')[:39]
    
    return bnb_address, private_key

def generate_tron_address():
    # Similar to Bitcoin but starts with 'T'
    btc_address, private_key = generate_btc_address()
    tron_address = "T" + btc_address[1:]  # Simplified conversion
    return tron_address, private_key