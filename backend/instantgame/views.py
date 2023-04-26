from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from authentication.models import UserData
from datetime import datetime
import time
from rest_framework.response import Response
from django.conf import settings
from .models import CoinFlip


class CoinFlipView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        coin_flips = CoinFlip.objects.filter(player=request.user)
        return Response(coin_flips)
 
    def post(self, request):
        bet = request.data['bet']
        bet_amount = request.data['bet_amount']
        print(bet)
        print(bet_amount)
        coinflip = CoinFlip()
        coinflip.bet = bet
        coinflip.bet_amount = bet_amount
        coinflip.player = request.user
        coinflip.save()
        coinflip.flip_coin()
        return Response(coinflip.status)
    
    # def put(self, request):
    #     return Response()
    
    # def delete(self, request):
    #     return Response()