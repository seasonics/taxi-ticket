from django.conf.urls import patterns, url
from text_taxi.views import Home, Tickets, ThanksView

urlpatterns = patterns('text_taxi.views',
	url(r'^$', Home.as_view(), name='home'),
	url(r'^tickets/(?P<number>.*)/$', Tickets.as_view(), name='tickets'),
	url(r'^message/$', ThanksView.as_view(), name='thanks'),
	)
