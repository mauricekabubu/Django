from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Order
from django.urls import reverse
from rest_framework import status

User = get_user_model()

# Create your tests here.
class UserOrderTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username="user1",password="test1")
        user2 = User.objects.create_user(username="user2", password="test2")
        
        Order.objects.create(user=user1)
        Order.objects.create(user=user1)
        Order.objects.create(user=user2)
        Order.objects.create(user=user2)        
    
    def test_user_order_endpoint_retrieves_only_authenticated_user_orders(self):
        user = User.objects.get(username="user2")
        self.client.force_login(user)
        response = self.client.get(reverse("user-orders"))
        
        assert response.status_code == status.HTTP_200_OK
        
        orders = response.json()
        self.assertTrue(all(order["user"] == user.id for order in orders))
    
    def test_user_order_list_unauthenticated(self):
        response = self.client.get(reverse("user-orders"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
        