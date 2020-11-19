from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import DumboUserManager, DumboUser, Profile
import json

class TestViews(TestCase):

	def setUp(self):
		self.client = Client()
		#self.user = DumboUser.objects.create_user('kumar', 'rajeshkumar.p18@iiits.in', 'patta@2001')
		self.register_url = reverse('register')
		self.login_url = reverse('login')
		self.profile_url = reverse('profile')
		self.changepass_url = reverse('changepass')
		"""self.user = {
									'email':'testemail@gmail.com',
						            'username':'username',
						            'password':'password',
						            'fullname':'fullname'
								}
						        return super().setUp()
						"""


	def test_register_GET(self):

		response = self.client.get(self.register_url)

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'accounts/register.html')


	def test_login_view_GET(self):
		response = self.client.get(self.login_url)

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'accounts/login.html')

	"""def test_can_register_user(self):
			        response=self.client.post(self.register_url,self.user,format='text/html')
			        self.assertEqual(response.status_code,302)"""

	"""def test_profile_GET(self):
					response = self.client.get(self.profile_url)
									
					self.assertEquals(response.status_code, 200)
					self.assertTemplateUsed(response, 'accounts/profile_base.html')"""

	"""def test_user_change_pass_GET(self):
					response = self.client.get(self.changepass_url)
					self.client.login(username='kumar', password='patta@2001')
					self.assertEquals(response.status_code, 200)
					self.assertTemplateUsed(response, 'accounts/changepass.html')"""


	"""def test_can_register_user(self):
					response=self.client.post(self.register_url,self.user,format='text/html')
					self.assertEqual(response.status_code,302)"""


	  