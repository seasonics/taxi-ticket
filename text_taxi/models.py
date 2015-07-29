from django.db import models


# Create your models here.


class Taxi(models.Model):
	plate_number = models.CharField(max_length=256)
	phone_number = models.CharField(max_length=256)
	start = models.DateTimeField()
	last_run = models.DateTimeField()
	end = models.DateTimeField(blank=True, null=True)


class Ticket(models.Model):
	ticket_id = models.CharField(max_length=24, unique=True)
	ticket_type = models.CharField(max_length=256,blank=True, null=True)
	date = models.DateTimeField()
	taxies = models.ManyToManyField(Taxi)


