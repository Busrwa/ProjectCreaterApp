from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from django.views.generic import RedirectView
from rest_framework.permissions import IsAdminUser
from .models import CrudUser

# Token'ı blacklist'e eklemek için fonksiyon
def blacklist_token(token):
    token = AuthToken.objects.get(token=token)
    token.blacklist()

# Register API - Yeni kullanıcı kaydı yapar
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Kayıt sonrası dönecek kullanıcı verilerini UserSerializer ile düzenliyoruz
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]  # Knox token üretimi
        })

# Login API - Kullanıcı girişi yapar
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if user is None:
            token = request.data.get('token')
            blacklist_token(token)
            raise AuthenticationFailed('Kullanıcı bulunamadı veya yanlış şifre.')

        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

# Logout API - Kullanıcı çıkış yapar ve token'ı blacklist'e ekler
class LogoutAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        token = request.auth
        blacklist_token(token)
        return Response({"message": "Başarıyla çıkış yapıldı."})

# RedirectView örneği
class ProjectCreaterRedirectView(RedirectView):
    url = '/some-url/'

# Kullanıcı listeleme (Sadece Admin)
class UserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = CrudUser.objects.all()  # CrudUser üzerinden tüm kullanıcıları çekiyoruz
        print(users.count())  # Konsolda toplam kayıt sayısını görebilirsiniz
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

# Kullanıcı güncelleme (Sadece Admin)
class UserUpdateView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        try:
            user = CrudUser.objects.get(id=pk)
        except CrudUser.DoesNotExist:
            return Response({"error": "Kullanıcı bulunamadı."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Kullanıcı silme (Sadece Admin)
class UserDeleteView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        try:
            user = CrudUser.objects.get(id=pk)
        except CrudUser.DoesNotExist:
            return Response({"error": "Kullanıcı bulunamadı."}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({"message": "Kullanıcı başarıyla silindi."})
