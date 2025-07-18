from django.urls import path
from .views import *

urlpatterns = [
	    path('', index),
		path('ranking/', views.ranking_view, name='ranking'),
		path('ranking/all/', views.ranking_all, name='ranking_all'),
]