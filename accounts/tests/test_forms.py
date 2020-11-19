from django.test import SimpleTestCase
from accounts.forms import UserUpdateForm, ProfileUpdateForm, DumboUserLoginForm

class TestForm(SimpleTestCase):
	"""def test_DumboUserLoginForm_valid_data(self):
					form = DumboUserLoginForm(data = {
						'identifier': 'jayachand',
						'password': 'chand@2001'
					})
			
					#self.assertTrue(form.is_valid())
			
				def test_DumboUserLoginForm_no_data(self):
					form = DumboUserLoginForm(data = {})
					self.assertFalse(form.is_valid())
					self.assertEquals(len(form.errors), 2)"""


	def test_UserUpdateForm_valid_data(self):
		form = UserUpdateForm(data = {
			'fullname': 'jayachand',
			'phone_number': 9999999999
		})

		self.assertTrue(form.is_valid())

	def test_UserUpdateForm_no_data(self):
		form = UserUpdateForm(data = {})
		self.assertFalse(form.is_valid())
		self.assertEquals(len(form.errors), 2)

	def test_ProfileUpdateForm_valid_data(self):
		form = ProfileUpdateForm(data = {
			'image': 'https://storage.googleapis.com/dumbo-document-storage/profile_pics/default.png',
			'twitter_link': 'https://twitter.com/abcd12'
		})

		self.assertTrue(form.is_valid())

	def test_ProfileUpdateForm_no_data(self):
		form = ProfileUpdateForm(data = {})
		self.assertFalse(form.is_valid())
		self.assertEquals(len(form.errors), 1)



