from django.urls import path
from . import views
from authentication.views import activate

urlpatterns = [
    path('base/', views.base, name="base"),
]
