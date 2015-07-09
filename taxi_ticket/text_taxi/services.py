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
module_dir = os.path.dirname(__file__)


def create_taxi(plateNumber, phoneNumber):
    taxi = Taxi(plate_number=plateNumber, start=datetime.datetime.now(), phone_number=phoneNumber)
    taxi.save()

def create_ticket(ticketNumber):
    ticket = Ticket(ticket_id=ticketNumber)
    ticket.save()

def associate_ticket_to_taxi(ticketNumber,plateNumber):
    ticket= Ticket().objects.get(ticket_id=ticketNumber)
    taxi = Taxi().objects.get(plate_number=plateNumber)
    ticket.taxis.add(taxi)

def end_taxi_service(plateNumber):
    taxi = Taxi().objects.get(plate_number=plateNumber)
    taxi.end = datetime.datetime.now()

def clear_taxis():
    Taxi().objects.get(end__lte=datetime.now()-timedelta(days=7)).delete()

class PlateDatabase:
    excel = os.path.join(module_dir, 'fixtures/taxi_plates.csv')

    def plateToOwner(self, plateNumber):
        with open(self.excel, 'rb') as csvfile:
            platereader = csv.reader(csvfile, delimiter=',')
            for row in platereader:
                if plateNumber[:-2] == row[1]:
                    return row[14]


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
        self.response = response

    def parse(self):
        tickets = []
        soup = BeautifulSoup(self.response.read())
        ticketlist = soup.select("table.ticketList tbody tr")
        for x in ticketlist:
            ticket = {}
            td_list = x.select("td")
            ticket["ticket_id"] = td_list[1].string
            ticket["ticket_type"] = td_list[2].string
            ticket["date"] = td_list[5].string
            tickets.append(ticket)
        return tickets
