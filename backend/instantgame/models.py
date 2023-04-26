from django.db import models
from randomhandler.tasks import generate_number
from randomhandler.models import ExtractedNumber


class InstantGameSettings(models.Model):
    name = models.CharField(max_length=16, default='default')
    reward_percentage = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.name} {self.reward_percentage}'


STATUS_CHOICES = (
    ('PENDING', 'Pending'),
    ('WON', 'Won'),
    ('LOST', 'Lost'),
)
class InstantGame(models.Model):
    extracted_number = models.ForeignKey('randomhandler.ExtractedNumber', null=True, on_delete=models.SET_NULL)
    player = models.ForeignKey('authentication.UserData', null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    bet_amount = models.FloatField(default=1)
    settings = models.ForeignKey('instantgame.InstantGameSettings', null=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        if not self.settings:
            self.settings = self.get_instant_game_settings()
        super(InstantGame, self).save(*args, **kwargs)
    
    def extract_number(self):
        res = generate_number.delay(
            self.player.public_seed,
            self.player.private_seed,
        )
        [number,
         extracted_pk,
         signed_private_seed_base64,
         hash
         ] = res.get(timeout=2)
        self.extracted_number = ExtractedNumber.objects.get(pk=extracted_pk)
        self.save()

    def get_instant_game_settings(self):
        try:
            settings = InstantGameSettings.objects.get(name='default')
        except:
            settings = InstantGameSettings()
            settings.save()
        return settings

    def __str__(self):
        return f'{self.player} {self.status}'


COIN_CHOICES = (
    ('NONE', 'None'),
    ('HEAD', 'Head'),
    ('TAILS', 'Tails'),
)
class CoinFlip(InstantGame):
    outcome = models.CharField(max_length=20, choices=COIN_CHOICES, default='NONE')
    bet = models.CharField(max_length=20, choices=COIN_CHOICES, default='NONE')
    
    def flip_coin(self):
        self.extract_number()
        if int(self.extracted_number.number) % 2 == 0:
            self.outcome = 'HEAD'
        else:
            self.outcome = 'TAILS'
        if self.outcome == self.bet:
            self.status = 'WON'
        else:
            self.status = 'LOST'
        self.save()