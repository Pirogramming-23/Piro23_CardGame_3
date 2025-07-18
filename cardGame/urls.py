from django.urls import path
from .views import *

urlpatterns = [
	path('', index),
    path('game-list/', game_list, name='game_list'),
    path('game/<int:pk>/cancel/', cancel_game, name='cancel_game'),
    path('game/<int:pk>/counter-attack/', counter_attack, name='counter_attack'),
    path('game/<int:pk>/detail/', game_detail, name='game_detail'),
    path('game/new/', start_new_game, name='start_new_game'),
]