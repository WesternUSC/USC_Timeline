import os
import secrets
from flask import url_for, current_app
from flask_mail import Message
from usctimeline import mail

def save_img_to_file_system(img, dir) -> str:
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(img.filename)
    filename = random_hex + file_ext
    directory = f'static/images/{dir}'
    filepath = os.path.join(current_app.root_path, directory, filename)
    img.save(filepath)

    return filename


def send_reset_email(user):
    token = user.get_reset_token()
    message = Message(
        'Password Reset Request',
        sender='noreply@demo.com',
        recipients=[user.email]
    )
    message.body = f'''
To reset your password, visit the following link:
{url_for('users.reset_password', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(message)
