from django import template
from store.models import ServiceDetails
import datetime

register = template.Library()

@register.filter(name='get_servicedetails')
def get_servicedetails(service):
    servicedet = ServiceDetails.objects.filter(ServiceID=service)
    return servicedet


@register.filter(name='get_dates')
def get_dates(day):
    day = int(day)
    todaywd = datetime.datetime.today().weekday()
    diff = 0
    if(todaywd<day):
        diff = day - todaywd

    elif(day<todaywd):
        diff = 7 + day - todaywd
    dates = [1, 2, 3]
    dates[0] = datetime.date.today() + datetime.timedelta(days=diff)
    dates[1] = dates[0] + datetime.timedelta(days=7)
    dates[2] = dates[1] + datetime.timedelta(days=7)
    print(dates[0])
    return dates