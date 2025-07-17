from django.urls import path
from .views import *

urlpatterns = [
	path('', index),
    path('game-list/', game_list, name='game_list'),
    
]