import hashlib
import logging
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import binascii
import base64

def hash_text_SHA512(text):
    text_bytes = text.encode('utf-8')
    sha512_hash = hashlib.sha512()
    sha512_hash.update(text_bytes)
    hash_hex = sha512_hash.hexdigest()
    return hash_hex

def verify_hash_SHA512(text, hash_hex):
    text_hash = hash_text_SHA512(text)
    return text_hash == hash_hex

def sign_message_SHA256(message, private_key_path='private_key.pem'):        
    with open(private_key_path, 'r') as f:
        private_key = RSA.import_key(f.read())
    hash = SHA256.new(message.encode('utf-8'))
    signature = pkcs1_15.new(private_key).sign(hash)
    # return binascii.hexlify(signature).decode()
    return signature

def verify_signature_SHA256(message, signature, public_key_path='public_key.pem',):
    # signature = encode_signature_base64(signature)
    with open(public_key_path, 'r') as f:
        public_key = RSA.import_key(f.read())
    hash = SHA256.new(message.encode('utf-8'))
    try:
        pkcs1_15.new(public_key).verify(hash, signature)
        return True
    except (ValueError, TypeError):
        return False

def encode_base64(data: bytes) -> str:
    return base64.b64encode(data).decode('utf-8')

def decode_base64(encoded_data: str) -> bytes:
    return base64.b64decode(encoded_data)
