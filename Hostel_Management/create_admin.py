from app import app
from models import db, User

with app.app_context():

    existing_user = User.query.filter_by(
        username="admin"
    ).first()

    if existing_user:
        print("Admin account already exists.")
    else:
        admin = User(
            username="admin",
            password="admin123"
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin account created successfully!")
        print("Username: admin")
        print("Password: admin123")