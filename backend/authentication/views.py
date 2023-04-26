from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from .models import UserData, NonceSignRequest
from rest_framework import status
from rest_framework import permissions
from django.conf import settings
from .tasks import *
from django.http import JsonResponse
from uuid import uuid4
from rest_framework_simplejwt.tokens import RefreshToken
from django.template.loader import render_to_string
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver


class IsAdmin(permissions.BasePermission):

    edit_methods = ("PUT", "POST", "CREATE", "DELETE")

    def has_permission(self, request, view):
        return request.user.role == 'Admin'

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return False


class RegisterView(APIView):
    def post(self, request):
        print(request.data)
        request.data._mutable = True
        request.data.pop('address')
        request.data._mutable = False
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        # id = self.request.query_params.get('id', None)
        obj = request.user
        request.data._mutable = True
        if 'password' in request.data.keys():
            obj.set_password(request.data['password'])
            request.data.pop('password')
            obj.save()
        if 'address' in request.data.keys():
            request.data.pop('address')
        request.data._mutable = False
        serializer = UserSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class NonceSignRequestView(APIView):

    def post(self, request):
        address = request.data.get('address', '')
        print()
        if request.user.pk:
            res = generate_nonce.delay(address, request.user.pk)
        else:
            res = generate_nonce.delay(address)
        result = res.get(timeout=2)
        return Response(result)


class NonceSignatureView(APIView):

    def post(self, request):
        address = request.data.get('address', '')
        nonce = request.data.get('nonce', '')
        signature = request.data.get('signature', '')
        print(address)
        print(nonce)
        print(signature)
        verified = False
        try:
            res = check_nonce.delay(nonce, address, signature)
            verified = res.get(timeout=2)
        except Exception as e:
            print(e)
        if verified:
            try:
                print(f'USER: {request.user.pk}')
            except Exception as e:
                print(f'ERROR {e}')
            if request.user.pk:
                request.user.address = address
                request.user.save()
                user = request.user
            else:
                # check if there's an user with that address
                user = None
                try:
                    user = UserData.objects.get(address=address)
                except:
                    pass
                # if not create a new user with that address
                if not user:
                    try:
                        serializer = UserSerializer(data={
                            'address': address,
                            'password': str(uuid4())[:20],
                            'email': f'{address}@missing.mail',
                        })
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
                        user = UserData.objects.get(id=dict(serializer.data)['id'])
                    except Exception as e:
                        print(e)

            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)
            return Response({
                'access_token': access,
                'refresh_token': str(refresh)
            })

        return Response(status=status.HTTP_401_UNAUTHORIZED)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    domain_name = ''
    try:
        context = {
            'current_user': reset_password_token.user,
            'username': reset_password_token.user.username,
            'email': reset_password_token.user.email,
            'reset_password_url': f"https://{domain_name}/resetpassword/confirm?token={reset_password_token.key}"
        }

        # render email text
        email_html_message = render_to_string('email/user_reset_password.html', context)
        email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

        msg = EmailMultiAlternatives(
            # title:
            "Password Reset",
            # message:
            email_plaintext_message,
            # from:
            f"noreply@{domain_name}",
            # to:
            [reset_password_token.user.email]
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()
    except Exception as e:
        print(e)

