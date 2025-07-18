from django.urls import path
from .views import *

urlpatterns = [
	    path('', index),
		path('ranking/', views.ranking_view, name='ranking'),
]