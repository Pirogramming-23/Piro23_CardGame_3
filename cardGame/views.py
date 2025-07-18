from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount
from .models import Game, User, Ranking
from cardGame import views


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



#게임 결과 처리
def process_game_result(game: Game):
    attacker = game.attacker
    defender = game.defender
    a_card = game.attacker_card
    d_card = game.defender_card
    win_type = game.win_condition  # 'high' or 'low'

    # 승패 결정
    if a_card == d_card:
        game.winner = None
        game.point_change = 0
    else:
        if (win_type == 'high' and a_card > d_card) or (win_type == 'low' and a_card < d_card):
            game.winner = attacker
            game.point_change = a_card
            attacker.point += a_card
            defender.point -= d_card
        else:
            game.winner = defender
            game.point_change = d_card
            defender.point += d_card
            attacker.point -= a_card

    game.status = 'completed'
    attacker.save()
    defender.save()
    game.save()

    update_ranking(attacker)
    update_ranking(defender)

#랭킹 갱신 함수 
def update_ranking(user: User):
    ranking, created = Ranking.objects.get_or_create(user=user)
    ranking.point = user.point

    ranking.save()

def ranking_view(request):
    rankings = Ranking.objects.select_related('user').order_by('-point')
    return render(request, 'ranking/ranking.html', {'rankings': rankings})