from django.shortcuts import render, redirect, get_object_or_404
from allauth.socialaccount.models import SocialAccount
from django.db.models import Q
from .models import Game, User, Ranking, Card
from cardGame import views
import random
from django.contrib.auth.decorators import login_required

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
    # 1부터 10까지의 숫자 중 랜덤으로 5개 카드 생성
    available_cards = random.sample(range(1, 11), 5)

    # 현재 사용자를 제외한 모든 User 객체
    other_users = User.objects.exclude(id=request.user.id)

    # user에 대해 이미 진행 중인 게임이 있는지 확인 (선택 사항)
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

def update_ranking(user: User):
    ranking, created = Ranking.objects.get_or_create(
        user=user,
        defaults={
            'point': user.point,
            'rank': None  # 또는 0
        }
    )

    # 이미 있었던 경우 → 점수 갱신
    if not created:
        ranking.point = user.point
        ranking.save()

    # 전체 랭킹 순위 재계산
    all_rankings = Ranking.objects.order_by('-point')
    for idx, r in enumerate(all_rankings, start=1):
        r.rank = idx
        r.save()



def ranking_view(request):
    rankings = Ranking.objects.select_related('user').order_by('-point')
    return render(request, 'ranking/ranking.html', {'rankings': rankings})

@login_required
def ranking_all(request):
    user = request.user
    rankings = Ranking.objects.select_related('user').order_by('-point')

    # 현재 유저가 수비자인 pending 게임이 있는지 확인
    pending_game = Game.objects.filter(defender=user, status='pending').first()

    if request.method == 'POST' and pending_game:
        # 수비자가 반격할 카드 선택
        selected_card = int(request.POST.get('selected_card'))
        pending_game.defender_card = selected_card

        # 승부 판정 및 랭킹 갱신
        process_game_result(pending_game)

        return redirect('ranking_all')

    # GET 요청 시
    context = {
        'rankings': rankings,
        'pending_game': pending_game,
        'defense_cards': random.sample(range(1, 11), 5) if pending_game else None,
    }

    return render(request, 'ranking/ranking_all.html', context)


@login_required
def game_mgp(request):
    if request.method == 'GET':
        is_counter_mode = request.GET.get('mode') == 'counter'

        if is_counter_mode:
            # 기존 세션에서 값 사용 (반격)
            opponent_card = request.session.get('opponent_card')
            is_higher_wins = request.session.get('is_higher_wins')
        else:
            # 일반 게임: 새로운 게임 시작
            opponent_card = random.randint(1, 10)
            is_higher_wins = random.choice([True, False])
            request.session['opponent_card'] = opponent_card
            request.session['is_higher_wins'] = is_higher_wins

        # 카드 5개 뽑기
        my_cards = random.sample(range(1, 11), 5)
        request.session['my_cards'] = my_cards
        request.session['game_state'] = 'selecting'

        context = {
            'my_cards': my_cards,
            'game_state': 'selecting',
            'win_condition': '숫자가 큰 사람이 이깁니다' if is_higher_wins else '숫자가 작은 사람이 이깁니다',
            'is_counterattack': is_counter_mode
        }

        return render(request, 'cardGame/game_mgp.html', context)

    elif request.method == 'POST':
        selected_card = int(request.POST.get('selected_card'))
        opponent_card = request.session.get('opponent_card')
        is_higher_wins = request.session.get('is_higher_wins')
        my_cards = request.session.get('my_cards')

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
