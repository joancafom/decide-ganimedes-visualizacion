from django.contrib.auth.backends import ModelBackend
from rest_framework.authtoken.models import Token
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

    def authenticate(self, request, username=None, password=None, **kwargs):
        
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            is_active = getattr(user, 'is_active', None)
            if user.check_password(password) and is_active:
                # data = {
                #      'email': username,
                #      'password': password                     
                #      }

        #     serializer = self.serializer_class(data=request.data,
        #                                    context={'request': request})
        # serializer.is_valid(raise_exception=True)
        # user = serializer.validated_data['user']
            # serializer_class = AuthTokenSerializer            
            # serializer = serializer_class(data=data, context={'request': request})
            # if serializer.is_valid():
            #     user = serializer.validated_data['user']
                token, created = Token.objects.get_or_create(user=user)
                token=token.key
                print(token)
#               token = mods.post('authentication', entry_point='/login/', json=data)
                request.session['auth-token'] = token
                return user
