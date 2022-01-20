from pydoc import resolve
from select import select
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import CustomUserCreationForm, DweetForm
from .views import registerPage



class CustomUserTests(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(
            username = 'testuser',
            email = 'test@mail.com',
            password = 'testpass123'
        )


        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@mail.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    
    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            username = 'superuser',
            email = 'super@mail.com',
            password = 'superpass123'
        )

        self.assertEqual(admin_user.username, 'superuser')
        self.assertEqual(admin_user.email, 'super@mail.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class DashboardTests(TestCase):

    def test_dashboard_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'dwitter/dashboard.html')
        self.assertNotContains(response, 'kalyanamkara ve papamkara')

    def test_dashboard_url_name(self):
        response = self.client.get(reverse('dwitter:dashboard'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/login/')
        self.assertTemplateUsed(response, 'dwitter/login.html')

    def test_dashboard_create_dweet_post(self):
        url = reverse('dwitter:dashboard')
        formdata = {'body':'hello'}
        response = self.client.post(url, formdata, format='text/html')
        self.assertEqual(response.status_code, 302)

class SignupPageTests(TestCase):
    def setUp(self):
        self.url = reverse('dwitter:register')
        self.response = self.client.get(self.url)
        self.user = {
            'usename':'testuser',
            'email':'test@mail.com',
            'password1':'testpass123',
            'password2':'testpass123'
        }

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'dwitter/register.html')
        self.assertContains(self.response, 'Sign up')
        self.assertNotContains(self.response, 'Hi there! I should not be on the page')


    def test_signup_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, CustomUserCreationForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')
    
    def test_can_register_user(self):
        response = self.client.post(self.url, self.user, format='text/html')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user)
    


    class TestForms(TestCase):
        def test_CustomUserForm_valid_data(self):
            form = CustomUserCreationForm(data={
                'username':'testform',
                'email':'form@mail.com',
                'password1':'formpassword',
                'password2':'formpassword'
            })
        
            self.assertEqual(form.is_valid())
        
        def test_DweetForm_valid_data(self):
            form = DweetForm(data={
                'body':'hello'
            })

            self.assertEqual(form.is_valid())


