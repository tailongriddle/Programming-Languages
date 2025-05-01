from Employee import Employee

class Payroll():
    def __init__(self):
        self.emp = []

    def __repr__(self):
        return str(self.emp)
    
    def addEmp(self, e):
        self.emp.append(e)

    