import cookielib
import urllib2
import urllib
import datetime
import re
from bs4 import BeautifulSoup
import os
import csv
from models import Taxi, Ticket
import datetime
from twilio.rest import TwilioRestClient
from django.conf import settings
from django.utils import timezone
module_dir = os.path.dirname(__file__)





def create_taxi(plateNumber, phoneNumber):
    if Taxi.objects.filter(plate_number=plateNumber, phone_number=phoneNumber).exists():
        return None
    taxi = Taxi(plate_number=plateNumber, start=timezone.now(), last_run=timezone.now(), phone_number=phoneNumber)
    taxi.save()
    return taxi

def create_ticket(ticketNumber, ticketType, ticketDate):
    if Ticket.objects.filter(ticket_id=ticketNumber).exists():
        return None
    ticket = Ticket(ticket_id=ticketNumber, ticket_type=ticketType, date=ticketDate)
    ticket.save()
    return ticket

def associate_ticket_to_taxi(ticket,taxi):
    ticket.taxis.add(taxi)

def end_taxi_service(taxi):
    taxi.end = timezone.now()
    taxi.save()
    return taxi


def clear_taxis():
    taxis = Taxi.objects.filter(end__lte=timezone.now()-datetime.timedelta(days=7))
    if taxis.exists():
      taxis.delete()

class PlateDatabase:
    excel = os.path.join(module_dir, 'fixtures/taxi_plates.csv')

    def plateToOwner(self, plateNumber):
        with open(self.excel, 'rb') as csvfile:
            platereader = csv.reader(csvfile, delimiter=',')
            for row in platereader:
                if plateNumber[:-2] == row[1]:
                    return row[14]
        return None


class ParkingSite:
    URL = "https://parkingtickets.cityofchicago.org/CPSWeb/retrieveTicketsByLicensePlate.do"
    response = None

    def siteRequest(self, plateNumber, plateOwnerName):
        cookiej = cookielib.CookieJar()
        cookie_processor = urllib2.HTTPCookieProcessor(cookiej)
        opener = urllib2.build_opener(cookie_processor)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        payload = {
            'plateNumber': plateNumber,
            'plateState': "IL",
            'plateType': "TXI",
            'plateOwnerName': plateOwnerName,
        }

        encoded_data = urllib.urlencode(payload)
        request_object = urllib2.Request(self.URL, encoded_data.encode('utf-8'))
        response = opener.open(request_object)
        return response.read()

    def parse(self, response):
        ticketInfo = {}
        tickets = []
        soup = BeautifulSoup(response)
        ticketlist = soup.select("table.ticketList tbody tr")
        for x in ticketlist:
            ticket = {}
            td_list = x.select("td")
            ticket["ticket_id"] = td_list[1].string
            ticket["ticket_type"] = td_list[2].string
            ticket["date"] = datetime.datetime.strptime(td_list[5].string, "%m/%d/%Y").date()
            tickets.append(ticket)

        ticketInfo["count"] = len(tickets)
        ticketInfo["ticketList"] = tickets

        if not tickets:
            ticketInfo["ticketList"].append({'ticket_type':"You're fine"})
        return ticketInfo

class RunTaxi:

    def get_next_taxi(self):
        #should probs index last run
        if Taxi.objects.all().exists():
            taxi = Taxi.objects.order_by('last_run')[0]
            return taxi
        return None

    def get_taxi_tickets(self, taxi):
        PS = ParkingSite()
        PD = PlateDatabase()
        plate_owner = PD.plateToOwner(taxi.plate_number)
        response = PS.siteRequest(taxi.plate_number, plate_owner)
        tickets = PS.parse(response)
        taxi.last_run = timezone.now()
        taxi.save()
        return tickets

    def run_taxi_tickets(self,taxi,tickets):
        for x in tickets:
            self.run_ticket(x,taxi)


    def run_ticket(self, ticket, plateNumber):
        if not Ticket.objects.filter(ticket_id=ticket["ticket_id"]).exists():
            ticket = create_ticket(ticket["ticket_id"], ticket["ticket_type"],ticket["date"])
            taxi = Taxi().objects.get(plate_number=plateNumber)
            if ticket.date > taxi.start:
                if taxi.end is not None:
                    if ticket.date < taxi.end:
                        associate_ticket_to_taxi(ticket, taxi)
                        return self.send_message(taxi)
                else:
                    associate_ticket_to_taxi(ticket, taxi)
                    return self.send_message(taxi,ticket)
        return None

    def send_message(self, taxi, ticket):
        message_body = "New Ticket\n" + str(ticket.date) + ' ' + str(ticket.type)
        message = settings.TWILIO_CLIENT.messages.create(
            body=message_body,  # Message body, if any
            to=taxi.phone_number,
            from_=settings.TWILIO_PHONE_NUMBER,
        )
        return message
