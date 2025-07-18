from django.urls import path
from .views import index, game_start, create_game, game_mgp, ranking_view, ranking_all

urlpatterns = [
	path('', index, name="index"),
    path('game-list/', game_list, name='game_list'),
    path('game/<int:pk>/cancel/', cancel_game, name='cancel_game'),
    path('game/<int:pk>/counter-attack/', counter_attack, name='counter_attack'), # 후추 map_game로 변경될 항목
    path('game/<int:pk>/detail/', game_detail, name='game_detail'),
    path('game/new/', start_new_game, name='start_new_game'), # 후추 실제 새로운 게임 시작으로 변경될 항목
		path('ranking/', ranking_view, name='ranking'),
		path('ranking/all/', ranking_all, name='ranking_all'),
    path('', index, name='index'),
    path('game/start/', game_start, name='game_start'), # 게임시작
    path('game/create/', create_game, name='create_game'), # 게임생성 (카드 선택 및 상대방 공격)
    path('game_mgp/', game_mgp, name='game_mgp'),
    path('counterattack/', game_mgp, name='counterattack'),
]