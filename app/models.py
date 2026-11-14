# -----------------------------------------
# Section 1: Import database object
# -----------------------------------------

from database import db


# -----------------------------------------
# Section 2: Department model
# -----------------------------------------

class Department(db.Model):

    # Connect to existing DEPT table
    __tablename__ = "DEPT"

    deptno = db.Column("DEPTNO", db.Integer, primary_key=True)
    dname = db.Column("DNAME", db.String(14))
    loc = db.Column("LOC", db.String(13))


# -----------------------------------------
# Section 3: Employee model
# -----------------------------------------

class Employee(db.Model):

    # Connect to existing EMP table
    __tablename__ = "EMP"

    empno = db.Column("EMPNO", db.Integer, primary_key=True)
    ename = db.Column("ENAME", db.String(10), nullable=False)
    job = db.Column("JOB", db.String(9))
    mgr = db.Column("MGR", db.Integer)
    hiredate = db.Column("HIREDATE", db.Date)
    sal = db.Column("SAL", db.Numeric(7, 2))
    comm = db.Column("COMM", db.Numeric(7, 2))

    deptno = db.Column(
        "DEPTNO",
        db.Integer,
        db.ForeignKey("DEPT.DEPTNO")
    )


    # -----------------------------------------
    # Section 4: Convert employee to dictionary
    # -----------------------------------------

    def to_dict(self):

        return {
            "empno": self.empno,
            "ename": self.ename,
            "job": self.job,
            "mgr": self.mgr,
            "hiredate": (
                self.hiredate.isoformat()
                if self.hiredate else None
            ),
            "sal": float(self.sal) if self.sal is not None else None,
            "comm": float(self.comm) if self.comm is not None else None,
            "deptno": self.deptno
        }
