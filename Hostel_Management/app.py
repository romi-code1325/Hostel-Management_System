from flask import Flask, render_template, request, redirect, url_for
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user
)

from models import db, User, Student, Room, Complaint


app = Flask(__name__)


# =========================================================
# CONFIGURATION
# =========================================================

app.config["SECRET_KEY"] = "hostel-management-secret-key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hostel.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# =========================================================
# DATABASE
# =========================================================

db.init_app(app)


# =========================================================
# LOGIN MANAGER
# =========================================================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))


# =========================================================
# LANDING PAGE
# =========================================================

@app.route("/")
def landing():

    return render_template("welcome.html")


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(
            username=username
        ).first()

        if user and user.password == password:

            login_user(user)

            return redirect(url_for("home"))

        return render_template(
            "login.html",
            error="Invalid username or password"
        )

    return render_template("login.html")


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("landing"))


# =========================================================
# SIGN UP
# =========================================================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        confirm_password = request.form["confirm_password"]


        # Check password

        if password != confirm_password:

            return render_template(
                "signup.html",
                error="Passwords do not match."
            )


        # Check existing username

        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:

            return render_template(
                "signup.html",
                error="Username already exists."
            )


        # Create new user

        new_user = User(
            username=username,
            password=password
        )

        db.session.add(new_user)

        db.session.commit()


        return redirect(url_for("login"))


    return render_template("signup.html")


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
@login_required
def home():

    student_count = Student.query.count()

    room_count = Room.query.count()

    complaint_count = Complaint.query.count()


    return render_template(
        "index.html",
        student_count=student_count,
        room_count=room_count,
        complaint_count=complaint_count
    )


# =========================================================
# STUDENTS
# =========================================================

@app.route("/students")
@login_required
def students():

    all_students = Student.query.all()

    all_rooms = Room.query.all()


    return render_template(
        "students.html",
        students=all_students,
        rooms=all_rooms
    )


@app.route("/add_student", methods=["POST"])
@login_required
def add_student():

    name = request.form["name"]

    email = request.form["email"]

    phone = request.form["phone"]

    course = request.form["course"]

    room_number = request.form["room_number"]


    new_student = Student(
        name=name,
        email=email,
        phone=phone,
        course=course,
        room_number=room_number
    )

    db.session.add(new_student)


    # Increase room occupancy

    if room_number:

        room = Room.query.filter_by(
            room_number=room_number
        ).first()

        if room and room.occupied < room.capacity:

            room.occupied += 1


    db.session.commit()


    return redirect(url_for("students"))


@app.route("/delete_student/<int:id>")
@login_required
def delete_student(id):

    student = Student.query.get_or_404(id)

    db.session.delete(student)

    db.session.commit()


    return redirect(url_for("students"))


# =========================================================
# ROOMS
# =========================================================

@app.route("/rooms")
@login_required
def rooms():

    all_rooms = Room.query.all()


    return render_template(
        "rooms.html",
        rooms=all_rooms
    )


@app.route("/add_room", methods=["POST"])
@login_required
def add_room():

    room_number = request.form["room_number"]

    capacity = int(request.form["capacity"])

    image = request.form["image"]


    new_room = Room(
        room_number=room_number,
        capacity=capacity,
        occupied=0,
        image=image
    )


    db.session.add(new_room)

    db.session.commit()


    return redirect(url_for("rooms"))

    room_number = request.form["room_number"]

    capacity = int(request.form["capacity"])


    new_room = Room(
        room_number=room_number,
        capacity=capacity,
        occupied=0
    )

    db.session.add(new_room)

    db.session.commit()


    return redirect(url_for("rooms"))


@app.route("/delete_room/<int:id>")
@login_required
def delete_room(id):

    room = Room.query.get_or_404(id)

    db.session.delete(room)

    db.session.commit()


    return redirect(url_for("rooms"))


# =========================================================
# COMPLAINTS
# =========================================================

@app.route("/complaints")
@login_required
def complaints():

    all_complaints = Complaint.query.all()


    return render_template(
        "complaints.html",
        complaints=all_complaints
    )


@app.route("/add_complaint", methods=["POST"])
@login_required
def add_complaint():

    student_name = request.form["student_name"]

    complaint_text = request.form["complaint"]


    new_complaint = Complaint(
        student_name=student_name,
        complaint=complaint_text,
        status="Pending"
    )

    db.session.add(new_complaint)

    db.session.commit()


    return redirect(url_for("complaints"))


@app.route("/resolve_complaint/<int:id>")
@login_required
def resolve_complaint(id):

    complaint = Complaint.query.get_or_404(id)

    complaint.status = "Resolved"

    db.session.commit()


    return redirect(url_for("complaints"))


@app.route("/delete_complaint/<int:id>")
@login_required
def delete_complaint(id):

    complaint = Complaint.query.get_or_404(id)

    db.session.delete(complaint)

    db.session.commit()


    return redirect(url_for("complaints"))


# =========================================================
# CREATE DATABASE
# =========================================================

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

    app.run(debug=True)