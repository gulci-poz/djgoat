from django.test import TestCase


class HomePageTest(TestCase):
    # zamiast testowania stałych testujemy tylko implementację
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
