from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class PasswordResetTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='alice', email='alice@example.com', password='oldpass123')

    def test_password_reset_sends_email_and_allows_reset(self):
        # Request password reset
        resp = self.client.post(reverse('accounts:password_reset'), {'email': self.user.email})
        # should redirect to done page
        self.assertEqual(resp.status_code, 302)

        # An email should have been sent
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        # Subject should mention reset (case-insensitive)
        self.assertIn('reset', email.subject.lower())

        # Extract reset link from email body robustly
        import re
        from urllib.parse import urlparse

        # Try to find a full URL first
        u = re.search(r"https?://[^\s]+", email.body)
        if u:
            parsed = urlparse(u.group(0))
            path = parsed.path
        else:
            # Fallback: search for a path that contains 'reset'
            m = re.search(r"(/[^\s]*reset[^\s]*)", email.body)
            self.assertIsNotNone(m, 'No reset link found in email body')
            path = m.group(1)

        # Visit the password reset confirm page (GET) and follow redirects
        resp = self.client.get(path, follow=True)
        self.assertEqual(resp.status_code, 200)

        # Use the final path to post the new password (some setups redirect to a canonical URL)
        post_url = resp.request.get('PATH_INFO', path)
        resp = self.client.post(post_url, {'new_password1': 'newStrongPass1', 'new_password2': 'newStrongPass1'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        # Now login with new password
        login_ok = self.client.login(username=self.user.username, password='newStrongPass1')
        self.assertTrue(login_ok)

    def test_password_reset_uses_smtp_sender_when_smtp_backend_configured(self):
        # Ensure our custom SMTP sender is used when EMAIL_BACKEND is smtp
        from unittest.mock import patch
        from django.test import override_settings

        with override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'):
            with patch('accounts.forms.send_smtp_email') as mock_send:
                resp = self.client.post(reverse('accounts:password_reset'), {'email': self.user.email})
                # should redirect
                self.assertEqual(resp.status_code, 302)
                # our SMTP sender should have been called at least once
                self.assertTrue(mock_send.called)


class ProfileAndPasswordChangeTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='bob', email='bob@example.com', password='oldpass')

    def test_profile_view_and_update(self):
        self.client.login(username='bob', password='oldpass')
        resp = self.client.get(reverse('accounts:profile'))
        self.assertEqual(resp.status_code, 200)
        # update phone and location
        resp = self.client.post(reverse('accounts:profile'), {'username': 'bob', 'email': 'bob@example.com', 'phone': '12345', 'location': 'Nairobi'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone, '12345')
        self.assertEqual(self.user.location, 'Nairobi')

    def test_login_and_register_pages_have_password_reset_link(self):
        # login page contains forgot password link
        resp = self.client.get(reverse('login'))
        self.assertContains(resp, reverse('accounts:password_reset'))

        # register page contains forgot password link
        resp = self.client.get(reverse('register'))
        self.assertContains(resp, reverse('accounts:password_reset'))

    def test_base_contains_password_reset_modal(self):
        resp = self.client.get(reverse('home_page'))
        self.assertContains(resp, 'id="passwordResetModal"')

    def test_password_change_logged_in_user(self):
        self.client.login(username='bob', password='oldpass')
        resp = self.client.get(reverse('accounts:password_change'))
        self.assertEqual(resp.status_code, 200)
        # post change
        resp = self.client.post(reverse('accounts:password_change'), {
            'old_password': 'oldpass', 'new_password1': 'BrandNewPass1', 'new_password2': 'BrandNewPass1'
        }, follow=True)
        self.assertEqual(resp.status_code, 200)
        # ensure login works with new password
        self.client.logout()
        self.assertTrue(self.client.login(username='bob', password='BrandNewPass1'))
from django.test import TestCase

# Create your tests here.
