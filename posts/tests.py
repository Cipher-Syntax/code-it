from django.test import TestCase, Client
from . models import Posts
from users.models import UserRegistration

# Create your tests here.
class TestModels(TestCase):
    def setUp(self):
        """ Set up before each test """
        self.user = UserRegistration.objects.create(firstname='Justine', lastname='Toong', email='programmerjustine@gmaill.com', password='wmsu00018')

    def test_model_Posts(self):
        # Structure for testing
        # 1. Set up code
        # 2. Logic to test
        # 3. Assertions

        posts = Posts.objects.create(
            title = 'I am GOAT',
            caption = 'Just grind',
            user = self.user
        )
        self.assertTrue(isinstance(posts, Posts))