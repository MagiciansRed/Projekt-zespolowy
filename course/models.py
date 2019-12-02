from django.db import models
from django.conf import settings
from account.models import Account
from django.db.models.signals import pre_save
from django.utils.text import slugify


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=60, null=False, blank=False)
    description = models.CharField(default='This is a course description.', max_length=600, null=False, blank=False)
    image = models.ImageField(default='course_default.png', upload_to='course_banners')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Date added")
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.slug


class Subscription(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.course.name + "-" + self.user.username


class Word(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    source_word = models.CharField(max_length=60, unique=True, null=False, blank=False)
    target_word = models.CharField(max_length=60, null=False, blank=False)

    def __str__(self):
        return self.course.name + "-" + self.source_word


class WordDetails(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    value = models.IntegerField(default=0, null=True)
    is_learnt = models.BooleanField(null=True, default=False)

    def __str__(self):
        return self.word.source_word + "-" + self.user.username


def pre_save_course_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + instance.name)


pre_save.connect(pre_save_course_receiver, sender=Course)
