from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate


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


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )
    extra_kwargs = {'password': {'write_only': True,
                                 'help_text': 'Password should be at least 8 characters long.',
                                 'min_length': 8, },
                    'email': {'help_text': 'Email must be valid.',
                              }}

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            raise serializers.ValidationError({'Somethings wrong with the username or password '})

        attrs['user'] = user
        return attrs
