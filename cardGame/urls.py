from django.urls import path
from .views import index, game_start, create_game, game_mgp, ranking_view, ranking_all

urlpatterns = [
		path('ranking/', ranking_view, name='ranking'),
		path('ranking/all/', ranking_all, name='ranking_all'),
    path('', index, name='index'),
    path('game/start/', game_start, name='game_start'), # 게임시작
    path('game/create/', create_game, name='create_game'), # 게임생성 (카드 선택 및 상대방 공격)
    path('game_mgp/', game_mgp, name='game_mgp'),
    path('counterattack/', game_mgp, name='counterattack'),
]