# -----------------------------------------
# Section 1: Import required libraries
# -----------------------------------------

import pandas as pd
import numpy as np

from sqlalchemy import text

from database import db


# -----------------------------------------
# Section 2: Get employee data from MySQL
# -----------------------------------------

def get_employee_dataframe():

    query = text("""
        SELECT EMPNO, ENAME, SAL, DEPTNO
        FROM EMP
    """)

    dataframe = pd.read_sql_query(
        query,
        db.engine
    )

    return dataframe


# -----------------------------------------
# Section 3: Analyze employee salaries
# -----------------------------------------

def analyze_employee_salaries():

    # Retrieve data from database
    df = get_employee_dataframe()

    # Check whether data exists
    if df.empty:
        return {
            "message": "No employee records found"
        }

    # Convert salary column into numeric values
    salaries = pd.to_numeric(
        df["SAL"],
        errors="coerce"
    ).dropna()

    if salaries.empty:
        return {
            "message": "No salary values found"
        }

    # NumPy calculations
    salary_array = salaries.to_numpy()

    average_salary = np.mean(salary_array)
    maximum_salary = np.max(salary_array)
    minimum_salary = np.min(salary_array)
    standard_deviation = np.std(salary_array)

    # Pandas calculations
    department_count = df["DEPTNO"].nunique()

    return {
        "total_employees": int(len(df)),
        "average_salary": round(float(average_salary), 2),
        "maximum_salary": float(maximum_salary),
        "minimum_salary": float(minimum_salary),
        "standard_deviation": round(float(standard_deviation), 2),
        "total_departments": int(department_count)
    }
