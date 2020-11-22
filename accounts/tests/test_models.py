from accounts.models import DumboUser
from django.test import TestCase
from accounts.models import Profile, DumboUser
#from django.contrib.auth.models import User

class DumboUser_test_case(TestCase):
    def setUp(self):
        super(DumboUser_test_case, self).setUp()
        #self.user_1 = DumboUser.objects.get(pk=1)
        #self.user_2 = DumboUser.objects.get(pk=1)

    def test_Dumbouser(self):
        user = DumboUser.objects.create(
                username = 'something'
            )
        #self.assertTrue(response.context['user'].is_active)
        #self.assertTrue(user.username.is_active)
        #self.assertTrue(user.username, )



"""
class Test_models(TestCase):
    def setUp(self):
    	
        self.credentials = {
            'username': 'testuser',
            'fullname' : 'rajesh',
            'password': 'secret@200173956',
            'phone_number' : 9999999999,
            'email' : 'test@gmail.com'}
        #print('----------')
        DumboUser.objects.create_user(**self.credentials)

    def test_DumboUser(self):
        # send login data
        response = self.client.post('/user/login/', self.credentials, follow=True)
        # should be logged in now
        #print(response.context)
        self.assertTrue(response.context['user'].is_active)
        #self.assertTemplateUsed(response, 'accounts/login.html')

#from django.test import TransactionTestCase, Client

class UserHistoryTest(TransactionTestCase):
    self.user = DumboUser.objects.create(username='rajesh', password='pass@123', email='admin@2001.com')
    self.client = Client() # May be you have missed this line

    def test_history(self):
        self.client.login(username=self.user.username, password='pass@123')
        # get_history function having login_required decorator
        response = self.client.post(reverse('get_history'), {'user_id': self.user.id})
        self.assertEqual(response.status_code, 200)



class test_model(TestCase):
    def test_profile_fields(self):
        profile = Profile()
        #profile.twitter_link = 'https://twitter.com/abcd12'
        profile.save()
        record = Profile.objects.get(pk = 1)
        self.assertEqual(record , Profile)

	def test_DumboUser_fields(self):
        user = DumboUser()
        #user.username = 'rajeshkumar'
        user.save()
        record = DumboUser.objects.get(pk = 1)
        self.a"ssertEqual(reco"rd , DumboUser)


	def setUp(self):
		self.user = DumboUser.objects.create(
			username = "abc123",
			password = 'password231',
			email = 'test@test.com',
			phone_number = 9999999987
		)

	def test_unauth_user(self):
		request.user = AnnonymousUser
		response = self.client.post('/user/login/', self.user, follow=True)
		self.assertTrue(response.context['user'].is_active)"""


