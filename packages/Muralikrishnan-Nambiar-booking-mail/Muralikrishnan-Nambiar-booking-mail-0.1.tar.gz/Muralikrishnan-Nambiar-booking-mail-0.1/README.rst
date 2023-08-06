=====
Booking-Mail
=====

Booking-Mail is a Django app to crate a PDF and send it to the user who booked the bus ticket.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "booking_mail.apps.BookingMailConfig" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'booking_mail.apps.BookingMailConfig',
    ]

2. Include the polls URLconf in your project urls.py like this::

     path('booking/', include('booking_mail.urls')),

4. Book a ticket in  Blue-Bus application and you will get an option to send mail.