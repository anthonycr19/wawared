from celery.task import task


@task(name='notify password reset')
def notify_password_reset(user, new_password, change_password_url):
    from common.mail import Email
    email_data = {
        'template_name': 'perfiles/email/reset_password_notification.html',
        'context': {
            'user': user,
            'new_password': new_password,
            'change_password_url': change_password_url
        },
        'from_email': 'Wawared',
        'subject': 'Cambio de clave de usuario',
        'to': [user.email]
    }
    Email.send_email(**email_data)
