from rest_framework import serializers
from .models import User

from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(
        max_length=127,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message="username already taken."
            )
        ],
    )
    email = serializers.EmailField(
        max_length=127,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message="email already registered."
            )
        ],
    )
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    birthdate = serializers.DateField(default=None, allow_null=True)
    is_employee = serializers.BooleanField(allow_null=True, default=False)
    is_superuser = serializers.BooleanField(read_only=True)
 
    def create(self, validated_data: dict):
        is_employee = validated_data.get('is_employee', False)
        if is_employee:
            validated_data['is_superuser'] = True
        else:
            validated_data['is_superuser'] = False
        return User.objects.create_user(**validated_data)
    
    def update(self, instance: User, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.birthdate = validated_data.get("birthdate", instance.birthdate)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.set_password(validated_data.get("password", instance.password))

        instance.save()

        return instance
