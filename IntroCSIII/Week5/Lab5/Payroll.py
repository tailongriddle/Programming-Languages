from Employee import Employee

class Payroll():
    def __init__(self):
        self.emp = []

    def __repr__(self):
        return str(self.emp)
    
    def addEmp(self, e):
        self.emp.append(e)

    def total(self):
        total = 0
        for e in self.emp:
            total = total + e.getPay()   
        return total