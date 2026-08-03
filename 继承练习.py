#person类,有name和age属性,eat()和sleep()方法
#student类,继承person类,新增score,重写str
#使用super()调用父类init方法
#定义一个老师类,上课方法,有name和age
class Person(object):
    def __init__(self,name,age):
        self.name =name
        self.age = age
    def eat(self):
        print("吃吃吃,吃死你")
    def sleep(self):
        print('今天又睡美了')

class Student(Person):
    def __init__(self,name,age,score):
        super().__init__(name,age)
        self.score = score
    def __str__(self):
        return f'名字{self.name},年龄{self.age},分数{self.score}'

class Teacher(object):
    def __init__(self,name,age):
        self.name =name
        self.age =age

    def today(self):
        print('来了有奖励,不来有惩罚')

stu =Student('MING',12,90)
# print(stu)
stu.eat()
stu.sleep()
tea =Teacher('LI',34)
# print(tea)
tea.today()