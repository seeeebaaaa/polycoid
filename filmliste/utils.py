from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

# Function to send email verification
def send_verification_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    current_site = get_current_site(request)
    verification_link = reverse('filmliste:verify_email', kwargs={'uidb64': uid, 'token': token})
    verification_url = f"https://{current_site.domain}{verification_link}"

    subject = "Filmliste - Verify your email"
    message = render_to_string("filmliste/email_verification.html", {
        "user": user,
        "verification_url": verification_url
    })

    plain_content = strip_tags(message)
    mail = EmailMultiAlternatives(
        subject=subject,
        body=plain_content,
        from_email="no-reply@polycoid.com",
        to=[user.email]
    )
    mail.attach_alternative(message,"text/html")

    mail.send(fail_silently=False)
