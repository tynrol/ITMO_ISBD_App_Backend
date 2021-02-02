from django.db import models
from random import *
from datetime import *
import math
from django.db.models import F

class Children(models.Model):
    child_id = models.AutoField(primary_key=True)
    name = models.TextField()
    age = models.IntegerField()
    sex = models.TextField()

    class Meta:
        managed = False
        db_table = 'children'


class Couples(models.Model):
    couple_id = models.AutoField(primary_key=True)
    man = models.ForeignKey('Lodger', models.DO_NOTHING,related_name='man')
    woman = models.ForeignKey('Lodger', models.DO_NOTHING,related_name='woman')
    date_of_creation = models.DateTimeField(blank=True, null=True)
    feature = models.TextField(blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.date_of_creation is None:
            self.date_of_creation = datetime.now()
        feature1 = Lodger.objects.get(person_id=self.man_id).main_feature
        feature2 = Lodger.objects.get(person_id=self.woman_id).main_feature
        if random() > 0.5:
            feature1=feature2
        if self.feature is None:
            self.feature = feature1

    class Meta:
        managed = False
        db_table = 'couples'

    # def __str__(self):
    #     return '<%s: %s>' %(self.date_of_creation, self.feature)

class EscapeAttempt(models.Model):
    escape_id = models.AutoField(primary_key=True)
    person = models.ForeignKey('Lodger', models.DO_NOTHING)
    date = models.DateTimeField(blank=True, null=True)
    success = models.BooleanField(blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.date is None:
            self.date = datetime.now()

    class Meta:
        managed = False
        db_table = 'escape_attempt'


class Escaped(models.Model):
    escaped_id = models.AutoField(primary_key=True)
    escape = models.ForeignKey(EscapeAttempt, models.DO_NOTHING)
    days_left = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'escaped'


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    schedule = models.ForeignKey('Schedule', models.DO_NOTHING, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    event = models.TextField()
    mood_change = models.TextField()

    class Meta:
        managed = False
        db_table = 'event'


class Family(models.Model):
    family_id = models.AutoField(primary_key=True)
    couple = models.ForeignKey(Couples, models.DO_NOTHING)
    date = models.DateTimeField(blank=True, null=True)
    child = models.OneToOneField(Children, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'family'




class Lodger(models.Model):
    person_id = models.AutoField(primary_key=True)
    name = models.TextField()
    age = models.IntegerField(blank=True, null=True)
    sex = models.TextField()
    chosen_animal = models.TextField()
    main_feature = models.TextField()
    arrival_date = models.DateTimeField(blank=True, null=True)
    sexuality = models.IntegerField()
    mood = models.IntegerField()
    days_left = models.IntegerField(blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.sexuality is None:
            self.sexuality = randint(0,100)
        if self.mood is None:
            self.mood = randint(5,100)
        if self.days_left is None:
            self.days_left = 45
        if self.arrival_date is None:
            self.arrival_date = datetime.now()

    class Meta:
        managed = False
        db_table = 'lodger'

    def __str__(self):
        return self.name, self.age, self.sex, self.chosen_animal,self.main_feature, self.sexuality, self.mood


class Punished(models.Model):
    punishment_id = models.AutoField(primary_key=True)
    violation = models.ForeignKey('Violation', models.DO_NOTHING)
    person = models.ForeignKey(Lodger, models.DO_NOTHING)
    punishments = models.ForeignKey('Punishments', models.DO_NOTHING)
    penalty = models.TextField()

    class Meta:
        managed = False
        db_table = 'punished'


class Punishments(models.Model):
    punishments_id = models.AutoField(primary_key=True)
    law = models.TextField()
    punishment = models.TextField()

    class Meta:
        managed = False
        db_table = 'punishments'


class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    day_of_week = models.TextField()
    time_int = models.DurationField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.day_of_week is None:
            self.day_of_week = datetime.now().weekday()

    class Meta:
        managed = False
        db_table = 'schedule'


class Suitability(models.Model):
    man = models.OneToOneField(Lodger, models.DO_NOTHING, primary_key=True, related_name='suit_man')
    woman = models.ForeignKey(Lodger, models.DO_NOTHING, related_name='suit_woman')
    mutual_interest = models.FloatField(blank=True, null=True)
    days_to_couple = models.IntegerField(blank=True, null=True)



    class Meta:
        managed = False
        db_table = 'suitability'
        unique_together = (('man', 'woman'),)


class TurnedToAnimal(models.Model):
    to_animal_id = models.AutoField(primary_key=True)
    person = models.ForeignKey(Lodger, models.DO_NOTHING)
    animal_type = models.TextField()
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'turned_to_animal'


class Violation(models.Model):
    violation_id = models.AutoField(primary_key=True)
    person = models.ForeignKey(Lodger, models.DO_NOTHING, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    situation = models.TextField()

    class Meta:
        managed = False
        db_table = 'violation'
