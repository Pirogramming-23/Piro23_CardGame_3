from django.contrib import admin
from .models import User, Card, Game, Ranking, GameLog

admin.site.register(User)
admin.site.register(Card)
admin.site.register(Game)
admin.site.register(Ranking)
admin.site.register(GameLog)
