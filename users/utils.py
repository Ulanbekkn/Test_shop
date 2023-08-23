from django.core.mail import EmailMessage

host_user = 'settings.EMAIL_HOST_USER'


def send_email(subject, body, to_email):
    from_email = host_user
    email = EmailMessage(subject, body, from_email, to_email)
    email.send()
