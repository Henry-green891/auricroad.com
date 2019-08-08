from django.core import mail
from django.test import TestCase
from django.urls import reverse

from wagtail.core.models import Site

from .models import Contact
from .views import error
from .wagtail_hooks import ContactFormSettings


class SimpleTest(TestCase):
    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_error_route(self):
        visit = lambda: self.client.get(reverse("error"))
        self.assertRaises(Exception, error)
        self.assertRaises(Exception, visit)

    def test_404(self):
        response = self.client.get("/sdfasdfsafsadf", follow=True)
        self.assertEqual(response.status_code, 404)


class ContactFormTest(TestCase):
    def setUp(self):
        self.contact_form_settings = ContactFormSettings.objects.create(
            site=Site.objects.first(),
            to_address=["test@test.com"],
            from_address="testfrom@test.com",
            subject="Test Subject",
        )
        self.form_data = {
            "first_name": ["Test"],
            "last_name": ["User"],
            "email": ["testuser@test.com"],
            "return_url": ["/hotels/"],
            "csrfmiddlewaretoken": [
                "1aq2gKtcqddEp0fgm7InnoZKN2TLyNMOITaKAgz708NVV7lucF4Hjt0EKZ2aBc18"
            ],
        }

    def test_form_submission(self):
        url = reverse("contact_form")
        response = self.client.post(url, self.form_data)
        self.assertEqual(response.url, "/hotels/")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(Contact.objects.first().email, self.form_data["email"][0])

    def test_bad_form_submission(self):
        del self.form_data["last_name"]
        url = reverse("contact_form")
        response = self.client.post(url, self.form_data)
        self.assertEqual(response.url, "/hotels/")
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(Contact.objects.count(), 0)
