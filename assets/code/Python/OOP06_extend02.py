class Person:
    def routine(self):
        result = self.eat()
        if hasattr(self, 'study'):
            result += self.study()
        result += self.sleep()
        return result

    def eat(self):
        return 'Person eats...'

    def sleep(self):
        return 'Person sleeps...'


class Student(Person):
    def study(self):
        return 'Student studies...'
