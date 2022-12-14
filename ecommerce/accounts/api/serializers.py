from rest_framework import serializers
from ..models import Account


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'name', 'password']
        # extra_kwargs = {
        #     'password': {'write_only'}
        # }

    # def create(self, validated_data):
    #     """
    #     Create and return a new `Account` instance, given the validated data.
    #     """
    #
    #     return Account.objects.create(**validated_data)
    def create(self, validated_data):
        account = Account(
            email=validated_data['email'],
            name=validated_data['name']
        )
        account.set_password(validated_data['password'])
        account.save()
        return account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'password']
