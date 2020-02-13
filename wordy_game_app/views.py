import os

from django.shortcuts import render
from django.views import View


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'wordy_game_app/index.html')

    def post(self, request, *args, **kwargs):
        user_form_input = request.POST.get('user_form_input', None)

        if not user_form_input:
            context = {
                'error': 'Must POST user_input',
            }
        else:
            context = {
                'input_from_user': user_form_input,
            }

        return render(request, 'wordy_game_app/index.html', context)