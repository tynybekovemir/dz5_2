from rest_framework import serializers
from apps.users.models import User

class UserUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'phone', 'age', 'direction')

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, write_only=True)
    password2 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'phone', 'age', 'direction', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password2': 'Пароли отличаются'})
        elif '+996' not in attrs['phone']:
            raise serializers.ValidationError({'phone': 'Введенный номер не соответствует стандартам КР (+996)'})
        elif len(attrs['password']) < 8 and len(attrs['password2']) < 8:
            raise serializers.ValidationError({'password_len': 'Длина пароля меньше 8'}) 
        return attrs

    def create(self, validate_data):
        user = User.objects.create(
            username=validate_data['username'],
            phone=validate_data['phone'],
            age=validate_data['age'],
            direction=validate_data['direction'],
            password=validate_data['password']
        )
        user.set_password(validate_data['password'])
        user.save()
        return user

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'phone', 'age', 'direction', 'password', 'password2')


