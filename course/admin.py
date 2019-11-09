from django.contrib import admin
from course.models import *

# Register your models here.
admin.site.register(Course)
admin.site.register(Word)
admin.site.register(WordDetails)
admin.site.register(Subscription)