from django.db import IntegrityError
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from users.models import CoinsPurchase, User


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
        self.User: User = get_user_model()
        self.User.objects.create_user(
            email='prova@prova.com', password='foo', username='prova'
        )

    def test_login(self):
        response = self.client.login(
            username='prova', password='foo'
        )
        self.assertTrue(response)

    def test_login_invalid_credentials(self):
        response = self.client.login(
            username='prova', password='wrong'
        )
        self.assertFalse(response)

    def test_create_existing_user(self):
        with self.assertRaises(IntegrityError):
            self.User.objects.create_user(
                email='prova@prova.com', password='foo', username='prova'
            )

    def test_create_user_with_email_invalid(self):
        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                email='', password='foo', username='prova'
            )

    def test_create_user_with_username_invalid(self):
        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                email='prova2@prova.com', password='foo', username=''
            )

    def test_create_user_with_email_and_username_invalid(self):
        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                email='', password='foo', username=''
            )

    def test_create_user_with_password_invalid(self):
        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                email='prova2@prova.com', password='', username='prova2'
            )


class UserViewTest(TestCase):
    def setUp(self):
        self.User: User = get_user_model()
        self.User.objects.create_user(
            email='prova@prova.com', password='foo', username='prova'
        )

    def test_logout(self):
        self.client.login(username='prova', password='foo')
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)

    def test_change_username(self):
        self.client.login(username='prova', password='foo')

        user = self.User.objects.get(
            id=self.client.session.get('_auth_user_id'))
        self.assertEqual(user.username, 'prova')

        response = self.client.post(
            reverse('users:change_username'),
            {'username': 'new_username'},
        )

        self.assertEqual(response.status_code, 200)

        user.refresh_from_db()
        self.assertEqual(user.username, 'new_username')

    def test_change_username_invalid_username(self):
        self.client.login(username='prova', password='foo')

        user = self.User.objects.get(
            id=self.client.session.get('_auth_user_id'))
        self.assertEqual(user.username, 'prova')

        response = self.client.post(
            reverse('users:change_username'),
            {'username': ' '},
        )

        self.assertEqual(response.status_code, 400)

        user.refresh_from_db()
        self.assertEqual(user.username, 'prova')

    def test_change_username_invalid_username_length(self):
        self.client.login(username='prova', password='foo')

        user = self.User.objects.get(
            id=self.client.session.get('_auth_user_id'))
        self.assertEqual(user.username, 'prova')

        response = self.client.post(
            reverse('users:change_username'),
            {'username': 'a' * 2000},
        )

        self.assertEqual(response.status_code, 400)

        user.refresh_from_db()
        self.assertEqual(user.username, 'prova')

    def test_change_password(self):
        self.client.login(username='prova', password='foo')

        user: User = self.User.objects.get(
            id=self.client.session.get('_auth_user_id'))
        self.assertTrue(user.check_password('foo'))

        response = self.client.post(
            reverse('users:change_password'),
            {'old_password': 'foo', 'new_password1': 'ciao1234',
                'new_password2': 'ciao1234'},
        )

        self.assertEqual(response.status_code, 200)

        user.refresh_from_db()
        self.assertTrue(user.check_password('ciao1234'))

    def test_change_password_invalid_old_password(self):
        self.client.login(username='prova', password='foo')

        user: User = self.User.objects.get(
            id=self.client.session.get('_auth_user_id'))
        self.assertTrue(user.check_password('foo'))

        response = self.client.post(
            reverse('users:change_password'),
            {'old_password': 'wrong', 'new_password1': 'ciao1234',
                'new_password2': 'ciao1234'},
        )

        self.assertEqual(response.status_code, 400)

        user.refresh_from_db()
        self.assertTrue(user.check_password('foo'))

    def test_buy_coins(self):
        self.client.login(username='prova', password='foo')

        user = self.User.objects.get(
            id=self.client.session.get('_auth_user_id'))
        self.assertEqual(user.coins, 0)

        response = self.client.post(
            reverse('users:buy_coins'),
            {'coins_amount': 500},
        )

        self.assertEqual(response.status_code, 200)

        user.refresh_from_db()
        self.assertEqual(user.coins, 500)

    def test_buy_coins_invalid_amount(self):
        self.client.login(username='prova', password='foo')

        user = self.User.objects.get(
            id=self.client.session.get('_auth_user_id'))
        self.assertEqual(user.coins, 0)

        response = self.client.post(
            reverse('users:buy_coins'),
            {'coins_amount': -1},
        )

        self.assertEqual(response.status_code, 400)

        user.refresh_from_db()
        self.assertEqual(user.coins, 0)

    def test_buy_coins_invalid_amount_string(self):
        self.client.login(username='prova', password='foo')

        user = self.User.objects.get(
            id=self.client.session.get('_auth_user_id'))
        self.assertEqual(user.coins, 0)

        response = self.client.post(
            reverse('users:buy_coins'),
            {'coins_amount': 'a'},
        )

        self.assertEqual(response.status_code, 400)

        user.refresh_from_db()
        self.assertEqual(user.coins, 0)

    def test_buy_coins_invalid_amount_zero(self):
        self.client.login(username='prova', password='foo')

        user = self.User.objects.get(
            id=self.client.session.get('_auth_user_id'))
        self.assertEqual(user.coins, 0)

        response = self.client.post(
            reverse('users:buy_coins'),
            {'coins_amount': 0},
        )

        self.assertEqual(response.status_code, 400)

        user.refresh_from_db()
        self.assertEqual(user.coins, 0)

    def test_buy_coins_not_logged(self):
        self.client.logout()
        response = self.client.post(
            reverse('users:buy_coins'),
            {'coins_amount': 500},
        )

        self.assertEqual(response.status_code, 302)

    def test_buy_coins_entry_created(self):
        self.client.login(username='prova', password='foo')

        user = self.User.objects.get(
            id=self.client.session.get('_auth_user_id'))
        self.assertEqual(user.coins, 0)

        response = self.client.post(
            reverse('users:buy_coins'),
            {'coins_amount': 500},
        )

        self.assertEqual(response.status_code, 200)

        user.refresh_from_db()
        self.assertEqual(user.coins, 500)

        coins_purchase = CoinsPurchase.objects.get(user=user)
        self.assertEqual(coins_purchase.coins, 500)

    def test_buy_coins_entry_created_invalid_amount(self):
        self.client.login(username='prova', password='foo')

        user = self.User.objects.get(
            id=self.client.session.get('_auth_user_id'))
        self.assertEqual(user.coins, 0)

        response = self.client.post(
            reverse('users:buy_coins'),
            {'coins_amount': -1},
        )

        self.assertEqual(response.status_code, 400)

        user.refresh_from_db()
        self.assertEqual(user.coins, 0)

        coins_purchase = CoinsPurchase.objects.filter(user=user)
        self.assertEqual(coins_purchase.count(), 0)

    def test_become_creator(self):
        Group.objects.create(name='creator')
        self.client.login(username='prova', password='foo')

        user = self.User.objects.get(
            id=self.client.session.get('_auth_user_id'))
        self.assertFalse(user.is_creator)

        response = self.client.post(
            reverse('users:become_creator'),
        )

        self.assertEqual(response.status_code, 200)

        user.refresh_from_db()
        self.assertTrue(user.is_creator)

    def test_become_creator_not_logged(self):
        response = self.client.post(
            reverse('users:become_creator'),
        )

        self.assertEqual(response.status_code, 302)

    def test_become_creator_already_creator(self):
        Group.objects.create(name='creator')
        self.client.login(username='prova', password='foo')

        user = self.User.objects.get(
            id=self.client.session.get('_auth_user_id'))
        user.is_creator = True
        user.save()

        response = self.client.post(
            reverse('users:become_creator'),
        )

        self.assertEqual(response.status_code, 400)

        user.refresh_from_db()
        self.assertTrue(user.is_creator)
