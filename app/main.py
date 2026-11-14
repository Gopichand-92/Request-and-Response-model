# -----------------------------------------
# Section 1: Import required libraries
# -----------------------------------------

from flask import Flask, jsonify, request
from sqlalchemy.exc import SQLAlchemyError


from analysis import analyze_employee_salaries



from database import db, DATABASE_URL
from repositories import (
    get_all_employees,
    get_employee_by_id,
    create_employee
)


# -----------------------------------------
# Section 2: Create Flask application
# -----------------------------------------

app = Flask(__name__)

# Configure MySQL database
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL.render_as_string(
    hide_password=False
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Connect SQLAlchemy with Flask
db.init_app(app)


# -----------------------------------------
# Section 3: Home route
# -----------------------------------------

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "Employee API is running successfully"
    })


# -----------------------------------------
# Section 4: Get all employees
# -----------------------------------------

@app.route("/employees", methods=["GET"])
def employees():

    try:
        employee_list = get_all_employees()

        response = [
            employee.to_dict()
            for employee in employee_list
        ]

        return jsonify(response), 200

    except SQLAlchemyError:
        db.session.rollback()

        return jsonify({
            "error": "Unable to retrieve employees"
        }), 500


# -----------------------------------------
# Section 5: Get employee by ID
# -----------------------------------------

@app.route("/employees/<int:empno>", methods=["GET"])
def employee_by_id(empno):

    try:
        employee = get_employee_by_id(empno)

        if employee is None:
            return jsonify({
                "error": "Employee not found"
            }), 404

        return jsonify(employee.to_dict()), 200

    except SQLAlchemyError:
        db.session.rollback()

        return jsonify({
            "error": "Database error"
        }), 500


# -----------------------------------------
# Section 6: Create a new employee
# -----------------------------------------

@app.route("/employees", methods=["POST"])
def add_employee():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must contain JSON data"
        }), 400

    if not data.get("empno") or not data.get("ename"):
        return jsonify({
            "error": "Employee number and name are required"
        }), 400

    try:
        employee = create_employee(data)

        return jsonify({
            "message": "Employee created successfully",
            "employee": employee.to_dict()
        }), 201

    except (ValueError, TypeError, KeyError):
        db.session.rollback()

        return jsonify({
            "error": "Invalid employee data. Check the field values and date format."
        }), 400

    except SQLAlchemyError:
        db.session.rollback()

        return jsonify({
            "error": "Unable to save employee. Check for duplicate ID or invalid department."
        }), 400


    

@app.route("/analysis/salary", methods=["GET"])
def salary_analysis():

    try:
        result = analyze_employee_salaries()
        return jsonify(result), 200

    except SQLAlchemyError:
        db.session.rollback()

        return jsonify({
            "error": "Unable to analyze employee data"
        }), 500

# -----------------------------------------
# Section 7: Run Flask application
# -----------------------------------------

if __name__ == "__main__":

    app.run(debug=True)
