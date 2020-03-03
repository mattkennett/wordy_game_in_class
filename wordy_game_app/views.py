from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from wordy_game_app.globals import raise_unexpected_error, VIEW_DECORATORS
from wordy_game_app.model_functions import credentials_are_valid

import wordy_game_app.forms as wordy_forms
import wordy_game_app.models as wordy_models


class Index(View):
    def get(self, request, *args, **kwargs):
        """
        This function returns the template site/wordy_game.html as a response to an HTTP GET request
        :param request: Django Request object
        :param args: Python argument list
        :param kwargs: Python kword argument dictionary
        :return: HTTP response object created by rendering the request through the template
        """
        return render(request, 'wordy_game_app/site/wordy_game.html')


class Register(View):
    form_class = wordy_forms.RegistrationForm

    def __init__(self):
        # Set registration_form for this instance to a new (and empty) instance of the
        # appropriate Form class for this View
        self.registration_form = self.form_class()

    def get(self, request, *args, **kwargs):
        # At this point, self.registration_form is a new instance of our form class and
        # we simply need to pass it to our template for rendering. We do that using a
        # context variable.
        context = {
            'registration_form': self.registration_form,
        }
        return render(request, 'wordy_game_app/user_management/register.html', context)

    def post(self, request, *args, **kwargs):
        # Set registration_form for this instance to a new instance of the appropriate
        # Form class for this View based on the form that was POSTed to this function
        self.registration_form = self.form_class(request.POST)

        if not self.registration_form.is_valid():
            context = {
                'registration_form': self.registration_form,
            }
            return render(request, 'wordy_game_app/user_management/register.html', context)

        new_user = self.registration_form.save()
        request.session['new_username'] = new_user.username
        return redirect('set_password')


class SetPassword(View):
    form_class = wordy_forms.PasswordForm

    def __init__(self):
        self.password_form = self.form_class()

    def get(self, request, *args, **kwargs):
        """
        This function checks to see if a valid user_object can be created from a request and returns a template
        rendered with a new PasswordForm if so
        :param request: Django Request object- request.SESSION['new_username'] must be a valid new username
        :param args: ~not used~
        :param kwargs: ~not used~
        :return: On Success: New PasswordForm rendered through a Django template
                 On Failure: redirect to 'not_found'
        """
        user_object = self.check_username(request)

        if not user_object:
            return redirect('not_found')

        context = {
            'password_form': self.password_form,
        }
        return render(request, 'wordy_game_app/user_management/set_password.html', context)

    def post(self, request, *args, **kwargs):
        """
        This function checks to see if a valid user_object can be created from a request and then checks the POSTed
        form for validity. If the form is valid, the user's password is changed, the user is logged in, and is finally
        redirected to 'puzzles'
        :param request: Django Request object- request.SESSION['new_username'] must be a valid new username
        :param args: ~not used~
        :param kwargs: ~not used~
        :return: On Success: logged-in redirect to 'puzzles'
                 On Failure: Error PasswordForm rendered through a Django template or redirect to 'not_found' if valid
                 username not passed to function
        """
        user_object = self.check_username(request)

        if not user_object:
            return redirect('not_found')

        self.password_form = self.form_class(request.POST)

        if not self.password_form.is_valid():
            context = {
                'password_form': self.password_form,
            }
            return render(request, 'wordy_game_app/user_management/set_password.html', context)

        user_object.set_password(self.password_form.cleaned_data['password'])
        user_object.save()

        # Log our user in before redirecting
        if credentials_are_valid(request, user_object.username, self.password_form.cleaned_data['password']):
            # This should always be the case because we just set the password for this user
            return redirect('puzzles')
        else:
            raise_unexpected_error(PermissionError('Invalid credentials'))

    @staticmethod
    def check_username(request):
        """
        This function checks that the session variable 'new_username' is set to a user that has an unusable password
        :param request: Django Request Object
        :return: On Success: the WordyUser instance where username=request.session['new_username']
                 On Failure: None
        """
        username = request.session.get('new_username', None)

        if not username:
            # TODO: Implement Django messaging service and then redirect to a site_error page that can consume
            # the messages passed to it. This will be much more useful than the simple not_found page that
            # has already been implemented.
            return None

        try:
            user_object = wordy_models.WordyUser.objects.get(
                username=username,
            )

            # The if/else statement below could be reduced to the following one-liner:
            # return user_object if not user_object.has_unusable_password() else None
            if user_object.has_usable_password():
                return None
            else:
                return user_object
        except wordy_models.WordyUser.DoesNotExist:
            # This exception isn't really an error. It just means that the username passed in does not exist in the
            # database. We don't need to stop the server for this issue, though we would probably want to log the
            # event in a production app.
            return None
        except Exception as e:
            raise_unexpected_error(e)


@method_decorator(VIEW_DECORATORS, name='dispatch')
class Puzzles(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'wordy_game_app/puzzles/list.html')


class NotFound(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'wordy_game_app/site/not_found.html')
