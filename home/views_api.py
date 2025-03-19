from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Profile
from .helpers import *
from django.contrib.auth import authenticate, login


class LoginView(APIView):

    def post(self, request):
        response = {}
        response['status'] = 500
        response['message'] = 'Something went wrong'
        try:
            data = request.data

            if data.get('username') is None:
                response['message'] = 'key username not found'
                raise Exception('key username not found')

            if data.get('password') is None:
                response['message'] = 'key password not found'
                raise Exception('key password not found')

            check_user = User.objects.filter(
                username=data.get('username')).first()

            if check_user is None:
                response['message'] = 'invalid username , user not found'
                raise Exception('invalid username not found')

            if not Profile.objects.filter(user=check_user).first().is_verified:
                response['message'] = 'your profile is not verified'
                raise Exception('profile not verified')

            user_obj = authenticate(username=data.get('username'),
                                    password=data.get('password'))
            if user_obj:
                login(request, user_obj)
                response['status'] = 200
                response['message'] = 'Welcome'
            else:
                response['message'] = 'invalid password'
                raise Exception('invalid password')


        except Exception as e:
            print(e)

        return Response(response)


LoginView = LoginView.as_view()


class RegisterView(APIView):

    def post(self, request):
        response = {'status': 500, 'message': 'Something went wrong'}
        try:
            data = request.data

            username = data.get('username')
            password = data.get('password')

            if not username:
                response['message'] = 'Username is required'
                return Response(response)

            if not password:
                response['message'] = 'Password is required'
                return Response(response)

            # Check if user exists
            if User.objects.filter(username=username).exists():
                response['message'] = 'Username already taken'
                return Response(response)

            if User.objects.filter(email=username).exists():
                response['message'] = 'Email already registered'
                return Response(response)

            # Create user
            user_obj = User.objects.create_user(username=username, email=username, password=password)
            token = generate_random_string(20)

            # Set verified user
            Profile.objects.create(user=user_obj, token=token, is_verified=True)

            response['message'] = 'User created successfully'
            response['status'] = 200
        except Exception as e:
            print(e)
            response['message'] = str(e)

        return Response(response)

RegisterView = RegisterView.as_view()