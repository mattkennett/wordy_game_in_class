from django.urls import path

from wordy_game_app.views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('register', Register.as_view(), name='register'),
    path('set_password', SetPassword.as_view(), name='set_password'),
    path('puzzles', Puzzles.as_view(), name='puzzles'),
    path('not_found', NotFound.as_view(), name='not_found'),
]
