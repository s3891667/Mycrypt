from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from mycrypt.token import *
from django.contrib.auth.models import User
from mycrypt.models import User
from mycrypt.token import *


class ForgotForm(forms.Form):

    name = forms.CharField(max_length=120)
    email = forms.EmailField()

    def get_info(self):
        """
        Method that returns formatted information
        :return: subject, msg
        """
        # Cleaned data
        cl_data = super().clean()

        name = cl_data.get('name').strip()
        email = cl_data.get('email')

        return name, email

    def send(self, current_site):
        name, email = self.get_info()
        user = User.objects.filter(userName=name)
        account = User.objects.get(userName=name)
        message = render_to_string('mycrypt/link.html', {
            'user': account,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(account.userName)),
            'token': tokenGener.make_token(account),
        })
        if user is not None:
            send_mail(
                subject='Mycrypt verification email',
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
            )
