from django.contrib.auth import get_user_model
from rest_framework import serializers

from habit.serializers import HabitSerializer


class UserSerializer(serializers.ModelSerializer):
    """ View public user profile """
    public_habits = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'country', 'public_habits']

    def get_public_habits(self, instance):
        public_habits = instance.habits.filter(is_public=True)
        return HabitSerializer(public_habits, many=True).data


class UserProfileSerializer(serializers.ModelSerializer):
    """ View full user profile """
    password = serializers.CharField(write_only=True, required=True)
    habits = HabitSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = '__all__'
