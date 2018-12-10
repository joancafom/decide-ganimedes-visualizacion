from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from .models import User
from rest_framework.authtoken.models import Token

from base import mods


class AuthTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)
        u = User(email='voter1@gmail.com')
        u.set_password('test1234')
        u.save()

    def tearDown(self):
        self.client = None

    def test_login(self):
        data = {'email': 'voter1@gmail.com', 'password': 'test1234'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)

        token = response.json()
        self.assertTrue(token.get('token'))

    def test_login_fail(self):
        data = {'email': 'voter1@gmail.com', 'password': 'test1234'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_getuser(self):
        data = {'email': 'voter1@gmail.com', 'password': 'test1234'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 200)

        user = response.json()
        self.assertEqual(user['id'], 1)
        self.assertEqual(user['email'], 'voter1@gmail.com')

    def test_getuser_invented_token(self):
        token = {'token': 'invented'}
        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 404)

    def test_getuser_invalid_token(self):
        data = {'email': 'voter1@gmail.com', 'password': 'test1234'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Token.objects.filter(user__email='voter1@gmail.com').count(), 1)

        token = response.json()
        self.assertTrue(token.get('token'))

        response = self.client.post('/authentication/logout/', token, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 404)

    def test_logout(self):
        data = {'email': 'voter1@gmail.com', 'password': 'test1234'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Token.objects.filter(user__email='voter1@gmail.com').count(), 1)

        token = response.json()
        self.assertTrue(token.get('token'))

        response = self.client.post('/authentication/logout/', token, format='json')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Token.objects.filter(user__email='voter1@gmail.com').count(), 0)

#------------------------signup------------------------------
#sudo python3 ./manage.py test authentication.tests

    # def test_signup_new(self):
    #     data = {'username': 'new', 'password': 'new'}# this user must not exits in db
    #     response = mods.get('authentication/signup', json=data, response=True) #getting the html
    #     self.assertEqual(response.status_code, 200)  
    #     response = mods.post('authentication/login', json=data, response=True) #trying logging
    #     self.assertNotEqual(response.status_code, 200)  #user does not exit   
    #     response = mods.post('authentication/save', json=data, response=True) #saving user
    #     self.assertEqual(response.status_code, 200) 
    #     response = mods.post('authentication/login', json=data, response=True) #trying logging
    #     self.assertEqual(response.status_code, 200)  #user exits 

      

