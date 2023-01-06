from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=50, blank=False, null=False)
    lastName = models.CharField(max_length=50, blank=False, null=False)
    # user_name = models.CharField(max_length = 50)
    email = models.EmailField(
        max_length=100, blank=False, null=False, unique=True)
    mobileNo = models.BigIntegerField(blank=False, null=False)
    password = models.CharField(max_length=300, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email + ' ' + self.firstName

    @property
    def fullName(self):
        return '%s %s' % (self.firstName.capitalize(), self.lastName.capitalize())


class Note(models.Model):
    title = models.CharField(max_length=1000, blank=False)
    secured_content = models.CharField(
        max_length=1000, blank=False, null=False)
    isset_Password = models.BooleanField(default=False)
    password = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_time = models.DateTimeField(blank=True, null=True)
    creator = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def set_PasswordEncrypt(txt):
        if txt == '':
            return None
        else:
            key = Fernet(settings.KEY)
            byteTxt = key.encrypt(txt.encode('utf8'))
            return byteTxt.decode('utf8')

    def set_PasswordDecrypt(txt):
        if txt is None:
            return None
        else:
            key = Fernet(settings.KEY)
            strTxt = key.decrypt(txt.encode('utf8'))
            return strTxt.decode('utf8')
