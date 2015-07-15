from django.contrib import admin
from models import Taxi

# Register your models here.
class TaxiAdmin(admin.ModelAdmin):
	pass


admin.site.register(Taxi, TaxiAdmin)
