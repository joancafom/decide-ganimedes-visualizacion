from django.urls import include, path
from .views import obtain_auth_token

from .views import GetUserView, LogoutView, SignUpView, SaveUserView, nuevo_usuario


urlpatterns = [
    path('login/', obtain_auth_token),
    path('logout/', LogoutView.as_view()),
    path('getuser/', GetUserView.as_view()),
    path('signup/', SignUpView.as_view()),
    path('save/', SaveUserView.as_view()),
    path('nuevo-usuario/', nuevo_usuario),
]
