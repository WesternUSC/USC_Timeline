import os
from usctimeline import create_app, db, bcrypt
from usctimeline.models import User

app = create_app()
with app.app_context():
    password = bcrypt.generate_password_hash(os.environ.get('USC_PASSWORD')).decode('utf-8')
    user = User(
        username='Nikolas',
        email='webdevelopment.intern@westernusc.ca',
        password=password
    )
    db.session.add(user)
    db.session.commit()
