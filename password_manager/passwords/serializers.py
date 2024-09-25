from rest_framework import serializers
from .models import Password


class PasswordSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Password"""

    class Meta:
        model = Password
        fields = '__all__'

