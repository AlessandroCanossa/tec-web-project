from django.contrib.auth import get_user_model
from django.test import TestCase


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='normal@user.com', password='foo', username='normalUser')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_creator)
        self.assertEqual(user.username, 'normalUser')
        self.assertEqual(user.coins, 0)

        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo", username='foo')

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='super@user.com', password='foo', username='super')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertEqual(admin_user.username, 'super')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False)


class UsersModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='prova@prova.com', password='foo', username='prova'
        )

    def test_user_str(self):
        self.assertEqual(self.user.__str__(), 'prova')
