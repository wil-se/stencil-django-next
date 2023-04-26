from django.core.management.base import BaseCommand, CommandError
from lib.utils import *
from randomhandler.utils import *
import os
from randomhandler.models import HashChainIndex


chains = [
    {
        'name': '0',
        'seed': 'zero',
        'number': 1000
    },
    # {
    #     'name': '1',
    #     'seed': 'one',
    #     'number': 10000000
    # },
    # {
    #     'name': '2',
    #     'seed': 'two',
    #     'number': 10000000
    # },
    # {
    #     'name': '3',
    #     'seed': 'three',
    #     'number': 10000000
    # },
]

class Command(BaseCommand):
    help = 'Init Chains'

    def handle(self, *args, **options):
        base_path = os.getcwd()
        chains_dir = f'{base_path}/randomhandler/chains'
        for data in chains:
            chain = build_chain(data['number'], data['seed'])
            # verified = verify_chain(chain)
            if f'{data["seed"]}.chain' not in os.listdir(f'{chains_dir}/'):
                with open(f'{chains_dir}/{data["seed"]}.chain', 'w') as file:
                    file.write('\n'.join(reversed(chain)))

            try:
                HashChainIndex().save()
            except Exception as e:
                print(e)