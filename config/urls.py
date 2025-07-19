
# urls.py
from django.contrib import admin
from django.urls import path, include
from cardGame.views import index, game_start, game_mgp

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('cardGame/', include('cardGame.urls')),
    path('accounts/', include('allauth.urls')),
    path('game/start/', game_start),
    path('game_mgp/', game_mgp, name='game_mgp')
]
