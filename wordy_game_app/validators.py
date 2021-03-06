import re

from django.contrib.auth.password_validation import CommonPasswordValidator, \
    MinimumLengthValidator, \
    NumericPasswordValidator, \
    UserAttributeSimilarityValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.forms import ValidationError

from wordy_game_app.globals import raise_unexpected_error

import wordy_game_app.models as wordy_models


class NewUsernameValidator(object):
    default_validators = [
        UnicodeUsernameValidator
    ]

    def __call__(self, *args, **kwargs):
        self.validate(args[0])

    def validate(self, username):
        try:
            for validator in self.default_validators:
                if not re.match(validator.regex, username):
                    raise ValidationError(
                        'Username %(username)s is invalid.',
                        code='invalid',
                        params={'username': username},
                    )
        except ValidationError as e:
            raise e
        except Exception as e:
            raise_unexpected_error(e)

        # At this point, the username *might* be valid. The check above doesn't ensure that the name is available-
        # it only ensures that the name has the correct form (it doesn't have whitespace and only uses allowed
        # characters).

        # Let's count the number of WordyUser objects that have this username. Since usernames must be unique,
        # this value will either be 0 or 1. That's super nice because we can just return the result of our
        # WordyUser count and Django will treat a 0 as "falsy" and any other number as "truthy."
        username_in_use = wordy_models.WordyUser.objects.all().filter(username=username).count()
        if username_in_use:
            raise ValidationError(
                'Username %(username)s is already in use. Please choose another. Or you can see this message again.'
                'I\'m a computer. I don\'t care.',
                params={'username': username},
                code='invalid',
            )

        # If we get to this point, we know the username is valid and available. Validate functions need to return
        # the validated value on success
        return username


class PasswordValidator(object):
    default_validators = [
        CommonPasswordValidator,
        MinimumLengthValidator,
        NumericPasswordValidator,
        UserAttributeSimilarityValidator,
    ]

    def __call__(self, *args, **kwargs):
        self.validate(args[0])

    def validate(self, password):
        try:
            for validator in self.default_validators:
                validator().validate(password)
        except ValidationError as e:
            raise e
        except Exception as e:
            raise_unexpected_error(e)
