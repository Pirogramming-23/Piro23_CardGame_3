from django.urls import path
from .views import *

urlpatterns = [
	path('', index, name="index"),
    path('game-list/', game_list, name='game_list'),
    path('game/<int:pk>/cancel/', cancel_game, name='cancel_game'),
    path('game/<int:pk>/counter-attack/', counter_attack, name='counter_attack'), # 후추 map_game로 변경될 항목
    path('game/<int:pk>/detail/', game_detail, name='game_detail'),
    path('game/new/', start_new_game, name='start_new_game'), # 후추 실제 새로운 게임 시작으로 변경될 항목
]