from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра пользователей"""

    class Meta:
        model = User
        fields = ['name', 'email', 'avatar', 'date_joined']


class UserModifySerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации и обновления профиля пользователя"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'password_confirm', 'avatar']

    def validate(self, data):
        if 'password' in data and data['password'] != data.get('password_confirm'):
            raise serializers.ValidationError({"password": "Пароли не совпадают."})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)

        if 'avatar' not in validated_data:
            validated_data['avatar'] = 'users/no_avatar.png'

        user = User(
            email=validated_data['email'],
            name=validated_data['name'],
            avatar=validated_data.get('avatar')
        )
        user.is_active = True
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        validated_data.pop('password_confirm', None)

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.name = validated_data.get('name', instance.name)
        instance.avatar = validated_data.get('avatar', instance.avatar)

        validated_data.pop('email', None)

        instance.save()
        return instance
