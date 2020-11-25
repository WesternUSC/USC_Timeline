import os
import secrets
from flask import url_for, current_app
from flask_mail import Message
from usctimeline import mail
from usctimeline.models import Image


def save_img_to_file_system(img):
    """Saves image to filesystem.

    Args:
        img: Image file

    Returns:
        New instance of Image
    """
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(img.filename)
    filename = random_hex + file_ext
    directory = 'static/images/event'
    filepath = os.path.join(current_app.root_path, directory, filename)
    img.save(filepath)

    return Image(filename=filename)


def delete_img_from_file_system(img):
    filename = img.filename
    if os.path.isfile('./usctimeline/static/images/event/' + filename):
        os.remove('./usctimeline/static/images/event/' + filename)
        return True
    else:
        return False


def send_reset_email(user):
    """Sends email to user who requests password reset.

    Args:
        user: Instance of User

    Returns:
        None
    """
    token = user.get_reset_token()
    message = Message(
        'Password Reset Request',
        sender='noreply.westernusc.timeline@gmail.com',
        recipients=[user.email]
    )
    message.body = f'''
To reset your password, visit the following link:
{url_for('users.reset_password', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(message)
