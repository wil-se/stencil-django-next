from django.db import models, transaction


class HashChainIndex(models.Model):
    chain = models.CharField(default='0', unique=True)
    index = models.PositiveBigIntegerField(default=0, editable=False)

    def __str__(self) -> str:
        return f'{self.index}'
    
    def get_next_index(self, chain='0'):
        with transaction.atomic():
            chain = HashChainIndex.objects.get(chain=chain)
            chain.index += 1
            chain.save()
            return chain.index


class ExtractedNumber(models.Model):
    number = models.CharField(max_length=256)
    public_seed = models.CharField(max_length=128)
    private_seed = models.CharField(max_length=128)
    signed_private_seed_base64 = models.CharField(max_length=400)
    chain = models.CharField(max_length=16)
    index = models.PositiveBigIntegerField()

    def __str__(self):
        return f'{self.chain} {self.index} {self.number} {self.public_seed}'