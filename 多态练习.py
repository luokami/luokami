
class Employee(object):
    def work(self):
        print('working')


class Programmer(Employee):
    def work(self):
        print('-- working')


class Manager(Employee):
    def work(self):
        print('u working')


class Company(object):
    # 传入不同的对象，执行不同的代码，即不同的work函数。
    def start_work(self, employee):
        employee.work()
        # self.work()


pro = Programmer()
manager = Manager()
comp = Company()
comp.start_work(pro)
comp.start_work(manager)
