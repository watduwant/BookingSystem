import calendar
from datetime import datetime

from store.models import ServiceDetailsDayTime


class GetServiceSlot(object):

    @staticmethod
    def service_data(service_id):
        return ServiceDetailsDayTime.objects.get(id=service_id)

    @staticmethod
    def check_slot(date, slot_date_list):
        if str(date) in slot_date_list:
            slot_booked = True
        else:
            slot_booked = False
        return slot_booked, slot_date_list

    def process(self, slot_date, service):
        date = datetime.strptime(slot_date, '%Y-%m-%d').date()
        slot_date_list = []
        cal = calendar.Calendar()
        weekday = self.service_data(service).ServiceDetailsDayID.Day

        for day in cal.itermonthdates(date.year, date.month):
            if day.weekday() == int(weekday):
                slot_date_list.append(day.strftime("%Y-%m-%d"))
        return self.check_slot(date, slot_date_list)
