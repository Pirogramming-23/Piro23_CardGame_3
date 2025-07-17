from django.urls import path
from cardGame.views import index, game_start, game_mgp

urlpatterns = [
    path('', index, name='index'),
    path('game/', game_start, name='game_start'),
    path('game_mgp/', game_mgp, name='game_mgp'),
]