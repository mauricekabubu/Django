#from django.test import TestCase
# from django.contrib.auth import get_user_model
# from .models import Order
from django.urls import reverse
from .models import User, Product
from rest_framework.test import APITestCase
from rest_framework import status

# User = get_user_model()

# # Create your tests here.
# class UserOrderTestCase(TestCase):
#     def setUp(self):
#         user1 = User.objects.create_user(username="user1",password="test1")
#         user2 = User.objects.create_user(username="user2", password="test2")
        
#         Order.objects.create(user=user1)
#         Order.objects.create(user=user1)
#         Order.objects.create(user=user2)
#         Order.objects.create(user=user2)        
    
#     def test_user_order_endpoint_retrieves_only_authenticated_user_orders(self):
#         user = User.objects.get(username="user2")
#         self.client.force_login(user)
#         response = self.client.get(reverse("user-orders"))
        
#         assert response.status_code == status.HTTP_200_OK
        
#         orders = response.json()
#         self.assertTrue(all(order["user"] == user.id for order in orders))
    
#     def test_user_order_list_unauthenticated(self):
#         response = self.client.get(reverse("user-orders"))
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username="Maurice",password="Burunje@")
        self.normal_user = User.objects.create_user(username="Ashley",password="Ashley254@")
        self.product = Product.objects.create(
            name="Remote",
            description="A digital and smart remote control",
            price=2500.00,
            stock=5
        ) 
        
        self.url = reverse("product-detail", kwargs={"product_id":self.product.pk})
    
    def test_get_product(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product.name)
        
    def test_unauthorized_update_product(self):
        data = {"name":"Updated product"}
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_unauthorized_delete_product(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_only_admins_can_delete_products(self):
        # test normal user cannot delete - note that this could be its own method
        self.client.login(username="Ashley",password="Ashley254@")
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())
        
        # test admin user can delete
        self.client.login(username="Maurice",password="Burunje@")
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())
        