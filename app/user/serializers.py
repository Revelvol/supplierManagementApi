from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['name', 'email', 'password', 'is_active', 'is_staff', 'groups']
        read_only_fields = ['groups', 'is_active']
        extra_kwargs = {'password': {'write_only': True,
                                     'help_text': 'Password should be at least 8 characters long.',
                                     'min_length': 8, },
                        'email': {'help_text': 'Email must be valid.',
                                  }}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

