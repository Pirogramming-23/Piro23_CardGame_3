from django.urls import path
from .views import index, game_start, create_game # game_start와 create_game 뷰 import

urlpatterns = [
    path('', index, name='index'),
    path('game/start/', game_start, name='game_start'), # 게임시작
    path('game/create/', create_game, name='create_game'), # 게임생성 (카드 선택 및 상대방 공격)
]