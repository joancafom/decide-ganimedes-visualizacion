from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from .serializers import UserSerializer
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404

from base import mods
from django.contrib.auth.models import User

class GetUserView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        return Response(UserSerializer(tk.user, many=False).data)


class LogoutView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        try:
            tk = Token.objects.get(key=key)
            tk.delete()
        except ObjectDoesNotExist:
            pass

        return Response({})


class SignUpView(TemplateView):
    template_name = 'authentication/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context


class SaveUserView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        User.objects.create_user(username,None, password)

        return Response({})
        