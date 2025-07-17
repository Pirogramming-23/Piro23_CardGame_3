from django.urls import path
from cardGame.views import index, game_start

urlpatterns = [
    path('', index, name='index'),
    path('game/', game_start, name='game_start'),
]