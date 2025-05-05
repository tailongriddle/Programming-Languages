

class Employee():

    def __init__(self, firstName, lastName, pay):
        self.firstName = firstName
        self.lastName = lastName
        self.pay = pay

    def __repr__(self):
        return self.firstName + " " + self.lastName

    def getPay(self):
        return self.pay
    