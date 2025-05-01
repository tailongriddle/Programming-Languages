from Employee import Employee
from Payroll import Payroll

# Make a payroll and add employees
pr = Payroll()
pr.addEmp(Employee("Peter", "Parker", 75000))
pr.addEmp(Employee("Clark", "Kent", 120000))
pr.addEmp(Employee("Diana", "Prince", 100000))
pr.addEmp(Employee("King", "T'Challa", 140000))
pr.addEmp(Employee("Carol", "Danvers", 150000))

print(pr)

if pr.total() == 75000 + 120000 + 100000 + 140000 + 150000:
    print("CORRECT TOTAL SUM: ", pr.total())
else:
    print("INCORRECT TOTAL SUM: ", pr.total())


