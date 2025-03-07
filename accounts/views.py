from rest_framework import generics, permissions  # Django Rest Framework'ün gerekli modüllerini içe aktarır
from rest_framework.response import Response  # API yanıtları döndürmek için
from knox.models import AuthToken  # Knox token tabanlı kimlik doğrulaması için AuthToken modeli
from .serializers import UserSerializer, RegisterSerializer  # Kullanıcı ve kayıt işlemleri için serializer'lar
from django.contrib.auth import login  # Django'nun kullanıcı girişi işlevi
from rest_framework.authtoken.serializers import AuthTokenSerializer  # Django'nun token doğrulama serializer'ı
from knox.views import LoginView as KnoxLoginView  # Knox Login API'si
from rest_framework.views import APIView  # Çıkış işlemi için
from rest_framework.exceptions import AuthenticationFailed  # Hatalı doğrulama için
from django.shortcuts import redirect
from django.views.generic import RedirectView


# Token'ı blacklist'e eklemek için fonksiyon
def blacklist_token(token):
    # Token'ı veritabanından al
    token = AuthToken.objects.get(token=token)
    # Token'ı blacklist'le
    token.blacklist()


# Register API - Yeni kullanıcı kaydı yapar
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer  # Kullanıcı kaydı için serializer'ı belirler

    def post(self, request, *args, **kwargs):
        # Kullanıcı kaydını gerçekleştirir ve kullanıcı verisini ve token'ı döndürür
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,  # Kullanıcı verisini döndürür
            "token": AuthToken.objects.create(user)[1]  # Kullanıcıya ait token'ı döndürür
        })


# Login API - Kullanıcı girişi yapar
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)  # Herkesin giriş yapmasına izin verir

    def post(self, request, format=None):
        # Token doğrulaması yaparak kullanıcıyı giriş yapmış sayar
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Eğer geçersiz bir kullanıcı varsa (örn. şifre yanlış), token'ı blacklist'le
        if user is None:
            token = request.data.get('token')
            blacklist_token(token)
            raise AuthenticationFailed('Kullanıcı bulunamadı veya yanlış şifre.')

        login(request, user)  # Kullanıcıyı giriş yaptırır
        return super(LoginAPI, self).post(request, format=None)  # Knox'un login metodunu çağırır


# Logout API - Kullanıcı çıkış yapar ve token'ı blacklist'e ekler
class LogoutAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        token = request.auth  # Mevcut token'ı al
        blacklist_token(token)  # Token'ı blacklist'e ekle
        return Response({"message": "Başarıyla çıkış yapıldı."})

# RedirectView örneği
class ProjectCreaterRedirectView(RedirectView):
    url = '/some-url/'  # Yönlendirmek istediğiniz URL'yi buraya yazın
