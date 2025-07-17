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