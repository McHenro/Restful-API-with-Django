# from rest_framework import serializers

# class RegistrationSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = User
#         fields = [
#             "name",
#             "Email_Address",
#             "zipcode",
#             "Date_of_Birth",
#             "password",

#         ]

#         extra_kwargs = {"password": {"write_only": True}}
#         password = self.validated_data["password"]
#         account.set_password(password)
#         account.save()
#         return account


from rest_framework import serializers
from django.contrib.auth.models import User


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=50)
    first_name = serializers.CharField(max_length= 50)
    last_name = serializers.CharField(max_length= 50)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password','first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user