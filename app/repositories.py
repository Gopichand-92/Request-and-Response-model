
# -----------------------------------------
# Section 1: Import required libraries
# -----------------------------------------

from datetime import datetime
from decimal import Decimal

from database import db
from models import Employee


# -----------------------------------------
# Section 2: Get all employees
# -----------------------------------------

def get_all_employees():

    employees = Employee.query.order_by(Employee.empno).all()

    return employees


# -----------------------------------------
# Section 3: Get employee by ID
# -----------------------------------------

def get_employee_by_id(empno):

    employee = db.session.get(Employee, empno)

    return employee


# -----------------------------------------
# Section 4: Save a new employee
# -----------------------------------------

def create_employee(data):

    # Convert date string into Python date
    hiredate = None

    if data.get("hiredate"):
        hiredate = datetime.strptime(
            data["hiredate"],
            "%Y-%m-%d"
        ).date()

    # Create employee object
    employee = Employee(
        empno=int(data["empno"]),
        ename=data["ename"],
        job=data.get("job"),
        mgr=int(data["mgr"]) if data.get("mgr") is not None else None,
        hiredate=hiredate,
        sal=Decimal(str(data["sal"])) if data.get("sal") is not None else None,
        comm=Decimal(str(data["comm"])) if data.get("comm") is not None else None,
        deptno=int(data["deptno"]) if data.get("deptno") is not None else None
    )

    # Save employee into MySQL
    db.session.add(employee)

    db.session.commit()

    return employee
