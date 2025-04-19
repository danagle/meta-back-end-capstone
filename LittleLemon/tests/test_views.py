from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, Client
import json
from rest_framework import status
from rest_framework.test import APITestCase

from restaurant.models import Booking, Menu

###
# Tests using django.test.TestCase
###

class MenuView_Tests(TestCase):
    def setUp(self):
        self.client = Client()

        self.menu1 = Menu.objects.create(title='Pasta', price=12.50, inventory=10)
        self.menu2 = Menu.objects.create(title='Burger', price=9.99, inventory=20)

        self.list_url = reverse('menu-list')

    def test_get_menu_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['title'], self.menu1.title)
        self.assertEqual(data[1]['title'], self.menu2.title)

    def test_create_menu_item(self):
        new_item = {
            "title": "Salad",
            "price": 7.00,
            "inventory": 15
        }
        response = self.client.post(
            self.list_url,
            data=json.dumps(new_item),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Menu.objects.count(), 3)
        self.assertEqual(Menu.objects.latest('id').title, 'Salad')


class SingleMenuItemView_Tests(TestCase):
    def setUp(self):
        self.client = Client()
        self.menu = Menu.objects.create(title='Pizza', price=15.99, inventory=5)
        self.detail_url = reverse('menu-detail', args=[self.menu.id])  # Ensure your URL name matches

    def test_get_single_menu_item(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['title'], self.menu.title)
        self.assertEqual(float(data['price']), float(self.menu.price))

    def test_update_menu_item(self):
        updated_data = {
            'title': 'Expensive Pizza',
            'price': 99.49,
            'inventory': 3
        }
        response = self.client.put(
            self.detail_url,
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.menu.refresh_from_db()
        self.assertEqual(self.menu.title, 'Expensive Pizza')
        self.assertEqual(float(self.menu.price), 99.49)
        self.assertEqual(self.menu.inventory, 3)

    def test_partial_update_menu_item(self):
        response = self.client.patch(
            self.detail_url,
            data=json.dumps({'inventory': 3}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.menu.refresh_from_db()
        self.assertEqual(self.menu.inventory, 3)

    def test_delete_menu_item(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Menu.objects.filter(id=self.menu.id).exists())


class BookingViewSet_Tests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create user and login
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        # Create sample booking
        self.booking = Booking.objects.create(
            name='John Doe',
            no_of_guests=2
        )

        self.list_url = reverse('booking-list')
        self.detail_url = reverse('booking-detail', args=[self.booking.id])

    def test_list_bookings(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], self.booking.name)

    def test_create_booking(self):
        payload = {
            'name': 'Jane Smith',
            'no_of_guests': 4
        }
        response = self.client.post(
            self.list_url,
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Booking.objects.count(), 2)
        self.assertEqual(Booking.objects.latest('id').name, 'Jane Smith')

    def test_retrieve_booking(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['name'], self.booking.name)

    def test_update_booking(self):
        updated_payload = {
            'name': 'John Updated',
            'no_of_guests': 3
        }
        response = self.client.put(
            self.detail_url,
            data=json.dumps(updated_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.name, 'John Updated')
        self.assertEqual(self.booking.no_of_guests, 3)

    def test_delete_booking(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Booking.objects.filter(id=self.booking.id).exists())

    def test_unauthenticated_access_is_denied(self):
        self.client.logout()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 401)

###
# Tests using rest_framework.test.APITestCase
###

class MenuViewTests(APITestCase):
    def setUp(self):
        self.menu1 = Menu.objects.create(title='Pasta', price=12.50, inventory=10)
        self.menu2 = Menu.objects.create(title='Burger', price=9.99, inventory=20)
        self.list_url = reverse('menu-list')  

    def test_get_menu_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], self.menu1.title)
        self.assertEqual(response.data[1]['title'], self.menu2.title)

    def test_create_menu_item(self):
        data = {
            'title': 'Salad',
            'price': 7.00,
            'inventory': 15
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 3)
        self.assertEqual(Menu.objects.last().title, 'Salad')


class SingleMenuItemViewTests(APITestCase):
    def setUp(self):
        self.menu_item = Menu.objects.create(title='Pizza', price=15.99, inventory=5)
        self.detail_url = reverse('menu-detail', args=[self.menu_item.id])

    def test_get_single_menu_item(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.menu_item.title)

    def test_update_menu_item(self):
        updated_data = {
            'title': 'Expensive Pizza',
            'price': 99.49,
            'inventory': 7
        }
        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.title, 'Expensive Pizza')
        self.assertEqual(float(self.menu_item.price), 99.49)

    def test_partial_update_menu_item(self):
        response = self.client.patch(self.detail_url, {'inventory': 3}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.inventory, 3)

    def test_delete_menu_item(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Menu.objects.filter(id=self.menu_item.id).exists())


class BookingViewSetTests(APITestCase):
    def setUp(self):
        # Create and authenticate a user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        # Create a sample booking
        self.booking = Booking.objects.create(
            name='John Doe',
            no_of_guests=2
        )

        self.list_url = reverse('booking-list')  # from DefaultRouter
        self.detail_url = reverse('booking-detail', args=[self.booking.id])

    def test_list_bookings(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.booking.name)

    def test_create_booking(self):
        data = {
            'name': 'Jane Smith',
            'no_of_guests': 4
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 2)
        self.assertEqual(Booking.objects.latest('id').name, 'Jane Smith')

    def test_retrieve_booking(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.booking.name)

    def test_update_booking(self):
        updated_data = {
            'name': 'John Updated',
            'no_of_guests': 3
        }
        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.name, 'John Updated')

    def test_delete_booking(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Booking.objects.filter(id=self.booking.id).exists())

    def test_unauthenticated_access(self):
        self.client.logout()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
