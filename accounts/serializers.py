from rest_framework import serializers
from .models import CrudUser  # CrudUser modelinizi içe aktarıyoruz
from rest_framework_simplejwt.tokens import RefreshToken

# Kullanıcı bilgilerini serileştiren serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrudUser  # CrudUser modelini kullanıyoruz
        fields = ('id', 'username', 'email')  # API'ye döndürülecek alanlar
        extra_kwargs = {
            'password': {'write_only': True}  # Şifre alanını sadece yazılır yapıyoruz
        }

    # Eğer isterseniz create metodunu override edebilirsiniz, ancak listeleme gibi işlemlerde bu metot çağrılmayacak.
    def create(self, validated_data):
        user = CrudUser.objects.create_user(**validated_data)
        # Token üretimi gerekiyorsa, burada üretebilirsiniz; örneğin JWT token vs.
        token = RefreshToken.for_user(user)
        return user

# Kullanıcı kayıt işlemleri için serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrudUser  # CrudUser modelini kullanıyoruz
        fields = ('id', 'username', 'email', 'password')  # Kayıt için gerekli alanlar
        extra_kwargs = {'password': {'write_only': True}}  # Şifre sadece yazılır

    def create(self, validated_data):
        # Yeni bir kullanıcı oluşturur ve şifreyi güvenli şekilde kaydeder
        user = CrudUser.objects.create_user(**validated_data)
        return user
