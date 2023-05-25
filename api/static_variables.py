class USER_STATUS:
    CUSTOMER, CR, SHOPOWNER, SO = 'customer', 'cr', 'shopowner', 'so'


class APPOINTMENT_STATUS:
    Status_Choices = (
        ('pending', 'pending'),
        ('accepted', 'accepted'),
        ('cancelled', 'cancelled'),
    )
    PENDING, ACCEPTED, CANCELLED = 'pending', 'accepted', 'cancelled'
