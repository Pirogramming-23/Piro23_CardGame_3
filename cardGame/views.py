from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount
from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount

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
    #records = Record.objects.all()
    context = {
        #'records': records,
        'username': request.user.username,
    }
    return render(request, 'cardGame/game-list.html', context=context)
