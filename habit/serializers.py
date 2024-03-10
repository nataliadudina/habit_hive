from rest_framework import serializers

from habit.models import Habit
from . import validators


class HabitSerializer(serializers.ModelSerializer):
    frequency = serializers.IntegerField(default=1)
    estimated_time = serializers.IntegerField(default=120)
    user = serializers.SlugRelatedField(slug_field="email", read_only=True)

    def validate(self, data):
        frequency = data.get('frequency')
        estimated_time = data.get('estimated_time')

        # Frequency validation
        if frequency is not None:
            max_value = 7
            if frequency > max_value or frequency <= 0:
                raise serializers.ValidationError({
                    'frequency': "You should practice your habit at least once a week."
                })

        # Estimated_time validation
        if estimated_time is not None:
            max_value = 120
            if estimated_time > max_value:
                raise serializers.ValidationError({
                    'estimated_time': "Your new habit shouldn't take longer than 2 minutes."
                })

        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # If related_habit is filled, remove reward
        if representation['related_habit']:
            representation.pop('reward', None)
        # If reward is filled, remove related_habit
        elif representation['reward']:
            representation.pop('related_habit', None)
        # If both fields are empty, remove them from the view
        else:
            representation.pop('related_habit', None)
            representation.pop('reward', None)
        return representation

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [validators.RelatedHabitValidator('related_habit'),
                      validators.LearnedHabitValidator('related_habit', 'is_learned', 'reward'),
                      validators.RelatedHabitAndRewardValidator('related_habit', 'reward'),
                      validators.TimeSequenceValidator('related_habit', 'time')]


class HabitDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = '__all__'
