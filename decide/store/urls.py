from django.urls import path, include,re_path
from . import views


urlpatterns = [
    path('', views.StoreView.as_view(), name='store'),
    re_path('^votings/(?P<voting_id>.+)/$', views.VotingView().as_view()),
]
