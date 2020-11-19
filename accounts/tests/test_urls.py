from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import register, login_view, activate, profile, user_change_pass

class TestUrls(SimpleTestCase):
	def test_register_url_is_resolves(self):
		url = reverse('register')
		self.assertEquals(resolve(url).func, register)

	def test_login_url_is_resolves(self):
		url = reverse('login')
		self.assertEquals(resolve(url).func, login_view)
			
	def test_profile_url_is_resolves(self):
		url = reverse('profile')
		self.assertEquals(resolve(url).func, profile)

	def test_user_change_pass_url_is_resolves(self):
		url = reverse('changepass')
		self.assertEquals(resolve(url).func, user_change_pass)
