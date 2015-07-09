from django.db import models

# Create your models here.


class Taxi(models.Model):
	plate_number = models.CharField(max_length=256)
	phone_number = models.CharField(max_length=256)
	start = models.DateTimeField()
	end = models.DateTimeField()


class Ticket(models.Model):
	ticket_id = models.CharField(max_length=24)
	taxies = models.ManyToManyField(Taxi)


