from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app.models import MortgageOffer

TEST_OFFER = {
    "id": 3,
    "payment": 0,
    "bank_name": "post_bank",
    "term_min": 2,
    "term_max": 15,
    "rate_min": "3.0",
    "rate_max": "10.0",
    "payment_min": 1000000,
    "payment_max": 15000000,

}
UPDATED_OFFER = {
    "id": 2,
    "payment": 0,
    "bank_name": "updated_bank",
    "term_min": 10,
    "term_max": 30,
    "rate_min": "3.0",
    "rate_max": "10.0",
    "payment_min": 1000,
    "payment_max": 15000,

}


class BanksApiTestCase(APITestCase):
    # maxDiff = None

    def setUp(self) -> None:
        self.offers = [
            MortgageOffer.objects.create(
                bank_name="bank_1",
                term_min=2,
                term_max=15,
                rate_min=3.0,
                rate_max=10.0,
                payment_min=1000000,
                payment_max=15000000,
            ),
            MortgageOffer.objects.create(
                bank_name="bank_2",
                term_min=10,
                term_max=40,
                rate_min=11.0,
                rate_max=15.0,
                payment_min=100000,
                payment_max=10000000, )
        ]
        self.first_offer = {
            "id": 1,
            "payment": 74501,
            "bank_name": "bank_1",
            "term_min": 2,
            "term_max": 15,
            "rate_min": "3.0",
            "rate_max": "10.0",
            "payment_min": 1000000,
            "payment_max": 15000000,
        }
        self.second_offer = {
            "id": 2,
            "payment": 112820,
            "bank_name": "bank_2",
            "term_min": 10,
            "term_max": 40,
            "rate_min": "11.0",
            "rate_max": "15.0",
            "payment_min": 100000,
            "payment_max": 10000000,
        }

    def test_get_offer_list(self) -> None:
        """Test getting a list of offers"""
        url = reverse('offer-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, MortgageOffer.objects.count())

    def test_create_offer(self) -> None:
        """Test creating offer"""
        url = reverse('offer-list')
        response = self.client.post(url, TEST_OFFER, format='json')
        true_values = [item for item in TEST_OFFER.items()]  # list of tuples (key, value) pairs TEST_OFFER's
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, MortgageOffer.objects.count())
        for i, value in enumerate(response.data.items()):
            self.assertEqual(true_values[i], value)

    def test_update_offer(self) -> None:
        """Test updating offer"""
        offer = MortgageOffer.objects.last()
        url = reverse('offer-detail', args=(offer.id,))
        response = self.client.put(url, data=UPDATED_OFFER, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(UPDATED_OFFER, response.data)

    def test_delete_offer(self) -> None:
        """Test deleting offer"""
        offer = MortgageOffer.objects.first()
        url = reverse('offer-detail', args=(offer.id,))
        response = self.client.delete(url, format='json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(1, MortgageOffer.objects.count())

    def test_ordering_payment(self) -> None:
        """Test ordering offers"""
        url = reverse('offer-list')
        query_params = '?price=10000000&deposit=1000000&term=12&ordering=-payment'
        response = self.client.get(url + query_params)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([self.first_offer, self.second_offer], response.data)

        query_params = '?price=10000000&deposit=1000000&term=12&ordering=payment'
        response = self.client.get(url + query_params)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([self.first_offer, self.second_offer], response.data)

    def test_ordering_rate(self) -> None:
        """Test ordering offers"""
        url = reverse('offer-list')
        query_params = '?price=10000000&deposit=1000000&term=12&ordering=-rate_min'
        response = self.client.get(url + query_params)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([self.second_offer, self.first_offer], response.data)

        query_params = '?price=10000000&deposit=1000000&term=12&ordering=-rate_max'
        response = self.client.get(url + query_params)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([self.second_offer, self.first_offer], response.data)

    def test_filters_url(self) -> None:
        """Test filters"""
        url = '/api/offer/?price=10000000&deposit=1000000&term=12&'
        filter_rate = 'rate_max__lte=&rate_min__gte=3.1&payment_min=&payment_max='
        response = self.client.get(url + filter_rate)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([self.second_offer], response.json())

        filter_rate = 'rate_max__lte=10.0&rate_min__gte=&payment_min=&payment_max='
        response = self.client.get(url + filter_rate)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([self.first_offer], response.json())



