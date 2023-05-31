class USER_STATUS:
    CUSTOMER, CR, SHOPOWNER, SO = 'customer', 'cr', 'shopowner', 'so'


class APPOINTMENT_STATUS:
    Status_Choices = (
        ('pending', 'pending'),
        ('accepted', 'accepted'),
        ('cancelled', 'cancelled'),
    )
    PENDING, ACCEPTED, CANCELLED = 'pending', 'accepted', 'cancelled'


class TIMESLOTS:
    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
    week_days = (
        ("monday", 'Monday'),
        ("tuesday", 'Tuesday'),
        ("wednesday", 'Wednesday'),
        ("thursday", 'Thursday'),
        ("friday", 'Friday'),
        ("saturday", 'Saturday'),
        ("sunday", 'Sunday')
    )
    weekDays = [MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY]
