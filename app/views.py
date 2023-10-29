from app import app, db
from flask import render_template, request, jsonify
from app.models import User

@app.route("/", methods=["GET"])
def home():
    users = db.session.query(User).all()
    return render_template("index.html", users=users)

@app.route("/submit", methods=["POST"])
def submit():
    global_user_object = User()

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]    

    email_exists = db.session.query(User).filter(User.email == email).first()
    # print(email_exists)
    # check if user email already exists in db
    if email_exists:
        pass
    else:
        user = User(first_name=first_name, last_name=last_name, email=email)
        db.session.add(user)
        db.session.commit()

        db.session.commit()
        global_user_object = user

    response = f"""
    <tr>
        <td>{first_name}</td>
        <td>{last_name}</td>
        <td>{email}</td>
        <td>
            <button class="btn btn-warning"
                hx-get="/get-edit-form/{global_user_object.user_id}">
                Edit User
            </button>
        </td>
        <td>
            <button hx-delete="/delete/{global_user_object.id}"
                class="btn btn-danger">
                Delete User
            </button>
        </td>
    </tr>
    """
    return response

@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return ""

@app.route("/get-edit-form/<int:id>", methods=["GET"])
def get_edit_form(id):
    user = User.query.get(id)

    response = f"""
    <tr hx-trigger='cancel' class='editing' hx-get="/get-user-row/{id}">
        <td><input name="first_name" value="{user.first_name}"/></td>
        <td>{user.first_name}</td>
        <td><input name="last_name" value="{user.last_name}"/></td>
        <td>{user.last_name}</td>
        <td><input name="email" value="{user.email}"/></td>
        <td>{user.first_name}</td>
        <td>
            <button class="btn btn-primary" hx-get="/get-user-row/{id}">
                Cancel
            </button>
            <button class="btn btn-success" hx-put="/update/{id}" hx-include="closest tr">
                Save
            </button>
        </td>
    </tr>
    """
    return response

@app.route("/get-user-row/<int:id>", methods=["GET"])
def get_user_row(id):
    user = User.query.get(id)

    response = f"""
    <tr>
        <td>{user.first_name}</td>
        <td>{user.last_name}</td>
        <td>{user.last_name}</td>
        <td>
            <button class="btn btn-warning"
                hx-get="/get-edit-form/{id}">
                Edit User
            </button>
        </td>
        <td>
            <button hx-delete="/delete/{id}"
                class="btn btn-danger">
                Delete User
            </button>
        </td>
    </tr>
    """
    return response

@app.route("/update/<int:id>", methods=["PUT"])
def update_user(id):
    db.session.query(User).filter(User.user_id == id).update({"first_name": request.form["first_name"],
                                                              "last_name": request.form["last_name"],
                                                              "email": request.form["email"]})
    db.session.commit()

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    user = USer.query.get(id)
    

    response = f"""
        <tr>
            <td>{user.first_name}</td>
            <td>{user.last_name}</td>
            <td>{user.last_name}</td>
            <td>
                <button class="btn btn-warning"
                    hx-get="/get-edit-form/{id}">
                    Edit User
                </button>
            </td>
            <td>
                <button hx-delete="/delete/{id}"
                    class="btn btn-danger">
                    Delete User
                </button>
            </td>
        </tr>
        """
    return response
    