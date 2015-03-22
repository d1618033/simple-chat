from django.db import models
from django.utils.timezone import now
from datetime import timedelta
import string
import random


ROOM_EXPIRATION = timedelta(minutes=1)


class OldRoomsManager(models.Manager):
    def get_queryset(self):
        time = now() - ROOM_EXPIRATION
        queryset = []
        for room in super(OldRoomsManager, self).get_queryset():
            if (not room.has_participants()) or room.last_active() < time:
                queryset.append(room)
        return queryset


class Room(models.Model):
    objects = models.Manager()
    old_rooms = OldRoomsManager()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Room: {0}".format(self.pk)

    def last_active(self):
        result = self.message_set.aggregate(models.Max("created"))["created__max"]
        if result is None:
            return self.created
        else:
            return result

    def has_participants(self):
        return len(self.participant_set.all()) > 0


def generate_password():
    possible = string.ascii_letters + string.digits
    return "".join([random.choice(possible) for _ in range(100)])


class Participant(models.Model):
    room = models.ForeignKey(Room)
    name = models.CharField(max_length=100)
    password = models.CharField(default=generate_password, max_length=100)

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(Room)
    participant = models.ForeignKey(Participant)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "[{0}]: {1}".format(self.participant, self.message)
