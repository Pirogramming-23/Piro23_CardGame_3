from django.shortcuts import render, redirect, get_object_or_404
from allauth.socialaccount.models import SocialAccount
import random
from django.contrib.auth.decorators import login_required
from .models import User, Game, Card

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

@login_required
def game_start(request):
    #1부터 10까지의 숫자 중 랜덤으로 5개 카드 생성
    available_cards = random.sample(range(1, 11), 5)
    
    #현재 사용자를 제외한 모든 User 객체
    other_users = User.objects.exclude(id=request.user.id) 

    #user에 대해 이미 진행 중인 게임이 있는지 확인
    users_with_game_status = []
    for user in other_users:
        has_pending_game = Game.objects.filter(
            attacker=request.user,
            defender=user,
            status='pending'
        ).exists()
        users_with_game_status.append({
            'user': user,
            'has_pending_game': has_pending_game
        })

    context = {
        'available_cards': available_cards,
        'other_users_with_status': users_with_game_status,
    }
    return render(request, 'cardGame/game_nyc.html', context)

@login_required
def create_game(request):
    if request.method == 'POST':
        #POST 데이터에서 선택된 카드 번호와 수비자 ID 가져오기
        selected_card_number = request.POST.get('selected_card')
        defender_id = request.POST.get('defender')    
        #숫자로 변환 가능하고, 1~10 사이인지 확인
        try:
            selected_card_number = int(selected_card_number)
            if not (1 <= selected_card_number <= 10):
                #유효하지 않은 카드 숫자일 경우, game_start 페이지로 리다이렉트 또는 에러 메시지 표시
                return redirect('game_start')
        except (ValueError, TypeError):
            #숫자로 변환할 수 없는 경우 처리
            return redirect('game_start')

        #공격자 (현재 로그인한 사용자)
        attacker = request.user
        
        #수비자 (선택된 사용자)
        defender = get_object_or_404(User, id=defender_id)

        #게임 진행중이면 game_start 페이지로 리다이렉트
        if Game.objects.filter(attacker=attacker, defender=defender, status='pending').exists():
            return redirect('game_start')

        win_condition = random.choice(['high', 'low'])

        #game 객체 생성
        game = Game.objects.create(
            attacker=attacker,
            defender=defender,
            attacker_card=selected_card_number,
            win_condition=win_condition,
            status='pending', #대기 상태로 설정
        )
        
        return redirect('index')
    else:
        #post아니면 game_start 페이지로 리다이렉트
        return redirect('game_start')
