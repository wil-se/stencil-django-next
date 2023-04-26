from lib.utils import *


def build_chain(number=300, seed='eeEsss2233sss'):
    hashed_seed = hash_text_SHA512(seed)
    chain = [hashed_seed]
    for i in range(number-1):
        digest = hash_text_SHA512(chain[i])
        chain.append(digest)
    return chain

def verify_chain(chain):
    hash_index = len(chain)-1
    while hash_index > 0:
        if verify_hash_SHA512(chain[hash_index-1], chain[hash_index]):
            hash_index -= 1
        else:
            return False            
    return True