from django.test import TestCase
from django.urls import reverse

from course.models import Course
from account.models import Account


# Create your tests here.
class CourseTest(TestCase):

    @staticmethod
    def create_course(name="Test", description="Desc", source_lang="PL", target_lang="DE"):
        acc = Account.objects.create(username="John")
        return Course.objects.create(name=name, description=description,
                                     source_language=source_lang, target_language=target_lang,
                                     author=acc)

    def test_course_creation(self):
        course = self.create_course()
        self.assertTrue(isinstance(course, Course))
        self.assertTrue(course.__str__(), course.slug)

    def test_course_detail_view(self):
        course = self.create_course()
        url = reverse("course:detail", kwargs={'slug': course.slug})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)  # FOUND RESPONSE
