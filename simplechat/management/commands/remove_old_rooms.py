from django.core.management.base import BaseCommand
from simplechat.models import Room


class Command(BaseCommand):
    help = 'Removes old rooms'

    def handle(self, *args, **options):
        self.stdout.write("Number of existing rooms: {0}".format(len(Room.objects.all())))
        for room in Room.old_rooms.all():
            self.stdout.write("Deleting room {0}".format(room.pk))
            room.delete()
            self.stdout.write('Successfully deleted room')
        self.stdout.write("Number of remaining rooms: {0}".format(len(Room.objects.all())))