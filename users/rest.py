from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from firebase_admin import auth
from rest_framework.permissions import IsAuthenticated

from django.views.generic import View
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout
from django.urls import reverse_lazy

from .serializer import LoginSocialSerializer,PictureSerializer
from .models import OpticUser,Account


class GoogleLRegisterView(APIView):
    serializer_class = LoginSocialSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        # si no es correcto mandamos un error
        serializer.is_valid(raise_exception=True)

        # recupermos el token
        id_token = serializer.data.get('token_id')

        # descincriptamos
        decode_token = auth.verify_id_token(id_token)

        email = decode_token['email']
        name = decode_token['name']

        optic = request.POST["optic"]

        usuario = OpticUser.objects.create(
            email=email,
            full_name=name,
            optic=optic,
            is_staff=True,

        )
        token = Token.objects.create(user=usuario)


        login(self.request, usuario)
        # creamos un token para administras nuestros usuarios.es opcional


        user_get = {
            'id': usuario.id,
            'email': usuario.email,
            'full_name': usuario.full_name,

        }
        return Response(
            {
                'token': token.key,
                'user': user_get,
            }
        )


class GoogleLoginValidateView(APIView):
    serializer_class = LoginSocialSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        # si no es correcto mandamos un error
        serializer.is_valid(raise_exception=True)

        # recupermos el token
        id_token = serializer.data.get('token_id')

        # descincriptamos
        decode_token = auth.verify_id_token(id_token)
        print("=============",decode_token)

        email = decode_token['email']
        name = decode_token['name']
        email_verified = decode_token['email_verified']

        try:
            usuario = Account.objects.get(username=email)
            login(self.request, usuario)
            user_get = {
                'id': usuario.id,
                'email': usuario.email,
                'full_name': usuario.full_name,

            }
        except Account.DoesNotExist:
            user_get = None

        return Response(
            {
                'user': user_get,
            }
        )


class LogoutUser(View):
    def get(self, request, *args, **kwargs):
        logout(self.request)
        return HttpResponseRedirect(reverse_lazy('users:login'))



class PictureUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class=PictureSerializer
    queryset=Account.objects.all()
