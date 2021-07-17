from rest_framework import serializers
from .models import Event, User, UserProfile, Summary, Date
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'date', 'description')


class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Summary
        fields = ('id', 'body', 'date')


class DateSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True, read_only=True)
    summarys = SummarySerializer(many=True, read_only=True)

    class Meta:
        ordering = ['-id']
        model = Date
        fields = ('user', 'date', 'summarys', 'events')
        extra_kwargs = {'summarys': {'required': False}, 'events': {'required': False}}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'first_name', 'last_name', 'address')


class UserRegistrationSerializer(serializers.ModelSerializer):

    profile = UserSerializer(required=False)

    class Meta:
        model = User
        fields = ('email', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(
            user_id=user.id,
            first_name=profile_data['first_name'],
            last_name=profile_data['last_name'],
            address=profile_data['address'],
        )
        return user


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return {
            'email': user.email,
            'token': jwt_token
        }
