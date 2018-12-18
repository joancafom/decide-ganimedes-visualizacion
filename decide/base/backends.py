from django.contrib.auth.backends import ModelBackend

from base import mods
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class AuthBackend(ModelBackend):
    '''
    This class makes the login to the authentication method for the django
    admin web interface.
    If the content-type is x-www-form-urlencoded, a requests is done to the
    authentication method to get the user token and this token is stored
    for future admin queries.
    '''

    def new_authenticate(self, request, email=None, password=None, **kwargs):
        if email is None:
            email = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(email)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and super.user_can_authenticate(user):
                u = user

                # only doing this for the admin web interface
                if u and request.content_type == 'application/x-www-form-urlencoded':
                    data = {
                        'email': email,
                        'password': password,
                    }
                    token = mods.post('authentication', entry_point='/login/', json=data)
                    request.session['auth-token'] = token['token']

                return u