from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    social_type = models.CharField(max_length=20, blank=True, null=True)  # google/naver/kakao
    point = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    number = models.IntegerField()
    is_used = models.BooleanField(default=False)


class Game(models.Model):
    attacker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attacker_games')
    defender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='defender_games')

    attacker_card = models.IntegerField()
    defender_card = models.IntegerField(null=True, blank=True, default=None)

    win_condition = models.CharField(max_length=10)  # 'high' or 'low'
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_games')

    point_change = models.IntegerField(null=True, blank=True, default=0)
    status = models.CharField(max_length=20)  # 'pending', 'finished'

    created_at = models.DateTimeField(auto_now_add=True)


class Ranking(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rank = models.IntegerField(null=True) 
    point = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)


class GameLog(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='logs')
    action = models.CharField(max_length=20)
    detail = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)