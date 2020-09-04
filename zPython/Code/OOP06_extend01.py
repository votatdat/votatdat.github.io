class Person:
    def routine(self):
        return self.eat() + self.study() + self.sleep()

    def eat(self):
        return 'Person eats...'

    def sleep(self):
        return 'Person sleeps...'


class Student(Person):
    def study(self):
        return 'Student studies...'
