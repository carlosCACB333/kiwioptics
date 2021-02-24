from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from firebase_admin import auth
from .serializer import LoginSocialSerializer
from .models import OpticUser


class GoogleLoginView(APIView):
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
        avatar = decode_token['picture']
        verified = decode_token['email_verified']

        print("========================")
        print(decode_token)
        for i,valor in decode_token.items():
            print(i+"==="+str(valor))

        # usuario, created = OpticUser.objects.get_or_create(
        #     email=email,
        #     defaults={
        #         'full_name': name,
        #         'email': email,
        #         'is_active': True,
        #     }
        #
        # )
        #
        # login(self.request, usuario)
        # # creamos un token para administras nuestros usuarios.es opcional
        # if created:
        #     token = Token.objects.create(user=usuario)
        # else:
        #     token = Token.objects.get(user=usuario)
        #
        # user_get = {
        #     'id': usuario.pk,
        #     'email': usuario.email,
        #     'full_name': usuario.full_name,
        #     'genero': usuario.genero,
        #     'date_birth': usuario.date_birth,
        #     'city': usuario.city,
        # }
        # return Response(
        #     {
        #         'token': token.key,
        #         'user': user_get,
        #     }
        # )

        return Response(
            {
                'user':email
            }
        )
