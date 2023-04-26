from backend.celery import app
from lib.utils import *
from .models import HashChainIndex, ExtractedNumber
import linecache
import os
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
logger.info('Adding {0} + {1}')

BASE_PATH = os.getcwd()
CHAINS_DIR = f'{BASE_PATH}/randomhandler/chains'

def get_chain_line_from_index(index, chain='zero'):
    return linecache.getline(f'{CHAINS_DIR}/{chain}.chain', index).strip()


@app.task
def generate_number(public_seed, 
                    private_seed, 
                    nonce='', 
                    round='',
                    chain='0'):
    
    signed_private_seed = sign_message_SHA256(
        private_seed,
        private_key_path=f'{CHAINS_DIR}/private_key.pem'
        )
    hash_chain = HashChainIndex()
    index = hash_chain.get_next_index(chain=chain)
    pre_computed_random_hash = get_chain_line_from_index(index, chain=chain)
    logger.info(f'index: {index} hashed line: {pre_computed_random_hash}\n\n')
    number = int(hash_text_SHA512(
        public_seed+
        private_seed+
        pre_computed_random_hash+
        round+
        nonce
        ), 16)
    extracted_number = ExtractedNumber()
    extracted_number.number = str(number)
    extracted_number.public_seed = public_seed
    extracted_number.private_seed = private_seed
    extracted_number.signed_private_seed_base64 = encode_base64(signed_private_seed)
    extracted_number.chain = hash_chain.chain
    extracted_number.index = index
    extracted_number.save()
    return [number,
            extracted_number.id,
            extracted_number.signed_private_seed_base64,
            pre_computed_random_hash
            ]

@app.task
def check_number(public_seed, 
                 private_seed, 
                 pre_computed_random_hash, 
                 nonce='', 
                 round=''):
    signed_private_seed = sign_message_SHA256(private_seed)
    number = hash_text_SHA512(
        round+
        nonce+
        public_seed+
        private_seed+
        pre_computed_random_hash
        )
    signed_private_seed_base64_encoded = encode_base64(signed_private_seed)
    print(number)
    return (number, 
            signed_private_seed,
            signed_private_seed_base64_encoded,
            pre_computed_random_hash)