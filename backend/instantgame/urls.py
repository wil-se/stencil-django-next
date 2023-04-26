from django.urls import path
from .views import (
    CoinFlipView
    )


urlpatterns = [
    path('coin_flip', CoinFlipView.as_view(), name='coin_flip'),
]