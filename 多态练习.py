

# 定义员工父类 Employee，继承 object（Python3 所有类默认继承 object，可省略）
class Employee(object):
    # 员工通用工作方法
    def work(self):
        # 基础员工工作行为
        print('working')


# 程序员子类，继承自员工 Employee
class Programmer(Employee):
    # 重写父类 work 方法，实现程序员专属的工作行为（多态特性）
    def work(self):
        print('-- working')


# 管理者子类，继承自员工 Employee
class Manager(Employee):
    # 重写父类 work 方法，实现管理者专属工作行为
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
