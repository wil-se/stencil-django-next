from SeedManager import SeedManager
from random import randint
import base64
from utils import *
from pprint import PrettyPrinter
pp = PrettyPrinter()


seed_manager = SeedManager()

game = {
    'client_public_seed': 'abracadabra',
    'client_private_seed_signed': '',
    'client_private_seed_signed_base64_encoded': '',
    'pre_computed_random_hash': '',
    'client_private_seed': 'alakazam',
}


random_number = seed_manager.generate_number(
    game['client_public_seed'],
    game['client_private_seed']
    )

coin_flip = random_number[0] % 2
# print(f'coin flip: {coin_flip}')


game['client_private_seed_signed'] = random_number[1]
game['client_private_seed_signed_base64_encoded'] = random_number[2]
game['pre_computed_random_hash'] = random_number[3]

# print('AFTER GAME')
# pp.pprint(game)

# The user verifies that the client_private_seed_signed is client_private_seed
decoded = decode_base64(game['client_private_seed_signed_base64_encoded'])
verify = verify_signature_SHA256(game['client_private_seed'],
                                     decoded)
verify2 = verify_signature_SHA256(game['client_private_seed'],
                                     game['client_private_seed_signed'])
print(verify)
print(verify2)


hashed_check = hash_text_SHA512(
    game['client_public_seed']+
    game['client_private_seed']+
    game['pre_computed_random_hash']
)

# print(hashed_check)
number = int(hashed_check, 16)
print(number)
# print(number % 2)
