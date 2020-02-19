from django.shortcuts import render, redirect
from django.views import View

import wordy_game_app.models as wordy_models


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

class Register(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'wordy_game_app/register.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        password_verify = request.POST.get('password_verify', None)
        favorite_color = request.POST.get('favorite_color', None)

        if not username or not email or not password or not password_verify:
            context = {
                'error': 'Must Pass In Username, Email, Password, and Password Verify.'
            }
            return render(request, 'wordy_game_app/register.html', context=context)

        if not password == password_verify:
            context = {
                'error': 'Passwords did not match. Please try again.'
            }
            return render(request, 'wordy_game_app/register.html', context=context)

        if not username.isalnum():
            context = {
                'error': 'Username must be alphanumeric.'
            }
            return render(request, 'wordy_game_app/register.html', context=context)

        # user, created = wordy_models.WordyUser.objects.get_or_create()

        username_exists = wordy_models.WordyUser.objects.all().filter(
            username=username,
        ).count()

        if username_exists:
            context = {
                'error': 'Username already in use.'
            }
            return render(request, 'wordy_game_app/register.html', context=context)

        new_user = wordy_models.WordyUser(
            username=username,
            email=email,
            favorite_color=favorite_color,
        )
        new_user.set_password(password)
        new_user.save()

        return redirect('index')
