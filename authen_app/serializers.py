from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import    
# from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token
 
 
 
    
    
    # @api_view(["GET"])
    # @permission_classes([IsAuthenticated])
    # def User_logout(request):

    #     request.user.auth_token.delete()

    #     logout(request)

    #     return Response('User Logged out successfully')
    


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(
    write_only=True,
    required=True,
    min_length=4,
    
    style={'input_type': 'password', 'placeholder': 'Password'})
    validators=[validate_password]
    
    confirm_password= serializers.CharField(
    write_only=True,
    required=True,
    min_length=4,
    style={'input_type': 'password', 'placeholder': 'Password'})

    # password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    # confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'confirm_password', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user
    
    