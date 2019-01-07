from django.urls import include, path
from .views import Activate, obtain_auth_token, obtain_auth_token_rrss, GetUserView, LogoutView, signUp, contador, form_login

urlpatterns = [
    path('login/', obtain_auth_token),
    path('logout/', LogoutView.as_view()),
    path('getuser/', GetUserView.as_view()),
    path('signup/', signUp),   
    path('contador/', contador),
    path('activate/', Activate.as_view(), name='activate'),   
    path('obtain_auth_token_rrss/', obtain_auth_token_rrss),
    path('form-login/', form_login),
]
