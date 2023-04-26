from django.core.management.base import BaseCommand, CommandError
from lib.utils import *
from randomhandler.utils import *
import os
from randomhandler.models import HashChainIndex
from randomhandler.tasks import generate_number


class Command(BaseCommand):
    help = 'Init Chains'

    def handle(self, *args, **options):
        number = generate_number.delay('abc', 'abc')
        res = number.get(timeout=2)
        print(res)
