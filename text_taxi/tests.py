import json as _json
import os
import services
import datetime
from django.test import TestCase
from models import Taxi, Ticket
from django.test.client import Client
from services import ParkingSite, PlateDatabase, RunTaxi
from django.utils import timezone
module_dir = os.path.dirname(__file__)

# Create your tests here.
class CreateTaxiServices(TestCase):

	def setUp(self):
		self.sample_html = open(os.path.join(module_dir, 'fixtures/sample_parse.html'), 'rb').read()

	def test_create_taxi(self):
		before = timezone.now()
		services.create_taxi("eewjowjx", "deiuedcned")
		after = timezone.now()
		self.assertEqual(Taxi.objects.count(), 1)
		self.assertEqual(Taxi.objects.first().phone_number, "deiuedcned")
		self.assertEqual(Taxi.objects.first().plate_number, "eewjowjx")
		self.assertLess(Taxi.objects.first().last_run, after)
		self.assertGreater(Taxi.objects.first().last_run, before)

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
		date = timezone.now()
		services.create_ticket("eewjowjx", "deiuedcned", date)
		self.assertEqual(Ticket.objects.count(), 1)
		self.assertEqual(Ticket.objects.first().ticket_type, "deiuedcned")
		self.assertEqual(Ticket.objects.first().ticket_id, "eewjowjx")
		self.assertEqual(Ticket.objects.first().date, date)

	def test_two_create_ticket(self):
		date = timezone.now()
		services.create_ticket("eewjowjx", "deiuedcned", date)
		services.create_ticket("eewjwowjx", "deiuedcned", date)
		self.assertEqual(Ticket.objects.count(), 2)

	def test_same_ticket(self):
		date = timezone.now()
		services.create_ticket("eewjowjx", "deiuedcned", date)
		ticket_one = services.create_ticket("eewjowjx", "deidxuedcned", date)
		self.assertEqual(ticket_one, None)
		self.assertEqual(Ticket.objects.count(), 1)

	def test_associate_ticket_to_taxi(self):
		date = timezone.now()
		taxi_one = services.create_taxi("eewjowjx", "deiuedcned")
		ticket_one = services.create_ticket("eewjowjx", "deiuedcned", date)
		services.associate_ticket_to_taxi(ticket_one, taxi_one)
		self.assertEqual(taxi_one.ticket_set.first(), ticket_one)

	def test_associate_two_tickets_to_taxi(self):
		date = timezone.now()
		taxi_one = services.create_taxi("eewjowjx", "deiuedcned")
		ticket_one = services.create_ticket("eewjowjx", "deiuedcned", date)
		ticket_two = services.create_ticket("eewjowfjx", "deiuedcned", date)
		services.associate_ticket_to_taxi(ticket_one, taxi_one)
		services.associate_ticket_to_taxi(ticket_two, taxi_one)
		self.assertEqual(taxi_one.ticket_set.count(), 2)

	def test_associate_one_tickets_to_two_taxi(self):
		date = timezone.now()
		taxi_one = services.create_taxi("eewjowjx", "deiuedcned")
		taxi_two = services.create_taxi("eewjowjex", "deiuedcned")
		ticket_one = services.create_ticket("eewjowjx", "deiuedcned", date)
		services.associate_ticket_to_taxi(ticket_one, taxi_one)
		services.associate_ticket_to_taxi(ticket_one, taxi_two)
		self.assertEqual(taxi_one.ticket_set.first(), ticket_one)
		self.assertEqual(taxi_two.ticket_set.first(), ticket_one)

	def test_end_taxi_service(self):
		before = timezone.now()
		taxi = services.create_taxi("eewjowjx", "deiuedcned")
		self.assertIsNone(taxi.end)
		services.end_taxi_service(taxi)
		after = timezone.now()
		self.assertLess(taxi.end, after)
		self.assertGreater(taxi.end, before)

	def test_clear_taxis(self):
		taxi = services.create_taxi("eewjowjx", "deiuedcned")
		services.clear_taxis()
		self.assertEqual(Taxi.objects.count(), 1)
		taxi.end = timezone.now()
		services.clear_taxis()
		self.assertEqual(Taxi.objects.count(), 1)
		taxi.end = timezone.now()-datetime.timedelta(days=8)
		taxi.save()
		services.clear_taxis()
		self.assertEqual(Taxi.objects.count(), 0)
		
	#should probably test database better
	def test_plate_database(self):
		PD = PlateDatabase()
		plate_owner = PD.plateToOwner("6610tx")
		self.assertEqual(plate_owner, "Chicago Carriage Cab")
		self.assertIsNone(PD.plateToOwner("6610txsdf"))

	def test_parse(self):
		PS = ParkingSite()
		ticketInfo = PS.parse(self.sample_html)
		self.assertEqual(ticketInfo["count"], 14)
		self.assertEqual(ticketInfo["ticketList"][0]['ticket_type'], "Park or stand in bus/taxi/carriage stand")
		self.assertEqual(ticketInfo["ticketList"][0]['ticket_id'], "0054711465")
		self.assertEqual(ticketInfo["ticketList"][0]['date'], datetime.date(2008, 4, 10))

	#if this fails might be site
	def test_site_and_parse(self):
		PS = ParkingSite()
		PD = PlateDatabase()
		plate_owner = PD.plateToOwner("6610TX")
		response = PS.siteRequest("6610TX", plate_owner)
		ticketInfo = PS.parse(response)
		self.assertGreaterEqual(ticketInfo["count"], 14)
		self.assertEqual(ticketInfo["ticketList"][0]['ticket_type'], "Park or stand in bus/taxi/carriage stand")
		self.assertEqual(ticketInfo["ticketList"][0]['ticket_id'], "0054711465")
		self.assertEqual(ticketInfo["ticketList"][0]['date'], datetime.date(2008, 4, 10))

class RunTaxiServices(TestCase):

	def setUp(self):
		self.taxi_one = services.create_taxi("6610TX", "deiuedcned")
		self.taxi_two = services.create_taxi("two", "deiuedcned")
		self.taxi_three = services.create_taxi("three", "deiuedcned")

	def test_get_next_taxi(self):
		RT = RunTaxi()
		taxi = RT.get_next_taxi()
		self.assertEqual(self.taxi_one, taxi)

	def test_get_next_taxi_none(self):
		Taxi.objects.all().delete()
		RT = RunTaxi()
		taxi = RT.get_next_taxi()
		self.assertIsNone(taxi)

	def test_get_taxi_tickets(self):
		RT = RunTaxi()
		taxi = RT.get_next_taxi()
		ticketInfo = RT.get_taxi_tickets(taxi)
		self.assertGreaterEqual(ticketInfo["count"], 14)
		self.assertEqual(ticketInfo["ticketList"][0]['ticket_type'], "Park or stand in bus/taxi/carriage stand")
		self.assertEqual(ticketInfo["ticketList"][0]['ticket_id'], "0054711465")
		self.assertEqual(ticketInfo["ticketList"][0]['date'], datetime.date(2008, 4, 10))
		taxi = RT.get_next_taxi()
		ticketInfo = RT.get_taxi_tickets(taxi)
		self.assertEqual(ticketInfo["count"], 0)
		self.assertEqual(self.taxi_two, taxi)
		taxi = RT.get_next_taxi()
		self.assertEqual(self.taxi_three, taxi)

	def test_run_ticket(self):
		print "x"













	#def test_create_one(self):
		#client = Client()
		#json_data = '''{
  			#"From": "+12928348",
  			#"Body": "6610TX",
  			#}'''
		#self.assertEqual(False, True)