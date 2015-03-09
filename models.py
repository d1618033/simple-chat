from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    pass


class Participant(models.Model):
    room = models.ForeignKey(Room)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(Room)
    participant = models.ForeignKey(Participant)
    message = models.TextField()

    def __str__(self):
        return "[{0}]: {1}".format(self.participant, self.message)
