from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount
import random

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

def game_mgp(request):
    # 게임 시작
    if request.method == 'GET':
        # 새로운 게임 시작
        opponent_card = random.randint(1, 10)
        is_higher_wins = random.choice([True, False])
        
        # 내 카드 5개 뽑기 (중복 없음)
        all_numbers = list(range(1, 11))
        my_cards = random.sample(all_numbers, 5)
        
        # 세션에 저장
        request.session['opponent_card'] = opponent_card
        request.session['is_higher_wins'] = is_higher_wins
        request.session['my_cards'] = my_cards
        request.session['game_state'] = 'selecting'
        
        context = {
            'my_cards': my_cards,
            'game_state': 'selecting',
            'win_condition': '숫자가 큰 사람이 이깁니다' if is_higher_wins else '숫자가 작은 사람이 이깁니다'
        }
        
        return render(request, 'cardGame/game_mgp.html', context)
    
    elif request.method == 'POST':
        # 선택한 카드 처리
        selected_card = int(request.POST.get('selected_card'))
        
        # 세션에서 데이터 가져오기
        opponent_card = request.session.get('opponent_card')
        is_higher_wins = request.session.get('is_higher_wins')
        my_cards = request.session.get('my_cards')
        
        # 승부 판정
        if selected_card == opponent_card:
            result = '무승부!'
            result_class = 'draw'
            my_score = 0
            opponent_score = 0
        elif (is_higher_wins and selected_card > opponent_card) or (not is_higher_wins and selected_card < opponent_card):
            result = '승리!'
            result_class = 'win'
            my_score = selected_card
            opponent_score = -opponent_card
        else:
            result = '패배!'
            result_class = 'lose'
            my_score = -selected_card
            opponent_score = opponent_card
        
        # 게임 끝
        request.session['game_state'] = 'finished'
        
        context = {
            'my_cards': my_cards,
            'selected_card': selected_card,
            'opponent_card': opponent_card,
            'result': result,
            'result_class': result_class,
            'my_score': my_score,
            'opponent_score': opponent_score,
            'game_state': 'finished',
            'win_condition': '숫자가 큰 사람이 이깁니다' if is_higher_wins else '숫자가 작은 사람이 이깁니다'
        }
        
        return render(request, 'cardGame/game_mgp.html', context)
