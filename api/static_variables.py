class USER_STATUS:
    CUSTOMER, CR, SHOPOWNER, SO = 'customer', 'cr', 'shopowner', 'so'
    USER_ROLE = (
        ('cr', 'customer'),
        ('so', 'shopowner'),
    )


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
        ("0", 'Monday'),
        ("1", 'Tuesday'),
        ("2", 'Wednesday'),
        ("3", 'Thursday'),
        ("4", 'Friday'),
        ("5", 'Saturday'),
        ("6", 'Sunday')
    )
    weekDays = [MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY]


class GENDER_CHOICES:
    M, F, O = 'Male', 'Female', 'Other'
    Gender_Choices = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
