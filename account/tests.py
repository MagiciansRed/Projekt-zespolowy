from django.conf import settings
from django.test import TestCase

#from ProjektZespolowy import settings
from account.models import Account, MyAccountManager
from account.forms import RegistrationForm


# Create your tests here.
class AccountTest(TestCase):
    acc = Account.objects.filter(username="Tester")
    if acc:
        acc.delete()
    account = Account.objects.create(username="Tester", email="abc@def.gh")

    def test_account_creation(self):
        self.assertTrue(self.account, self.account.username)

    def test_valid_registration_form(self):
        acc = Account.objects.filter(username="Tester")
        if acc:
            acc.delete()

        data = {'username': "Tester", 'email': "abc@def.gh",
                'password1': "Qazxcvb111@", 'password2': "Qazxcvb111@"}

        form = RegistrationForm(data=data)
        self.assertTrue(form.is_valid())
