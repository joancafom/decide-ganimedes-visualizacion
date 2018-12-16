from django.urls import path, include,re_path
from . import views


urlpatterns = [
    path('', views.StoreView.as_view(), name='store'),
    path('users/voting/<int:voting_id>/', views.VotingView().as_view(), name='store'),
]
