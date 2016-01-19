from django.core.management.base import BaseCommand, CommandError
from text_taxi.services import RunTaxi

class Command(BaseCommand):

    def handle(self, *args, **options):
        RT = RunTaxi()
        taxi = RT.get_next_taxi()
        if taxi is not None:
            tickets = RT.get_taxi_tickets(taxi)
            RT.run_taxi_tickets(taxi, tickets)

        
