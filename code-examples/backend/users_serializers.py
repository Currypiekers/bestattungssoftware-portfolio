from venv import logger
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from users.models import CustomUser, Company, EmailSettings, BankAccount
from django.contrib.auth.hashers import make_password
User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'username'  # Appropriately using the username as the identifier

    def validate(self, attrs):
        # First, call the parent class's validate method
        data = super().validate(attrs)
    
        # Adding custom data to the token response
        data.update({
            'user_id': self.user.id,
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'mitarbeiter_kuerzel': self.user.mitarbeiter_kuerzel,
            'role': getattr(self.user, 'role', None),  # Safer access using getattr
            'company_name': getattr(self.user.company, 'name', None) if self.user.company else None,
            'company_id': getattr(self.user.company, 'id', None) if self.user.company else None
        })
        return data
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username  # Changed 'email' to 'username'
        token['company_name'] = getattr(user.company, 'name', None) if user.company else None
        return token
    

class UserManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = 'username', 'email', 'password', 'mitarbeiter_kuerzel', 'role', 'company', 'status', 'first_name', 'last_name', 'id',
        extra_kwargs = {'password': {'write_only': True}}  # Important: Hide password in responses

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = CustomUser.objects.create(**validated_data) # Changed to create instead of create_user
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.password = make_password(password)
        # Update other fields
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.mitarbeiter_kuerzel = validated_data.get('mitarbeiter_kuerzel', instance.mitarbeiter_kuerzel)
        instance.role = validated_data.get('role', instance.role)
        instance.status = validated_data.get('status', instance.status)
        instance.company = validated_data.get('company', instance.company)
        instance.save()
        return instance

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'
        extra_kwargs = {'company': {'read_only': True}}  # Add this line
        
class CompanySerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(required=False)
    bank_accounts = BankAccountSerializer(many=True, read_only=True)  # Add this line

    class Meta:
        model = Company
        fields = '__all__'

class EmailSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSettings
        fields = '__all__'



