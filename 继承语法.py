# 定义一个动物园管理系统
"""
1.定义一个动物类class animal
2.猫类
3.狗类
方法重写
1.父类;动物叫的方法
2子类重写覆盖父类
3.子类调用方法
"""

class Animal(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def eat(self):
        # print('%s is eating'%self.name)
        print('%s is eating')

    def call(self):
        print('叫......')

class Cat(Animal):
    def __init__(self, name, age, sex):
        # self.name =name
        # self.age =age

        # super调用父类init方法
        super().__init__(name, age)
        self.sex = sex

    # def call(self):
    #     print('哈气.....')
    # pass
    def call(self):
        print(f'{self.name}----mmmm----')

class Dog(Animal):
    def __init__(self, name, age, sex):
        super(Dog,self).__init__(name, age)
        self.sex = sex
    def call(self):
        print(f'{self.name}---wwww----')

    # def call(self):
    #     print('大狗叫...')
    # pass

# cat =Cat()
cat = Cat('耄耋', 2, '女')
# print(cat)
cat.eat()
cat.call()

# dog =Dog()
dog = Dog('大狗', 2, '男')
dog.eat()
dog.call()

# print(Dog.__bases__)  # 看类
# print(Cat.__bases__)
