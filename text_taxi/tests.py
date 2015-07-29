from django.test import TestCase
from models import Taxi, Ticket
import json as _json
from django.test.client import Client
import services
import datetime

# Create your tests here.
class CreateTaxi(TestCase):

	def test_create_taxi(self):
		services.create_taxi("eewjowjx", "deiuedcned")
		self.assertEqual(Taxi.objects.count(), 1)
		self.assertEqual(Taxi.objects.first().phone_number, "deiuedcned")
		self.assertEqual(Taxi.objects.first().plate_number, "eewjowjx")
		self.assertEqual(Taxi.objects.first().plate_number, "eewjowjx")

	def test_two_create_taxi(self):
		services.create_taxi("eewjowjx", "deiuedcned")
		services.create_taxi("eewjowx", "deiuedcned")
		self.assertEqual(Taxi.objects.count(), 2)

	def test_same_taxi(self):
		taxi_one = services.create_taxi("eewjowjx", "deiuedcned")
		taxi_two = services.create_taxi("eewjowjx", "deiuedcned")
		self.assertEqual(taxi_two, None)
		self.assertEqual(Taxi.objects.count(), 1)

	def test_create_ticket(self):
		date = datetime.datetime.now()
		services.create_ticket("eewjowjx", "deiuedcned", date)
		self.assertEqual(Ticket.objects.count(), 1)
		self.assertEqual(Ticket.objects.first().ticket_type, "deiuedcned")
		self.assertEqual(Taxi.objects.first().ticket_id, "eewjowjx")
		self.assertEqual(date, date)



	#def test_create_one(self):
		#client = Client()
		#json_data = '''{
  			#"From": "+12928348",
  			#"Body": "6610TX",
  			#}'''
		#self.assertEqual(False, True)