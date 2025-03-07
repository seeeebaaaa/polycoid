from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django_hosts.resolvers import reverse
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from PIL import Image


# Function to send email verification
def send_verification_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_url = reverse('verify_email',host="filmliste", kwargs={'uidb64': uid, 'token': token})

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


def resize_image(image_path, size=(512, 512)):
    """Resizes an image to the specified size."""
    img = Image.open(image_path)
    img = img.convert("RGB")  # Ensures consistent image format
    img.thumbnail(size)  # Resize the image, keeping aspect ratio
    img.save(image_path)  # Overwrite the original file

