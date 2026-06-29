from django.test import TestCase
from rest_framework.test import APIClient

class CGPACalculatorTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_valid_cgpa(self):
        response = self.client.post('/api/calculate/',
            {'semesters': [8.5, 7.9, 8.2, 9.0]}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('cgpa', response.data)
        self.assertIn('percentage', response.data)
        self.assertIn('grade', response.data)

    def test_empty_semesters(self):
        response = self.client.post('/api/calculate/',
            {'semesters': []}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_grade_O(self):
        response = self.client.post('/api/calculate/',
            {'semesters': [9.5, 9.8]}, format='json')
        self.assertEqual(response.data['grade'], 'O')
