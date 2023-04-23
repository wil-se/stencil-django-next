import hashlib
import logging
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import binascii
import base64
from pprint import PrettyPrinter
pp = PrettyPrinter()
from utils import *


class SeedManager:
    logger = None
    chain = []
    chain_index = 0

    def __init__(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        self.logger = logger
        self.chain = self.build_chain()

    def build_chain(self, number=300, seed='eeEsss2233sss'):
        hashed_seed = hash_text_SHA512(seed)
        chain = [hashed_seed]
        for i in range(number-1):
            digest = hash_text_SHA512(chain[i])
            chain.append(digest)
        return chain

    def verify_chain(self, chain):
        hash_index = len(chain)-1
        while hash_index > 0:
            if verify_hash_SHA512(chain[hash_index-1], chain[hash_index]):
                self.logger.info(f'{chain[hash_index-1]} -> {chain[hash_index]} OK')
                hash_index -= 1
            else:
                self.logger.error(f'{chain[hash_index-1]} -> {chain[hash_index]} ERROR')
                return False            
        return True

    def generate_number(self,
                        client_public_seed, 
                        client_private_seed, 
                        nonce='', 
                        round=''):
        client_signed_private_seed = sign_message_SHA256(client_private_seed)
        # convert client_signed_private_seed to HEX if necessary
        # client_signed_private_seed = client_signed_private_seed.hex()
        pre_computed_random_hash = self.chain[self.chain_index]
        self.chain_index += 1
        number = int(hash_text_SHA512(
            round+
            nonce+
            client_public_seed+
            client_private_seed+
            pre_computed_random_hash
            ), 16)
        client_signed_private_seed_base64_encoded = encode_base64(client_signed_private_seed)
        print(number)
        return (number, 
                client_signed_private_seed,
                client_signed_private_seed_base64_encoded,
                pre_computed_random_hash)

    def check_number(self, 
                     client_public_seed, 
                     client_private_seed, 
                     pre_computed_random_hash, 
                     nonce='', 
                     round=''):
        client_signed_private_seed = sign_message_SHA256(client_private_seed)
        number = hash_text_SHA512(
            round+
            nonce+
            client_public_seed+
            client_private_seed+
            pre_computed_random_hash
            )
        client_signed_private_seed_base64_encoded = encode_base64(client_signed_private_seed)
        print(number)
        return (number, 
                client_signed_private_seed,
                client_signed_private_seed_base64_encoded,
                pre_computed_random_hash)


    def flip_coin(self, client_public_seed='ciaone', client_private_seed='yoyoyo'):
        return self.generate_number(client_public_seed, client_private_seed)[0] % 2

    def dice_roll(self, client_public_seed='ciaone', client_private_seed='yoyoyo'):
        return self.generate_number(client_public_seed, client_private_seed)[0] % 6
        

