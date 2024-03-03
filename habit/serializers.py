from rest_framework import serializers

from habit.models import Habit
from . import validators


class HabitSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="email", read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Если related_habit заполнен, удаляем reward
        if representation['related_habit']:
            representation.pop('reward', None)
        # Если reward заполнен, удаляем related_habit
        elif representation['reward']:
            representation.pop('related_habit', None)
        # Если оба поля пустые, удаляем их из представления
        else:
            representation.pop('related_habit', None)
            representation.pop('reward', None)
        return representation

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [validators.RelatedHabitValidator('related_habit'),
                      validators.RelatedHabitAndRewardValidator('related_habit', 'reward'),
                      validators.LearnedHabitValidator('related_habit', 'is_learned', 'reward'),
                      validators.TimeSequenceValidator('related_habit', 'time')]


class HabitDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = '__all__'
