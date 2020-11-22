from django.test import SimpleTestCase
from accounts.forms import UserUpdateForm, ProfileUpdateForm, DumboUserLoginForm
from documents.forms import UploadDocumentForm, DocumentUpdateForm, DownloadDocumentForm

class TestForm(SimpleTestCase):


	def test_UserUpdateForm_valid_data(self):
		form = UserUpdateForm(data = {
			'fullname': 'rajesh',
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

class test_document_forms(SimpleTestCase):

	def test_UploadDocumentForm_valid_data(self):
		form = UploadDocumentForm(data = {
			'name': 'rajesh',
			'is_important': True,
			'is_public': True,
			'path': 'gs://{bucket-name}/{file-path}'

		})
		#self.assertTrue(form.is_valid())

	def test_UploadDocumentForm_no_data(self):
		form = UploadDocumentForm(data = {})
		self.assertFalse(form.is_valid())
		self.assertEquals(len(form.errors), 2)

	def test_DocumentUpdateForm_valid_data(self):
		form = DocumentUpdateForm(data = {
			'is_important': True,
			'is_public': True,
			'expiry_date': 11/11/2020
			
		})
		#self.assertTrue(form.is_valid())

	def test_DocumentUpdateForm_no_data(self):
		form = DocumentUpdateForm(data = {})
		self.assertFalse(form.is_valid())
		self.assertEquals(len(form.errors), 1)

	def test_DownloadDocumentForm_valid_data(self):
		form = DownloadDocumentForm(data = {
			'document_id': 'rajesh123',
		})
		self.assertFalse(form.is_valid())

	def test_DownloadDocumentForm_no_data(self):
		form = DownloadDocumentForm(data = {})
		self.assertFalse(form.is_valid())
		self.assertEquals(len(form.errors), 2)



