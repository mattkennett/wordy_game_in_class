from django.shortcuts import render, redirect
from django.views import View

import wordy_game_app.models as wordy_models


class Index(View):
    '''
      This is how Matt wants us to comment!
    '''
    def get(self, request, *args, **kwargs):
        return render(request, 'wordy_game_app/site/wordy_game.html')


class Register(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'wordy_game_app/user_management/register.html')

    def post(self, request, *args, **kwargs):

        return redirect('index')
