from django.db import models
from django.conf import settings
from account.models import Account


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=60, null=False, blank=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Date added")


class Subscription(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Word(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    source_word = models.CharField(max_length=60, null=False, blank=False)
    target_word = models.CharField(max_length=60, null=False, blank=False)


class WordDetails(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    value = models.IntegerField()
    is_learnt = models.BooleanField()


