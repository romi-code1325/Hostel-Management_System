from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


# =========================================================
# USER / ADMIN
# =========================================================

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )


# =========================================================
# STUDENT
# =========================================================

class Student(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    phone = db.Column(
        db.String(15)
    )

    course = db.Column(
        db.String(100)
    )

    room_number = db.Column(
        db.String(20)
    )


# =========================================================
# ROOM
# =========================================================

class Room(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    room_number = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    capacity = db.Column(
        db.Integer,
        nullable=False
    )

    occupied = db.Column(
        db.Integer,
        default=0
    )

    # Room image
    image = db.Column(
        db.String(200),
        default="room1.jpg"
    )


# =========================================================
# COMPLAINT
# =========================================================

class Complaint(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_name = db.Column(
        db.String(100),
        nullable=False
    )

    complaint = db.Column(
        db.Text,
        nullable=False
    )

    status = db.Column(
        db.String(30),
        default="Pending"
    )