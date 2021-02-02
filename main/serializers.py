from rest_framework import serializers
from . import models


class LodgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lodger
        fields = ('name','age','sex','chosen_animal','main_feature')

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lodger
        fields = ('person_id','name','age','sex')

class SuitabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Suitability
        fields = ('mutual_interest','days_to_couple')

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Schedule
        fields = ('name','description','day_of_week','time_int')

class EscapeAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EscapeAttempt
        fields = ('person_id', 'date', 'success')

class CouplesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Couples
        fields = ['man_id','woman_id','date_of_creation','feature']