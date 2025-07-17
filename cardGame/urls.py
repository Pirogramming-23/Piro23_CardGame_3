from django.urls import path
from cardGame.views import index

urlpatterns = [
    path('', index, name='index'),
]