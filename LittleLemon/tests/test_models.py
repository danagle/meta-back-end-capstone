from django.test import TestCase
from restaurant.models import Booking, Menu


class BookingModelTests(TestCase):
    def setUp(self):
        self.booking = Booking.objects.create(
            name='Ada Lovelace',
            no_of_guests=3
        )

    def test_booking_fields(self):
        self.assertEqual(self.booking.name, 'Ada Lovelace')
        self.assertEqual(self.booking.no_of_guests, 3)

    def test_booking_str_representation(self):
        self.assertEqual(str(self.booking), 'Ada Lovelace')


class MenuModelTests(TestCase):
    def setUp(self):
        self.menu = Menu.objects.create(
            title='Spaghetti',
            price=10.49,
            inventory=25
        )

    def test_menu_fields(self):
        self.assertEqual(self.menu.title, 'Spaghetti')
        self.assertEqual(float(self.menu.price), 10.49)
        self.assertEqual(self.menu.inventory, 25)

    def test_menu_str_representation(self):
        expected_str = 'Spaghetti : 10.49'
        self.assertEqual(str(self.menu), expected_str)
    