from django import forms
from django.forms import ValidationError

from wordy_game_app.globals import raise_unexpected_error

import wordy_game_app.models as wordy_models
import wordy_game_app.validators as wordy_validators


class RegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=128,
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form_text_input'}),
        validators=[wordy_validators.NewUsernameValidator()],
    )
    favorite_color = forms.CharField(
        max_length=128,
        label='Favorite Color',
        required=False,
        # Leaving the widget off here to show the difference
    )

    def save(self):
        """
        This function creates and returns a new WordyUser instance from the Form data. The new WordyUser instance will
        have an unusable password
        :return: On Success: A new WordyUser instance with an unusable password
                 On Failure: Raises whichever error is caught
        """
        username = self.cleaned_data.get('username', None)
        favorite_color = self.cleaned_data.get('favorite_color', None)

        try:
            new_user = wordy_models.WordyUser(
                username=username,
                email='none@none.com',
                password='irrelevant',
                favorite_color=favorite_color,
            )
            new_user.set_unusable_password()
            new_user.save()

            return new_user
        except Exception as e:
            # We would never expect an error here because this function should only be called after checking to make
            # sure that the form is valid.
            raise_unexpected_error(e)


class PasswordForm(forms.Form):
    password = forms.CharField(
        max_length=255,
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form_text_input'}),
        validators=[wordy_validators.PasswordValidator()]
    )
    verify_password = forms.CharField(
        max_length=255,
        label='Verify',
        widget=forms.PasswordInput(attrs={'class': 'form_text_input'})
    )

    def clean(self):
        """
        This function validates a Form instance by ensuring that the new password matches the verification password.
        Note that the first thing this function does is call its parent class's clean() function. That call will cause
        the wordy_validators.PasswordValidator() to run on this Form's instance of 'password' because a new instance
        of that class is passed to the form variable's 'validators' argument.
        :return: On Success: None
                 On Failure: Raises ValidationError
        """
        cleaned_data = super().clean()

        password = cleaned_data.get('password', None)
        verify_password = cleaned_data.get('verify_password', None)

        if not password or not verify_password:
            raise ValidationError(
                'Invalid Password',
                code='invalid',
            )

        if not password == verify_password:
            raise ValidationError(
                'Passwords did not match',
                code='invalid',
            )

        '''
        Please notice at this point that I have access to my user's new password IN PLAIN TEXT. You can verify
        that by printing out "password" or "verify_password" to the console. Those variables hold whatever our
        user entered in the HTML form. 
        
        I'm pointing this out in this long comment to highlight one of the many important reasons that you
        should be using some sort of password manager. You really need to be using unique passwords for every single
        website account that you use and it's just not feasible to keep up with that many unique and strong passwords.
        
        You really can't trust a website to not have access to the plaintext of any password you use for authentication
        unless you can read the source code for the site and somehow verify that the precise copy of the source code
        you read is the actual code running on both the server and client. Even then, Ken Thompson taught us that we
        can't trust any software stack that we haven't written ourselves. It's really best to just assume that any
        website you use has access to the plaintext version of the password you use for that site. That's why you
        need to be sure that you never reuse passwords.
        
        As developers, we're going to act ethically and verify our users' passwords using methods that won't allow us 
        to actually learn the password. We also won't store that plaintext password anywhere. However, it's a good idea 
        to assume that any website you visit was developed by unethical black hats that want to steal everything you 
        own.
        '''
