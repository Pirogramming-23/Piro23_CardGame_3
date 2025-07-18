from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount
from .models import Game, User
from django.db.models import Q

def index(request):
    user_data = None
    if request.user.is_authenticated:
        try:
            social = SocialAccount.objects.get(user=request.user)
            user_data = {
                'username': request.user.username,
                'email': social.extra_data.get('email'),
                'google_id': social.uid,
            }
        except SocialAccount.DoesNotExist:
            pass

    return render(request, 'cardGame/index.html', {'user_data': user_data})

def game_start(request):
    if not request.user.is_authenticated:
        return redirect('/')

    return render(request, 'cardGame/game.html')

def game_list(request):
    social = SocialAccount.objects.get(user=request.user)
    games = Game.objects.filter(Q(attacker=request.user) | Q(defender=request.user)).select_related('attacker', 'defender', 'winner').order_by('-created_at')
    context = {
        'username': request.user.username,
        'games' : games,
    }
    return render(request, 'cardGame/game-list.html', context=context)

def cancel_game(request, pk):
    game = Game.objects.get(id=pk)
    game.delete()
    return redirect('game_list')

def counter_attack(request):
    # 반격
    pass

def start_new_game(request):
    # 새로운 게임
    pass

def game_detail(request, pk):
    game = Game.objects.get(id=pk)
    context = {'game': game}
    return render(request, 'cardGame/game-detail.html', context=context)