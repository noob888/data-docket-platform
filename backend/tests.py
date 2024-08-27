from http import HTTPStatus
from django.test import TestCase, Client
from django.urls import reverse
from .models import *
from django.db import transaction
from django.core import serializers
from django.utils import timezone
import json

import logging
logger = logging.getLogger('django.db.backends')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

class UserTestCase(TestCase):
    @transaction.atomic
    def test_user_create(self):
        # Test creating a new user
        response = self.client.post('/user/create/', {'email': 'testuser@test.com', 'first_name': 'Test', 'last_name': 'User', 'phone_number': '1234567890', 'is_superadmin': False, 'rank': 1, 'university': 'Test University', 'company': 'Test Company'})
        self.assertEqual(response.status_code, 302)

        # Get the primary key of the newly created user from the response content
        user_id = int(response.url.split('/')[-2])

       # Test retrieving the newly created user
        user = User.objects.get(email='testuser@test.com')
        self.assertEqual(user.email, 'testuser@test.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.phone_number, '1234567890')
        self.assertEqual(user.is_superadmin, False)
        self.assertEqual(user.rank, 1)
        self.assertEqual(user.university, 'Test University')
        self.assertEqual(user.company, 'Test Company')

class CompetitionListTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('competition_list')
        self.competition_data = {
            'name': 'Test Competition',
            'category': 'finance',
            'host_id': 1,
            'prize_amount': 5000,
            'start_date': '2023-04-01T00:00:00Z',
            'end_date': '2023-04-30T23:59:59Z',
            'deliverable': '',
            'visualization': False,
            'guaranteed_submissions': False,
            'is_featured': False,
            'live_presentations': False,
        }

    def test_competition_list_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.json()), 0)  # assuming there are no competitions in the database

    def test_competition_list_post(self):
        response = self.client.post(self.url, data=json.dumps(self.competition_data), content_type='application/json')
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(response.json()['name'], self.competition_data['name'])
        self.assertEqual(response.json()['category'], self.competition_data['category'])


class CompetitionDetailTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.competition = Competition.objects.create(
            name='Test Competition',
            category='finance',
            host_id_id=1,
            prize_amount=5000,
            start_date='2023-04-01T00:00:00Z',
            end_date='2023-04-30T23:59:59Z',
        )
        self.url = reverse('competition_detail', args=[self.competition.pk])
        self.updated_data = {
            'name': 'Updated Test Competition',
            'category': 'sports',
            'prize_amount': 10000,
            'visualization': True,
            'is_featured': True,
        }

    def test_competition_detail_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json()['name'], self.competition.name)
        self.assertEqual(response.json()['category'], self.competition.category)

    def test_competition_detail_put(self):
        response = self.client.put(self.url, data=json.dumps(self.updated_data), content_type='application/json')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json()['name'], self.updated_data['name'])
        self.assertEqual(response.json()['category'], self.updated_data['category'])
        self.assertEqual(response.json()['prize_amount'], self.updated_data['prize_amount'])
        self.assertEqual(response.json()['visualization'], self.updated_data['visualization'])
        self.assertEqual(response.json()['is_featured'], self.updated_data['is_featured'])

    def test_competition_detail_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertFalse(Competition.objects.filter(pk=self.competition.pk).exists())