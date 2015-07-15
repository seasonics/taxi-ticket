from django.views.generic.edit import FormView
from django import forms
from django.shortcuts import render
from services import ParkingSite, PlateDatabase
import services
from django.views.generic import TemplateView, View
from twilio import twiml
from django.utils.decorators import method_decorator
from django_twilio.decorators import twilio_view
from django_twilio.request import decompose

class ThanksView(View):
    @method_decorator(twilio_view)
    def dispatch(self, request, *args, **kwargs):
        return super(ThanksView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        r = twiml.Response()
        twilio_request = decompose(request)
        plate = twilio_request.body
        services.create_taxi("fef" plate)
        r.message('Thanks for signing up')
        return r

class SearchForm(forms.Form):
    search = forms.CharField(label='Search', max_length=100)

class Home(FormView):
    template_name = 'home.html'
    form_class = SearchForm

    def form_valid(self, form):

    	self.success_url = '/tickets/'+form.cleaned_data['search']
        return super(Home, self).form_valid(form)

class Tickets(TemplateView):
    template_name = 'tickets.html'

    def get_context_data(self, **kwargs):
        context = super(Tickets, self).get_context_data(**kwargs)
        plate_number = self.kwargs['number']
        PS = ParkingSite()
        PD = PlateDatabase()
        plate_owner = PD.plateToOwner(plate_number)
        PS.siteRequest(plate_number, plate_owner)
        context['tickets'] = PS.parse()
        return context