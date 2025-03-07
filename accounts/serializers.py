from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


# Kullanıcı bilgilerini serileştiren serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Django'nun dahili User modelini kullanır
        fields = ('id', 'username', 'email')  # API'ye döndürülecek alanlar
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        token = RefreshToken.for_user(user)
        return user, token

# Kullanıcı kayıt işlemleri için serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Django'nun dahili User modelini kullanır
        fields = ('id', 'username', 'email', 'password')  # Kullanıcı kaydı için gerekli alanlar
        extra_kwargs = {'password': {'write_only': True}}  # Şifre alanı yalnızca yazılabilir, API yanıtında gösterilmez

    def create(self, validated_data):
        # Yeni bir kullanıcı oluşturur ve şifreyi güvenli şekilde kaydeder
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user
