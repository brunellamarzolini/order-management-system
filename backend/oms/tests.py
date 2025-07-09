from django.urls import reverse
from django.core.cache import cache
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from localization.models import Language
from .models import Order, Product, ProductLang
from .serializers import OrderSerializer
import json

class OrderAPITestCase(APITestCase):
    
    def setUp(self):
        cache.clear()
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.language = Language.objects.create(code='en', name='English')
        self.product = Product.objects.create(price=10.0)
        ProductLang.objects.create(product=self.product, lang=self.language, name='Test Product')

        order_data = {
            'name': 'Test Order',
            'description': 'A test order',
            'products': [self.product.id],
        }
        serializer = OrderSerializer(data=order_data)
        serializer.is_valid(raise_exception=True)
        self.order = serializer.save()

    def test_list_products(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('results' in response.data)
        self.assertGreaterEqual(len(response.data['results']), 1)
        # Check that the test product is in the results
        product_ids = [str(p['id']) for p in response.data['results']]
        self.assertIn(str(self.product.id), product_ids)

    def test_filter_products_by_name(self):
        url = reverse('product-list')
        response = self.client.get(url, {'search': 'Test Product'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('results' in response.data)
        # All returned products should have 'Test Product' in their name
        for product in response.data['results']:
            self.assertIn('Test Product', product['name'])

    def test_list_orders(self):
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('results' in response.data)
        # Check that the test order is in the results
        order_ids = [str(o['id']) for o in response.data['results']]
        self.assertIn(str(self.order.id), order_ids)

    def test_order_sorting(self):
        # Create a second order with a different created_at
        product2 = Product.objects.create(price=20.0)
        ProductLang.objects.create(product=product2, lang=self.language, name='Second Product')
        order_data = {
            'name': 'Second Order',
            'description': 'Another test order',
            'products': [product2.id],
        }
        serializer = OrderSerializer(data=order_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        url = reverse('order-list')
        response = self.client.get(url, {'ordering': '-created_at'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('results' in response.data)
        # The first order in the results should be the most recently created
        self.assertEqual(response.data['results'][0]['name'], 'Second Order')

    def test_retrieve_order(self):
        url = reverse('order-detail', args=[self.order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Order')

    # def test_create_order(self):
    #     url = reverse('order-list')
    #     data = {
    #         'name': 'New Order',
    #         'description': 'Created via test',
    #         'products': [str(self.product.id)],
    #     }
    #     serializer = OrderSerializer(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     json_data = json.dumps(data)
    #     response = self.client.post(url, json_data, content_type='application/json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Order.objects.count(), 2)

    def test_partial_update_order(self):
        url = reverse('order-detail', args=[self.order.id])
        
        # Create a second product to test product array update
        product2 = Product.objects.create(price=20.0)
        ProductLang.objects.create(product=product2, lang=self.language, name='Second Product')
        data = {
            'name': 'Patch Order',
            'description': 'Order updated via PATCH',
            'products': [str(self.product.id), str(product2.id)],
        }
        serializer = OrderSerializer(instance=self.order, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        json_data = json.dumps(data)
        response = self.client.patch(url, json_data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.name, 'Patch Order')
        self.assertEqual(self.order.description, 'Order updated via PATCH')

        # Check that both products are now associated with the order
        product_ids = [str(pid) for pid in self.order.products.values_list('id', flat=True)]
        self.assertIn(str(self.product.id), product_ids)
        self.assertIn(str(product2.id), product_ids)
        self.assertEqual(len(product_ids), 2)

    def test_update_order(self):
        url = reverse('order-detail', args=[self.order.id])
        # Create a second product to test product array update
        product2 = Product.objects.create(price=20.0)
        ProductLang.objects.create(product=product2, lang=self.language, name='Second Product')
        data = {
            'name': 'Put Order',
            'description': 'Order updated via PUT',
            'products': [str(product2.id)],
        }
        serializer = OrderSerializer(instance=self.order, data=data)
        serializer.is_valid(raise_exception=True)
        json_data = json.dumps(data)
        response = self.client.put(url, json_data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.name, 'Put Order')
        self.assertEqual(self.order.description, 'Order updated via PUT')

        # Check that only the new product is associated with the order
        product_ids = [str(pid) for pid in self.order.products.values_list('id', flat=True)]
        self.assertIn(str(product2.id), product_ids)
        self.assertEqual(len(product_ids), 1)

    def test_delete_order(self):
        url = reverse('order-detail', args=[self.order.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())

    def test_order_list_caches_response(self):
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        lang = self.language.code
        cache_key = f"order:list:{lang}"
        cached = cache.get(cache_key)
        self.assertIsNotNone(cached)
        self.assertEqual(cached, response.data)

    def test_order_update_invalidates_cache(self):
        url = reverse('order-list')
        self.client.get(url)  # Populate cache
        lang = self.language.code
        cache_key = f"order:list:{lang}"
        self.assertIsNotNone(cache.get(cache_key))
        update_url = reverse('order-detail', args=[self.order.id])
        data = {'name': 'Updated Order', 'description': 'desc', 'products': [self.product.id]}
        self.client.put(update_url, data, format='json')
        self.assertIsNone(cache.get(cache_key))