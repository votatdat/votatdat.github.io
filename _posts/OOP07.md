---
layout: post
title: Python OOP
subtitle: Phần 07: Giới thiệu về Single Inheritance (phần 2).
tags: [Python, OOP]
comments: true
---

* [List đầy đủ](https://votatdat.github.io/Python/Python_list) 
<br>
<br>

## 01. Single Inheritance
Thừa kế (inheritance) là một khái niệm trong lập trình hướng đối tượng OOP.
<br>Trong class sẽ có các property và method và những điều này sẽ được thừa kế để tạo nên thứ bậc.

Chúng ta xem hình dưới:
![](./PIKs/OOP06_ hierarchy1.PNG)

Dấu mũi tên chỉ mối quan hệ `IS-A` (dịch đại khái: là một), chẳng hạn như `Circle` is a `Ellipse` (Cirlce là một Ellipse). Ngoài ra còn có mối quan hệ `has a` trong composition mà chúng ta chưa đề cập ở đây.

Hình bên dưới là một vài thuật ngữ tiếng Anh, mình không dịch ra mà để nguyên.
![](./PIKs/OOP06_ hierarchy2.PNG)

Ở các ví dụ trên, một class con (children class, derived class) chỉ thừa kế lại duy nhất một class cha (parent class, base class), nên gọi là `single inheritance` (đơn thừa kế), thực tế còn có `multiple inheritance` (đa thừa kế) là class con thừa kế từ nhiều class cha, vấn đề này chúng ta chưa đề cập ở đây.
![](./PIKs/OOP06_ hierarchy3.PNG)

Ở hình trên, chúng ta thấy s1 là một Student hoặc s1 là một instance của Student, và do Student thừa kế từ Person nên s1 cũng là một Person, hay s1 cũng là một instance của Person, nhưng s1 không là Teacher.

Các property và method trong các clas có thể được `inherit` (thừa kế), `extend` (mở rộng) hoặc `override` (ghi đè, hình như chỗ khác dịch là nạp chồng):
- `inherit` là khi class cha có property/method X nào đó, class con không cần viết lại mà sử dụng được luôn property/method X này.
- `extend` là khi class cha không có property/method X nào đó, viết mới property/method X này ở class con.
- `override` là class cha có property/method X nào đó, property/method X này lại được viết lại ở class con. Instance của class con sẽ sử dụng property/method X mới này.

Chúng ta nhắc lại về hàm `type()`, type(instance) sẽ trả về tên class của instance đó, chẳng hạn type(s1) sẽ trả về Student.
<br>Rõ ràng, hàm type() chỉ trả về class con tạo nên instace đó (là Student), chứ không trả về class cha (Person).
<br>Nhưng hàm `isintance()` sẽ trả về True nếu hỏi object đó có được tạo từ lớp cha hay không. Ví dụ:

```python
>>> class Person:
...
...     pass
...
>>> class Teacher(Person):
...     pass
...
>>> class Student(Person):
...     pass
...
>>> p1 = Person()
>>> t1 = Teacher()
>>> s1 = Student()
>>> type(t1)
<class '__main__.Teacher'>
>>> type(s1)
<class '__main__.Student'>
>>> isinstance(t1, Teacher)
True
>>> isinstance(t1, Person)
True
```

Ngoài ra còn hàm `issubclass()` để kiểm tra class này có phải subclass của class khác hay không, ví dụ:

```python
>>> class Person():
...     pass
...
>>> class Student(Person):
...     pass
...
>>> class CollegeStudent(Student):
...     pass
...
>>> issubclass(Student, Person)
True
>>> issubclass(CollegeStudent, Student)
True
>>> issubclass(CollegeStudent, Person)
True
```

Chúng ta thấy rằn khi định nghĩa một class trong Python, thì có vẻ như class không thừa kế từ class nào, chẳng hạn như class dưới:

```python
>>> class Person():
...     pass
...
```

Nhưng thực tế, mọi class đều thừa kế từ một class có tên `object`.

```python
>>> isinstance(Person, object)
True
>>>
```

## 02. Object class
Thực sư khi tạo một class, chúng ta sẽ thừa kế từ object, nhưng chúng ta có thể bỏ nó đi cho gọn:

```python
>>> class Person(object):
...     pass
...
```

Chính vì lí do trên, mà class nào tạo ra cũng thừa kế nhưng attribute và method có sẵn của object như: `__name__`, `__new__`, `__init__`, `__repr__`, `__hash__`, `__eq__`... Để coi object có sẵn những attribute gì, chúng ta dùng hàm `dir()`.

```python
>>> p = Person()
>>> p.__repr__
<method-wrapper '__repr__' of Person object at 0x0000012AAD348880>
>>> p.__hash__
<method-wrapper '__hash__' of Person object at 0x0000012AAD348880>
>>> p == p
True
```

```python
>>> dir(object)
['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', 
'__format__', '__ge__', '__getattribute__', '__gt__', 
'__hash__', '__init__', '__init_subclass__', '__le__', 
'__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', 
'__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
```

Ở những phần trước, chúng ta cũng đã biết class có kiểu type, nhưng thực ra object, int, str, dict... đều có kiểu type, do đó chúng là những class và cũng phải thừa kế từ object.

```python
>>> type(Person)
<class 'type'>
>>> type(object)
<class 'type'>
>>> type(int)
<class 'type'>
>>> type(list)
<class 'type'>
>>> type(str)
<class 'type'>
>>> issubclass(int, object)
True
>>> issubclass(dict, object)
True
```

Tuy nhiên, không phải chỉ có class mà ngay cả function cũng thừa kế từ object.

```python
>>> def my_func():
...     pass
...
>>> import types
>>> types.FunctionType is type(my_func)
True
>>> issubclass(types.FunctionType, object)
True
>>> isinstance(my_func,  object)
True
>>> isinstance(my_func, types.FunctionType)
True
```

Khi chúng ta dùng `==` để so sánh 2 instance với nhau mà không cần viết `__eq__` là vì `__eq__` đã được viết trong object.

```python
>>> p1 = Person()
>>> p2 = Person()
>>> p1 is p2, p1 == p2, p1 is p1, p1 == p1
(False, False, True, True)
```

Và vì chúng ta không viết `__eq__` nên id của nó trong class và trong object là như nhau:

```python
>>> id(Person.__eq__)
1282805080848
>>> id(object.__eq__)
1282805080848
>>> id(Person.__init__) == id(object.__init__)
True
```

Tuy nhiên, khi chúng ta viết `__init__` trong class là chúng ta đã override nó, id sẽ thay đổi:

```python
>>> class Person:
...     def __init__(self):
...             pass
...
>>> id(Person.__init__) == id(object.__init__)
False
```


## 03. Overriding
Class con thừa kế các attribute và method ở class cha, nhưng chúng ta có thể định nghĩa lại các điều này ở class con, cái này gọi là `overriding`.
![](./PIKs/OOP06_ override1.PNG)

Ở trên, `say_hello()` đã được override ở class Student, còn `say_bye()` thì được thừa kế.
<br> Tương tự, chúng ta coi ví dụ dưới:
![](./PIKs/OOP06_ override2.PNG)

Chúng ta thấy rằng, trong class Person, `__init__()` và `__repr__` đã override các hàm này ở object, class Student thừa kế lại class Person, và override `__repr__` từ Person, đồng thời thừa kế lại `__init__`.

Lưu ý rằng:
- Object thì có property `__class__` trả lại class mà tạo ra object này.
- Class thì có property `__name__` trả lại một string chưa tên của class.

Giả sử chúng ta có đoạn code dưới:

```python
class Person:
	def __init__(self, name):
		self.name = name
	
	def __repr__(self):
		return f'Person(name={self.name})'
		

class Student(Person):
	def __repr__(self):
		return f'Student(name={self.name})'
```

Nó hơi dài dòng, chúng ta có thể viết lại cho gọn hơn:

```python
class Person:
	def __init__(self, name):
		self.name = name
	
	def __repr__(self):
		return f'{self.__class__.__name__}(name={self.name})'


class Student(Person):
	pass
```

Ở [phần 03](https://votatdat.github.io/Python/OOP03), chúng ta đã so sánh `__repr__` và `__str__`, chúng ta đã thấy rằng `__repr__` sử dụng được cho tất cả các hàm `print()`, `str()` và `repr()` lẫn gọi instance trực tiếp, còn `__str__` chỉ dùng được cho hàm `print()` và `str()`. Tới đây chúng ta đã giải thích được: bằng cách nào đó, `__repr__` đã thừa kế cách gọi hàm `print()` và `str()` từ `__str__` và được viết thêm cách gọi hàm `repr()`.

Chúng ta xem thêm ví dụ ở dưới, để cẩn thận hơn khi sử dụng override, các bạn có thể download `OOP06_override01.py` về [ở đây](./code/OOP06_override01.py)

```python
class Shape:
    def __init__(self, name):
        self.name = name
        
    def info(self):
         return f'Shape.info called for Shape({self.name})'
    
    def extended_info(self):
        return f'Shape.extended_info called for Shape({self.name})'
    
class Polygon(Shape):
    def __init__(self, name):
        self.name = name  # we'll come back to this later in the context of using the super()
        
    def info(self):
        return f'Polygon info called for Polygon({self.name})'
```

Chúng ta import file vào rồi chạy thử:

```python
>>> from OOP06_override01 import Shape, Polygon
>>> p = Polygon('square')
>>> p.info()
'Polygon info called for Polygon(square)'
>>> p.extended_info()
'Shape.extended_info called for Shape(square)'
```

Điều này cũng không có gì lạ, p là instance của Polygon, khi gọi `info()` thì method này được override ở class Polygon nên giá trị trả về phải từ method này.
<br>Còn khi gọi `extended_info()` thì chúng ta không viết method này trong Polygon nên Polygon thừa kế lại từ Shape.
<br>Câu hỏi là: nếu chúng ta gọi `info()` ở bên trong `extended_info()` thì method `info()` nào sẽ được gọi?

Chúng ta edit một chút, lưu lại tên mới `OOP06_override02.py`, các bạn có thể download [ở đây](./code/OOP06_override02.py)

```python
class Shape:
    def __init__(self, name):
        self.name = name
        
    def info(self):
         return f'Shape.info called for Shape({self.name})'
    
    def extended_info(self):
        return f'Shape.extended_info called for Shape({self.name})', self.info() # Thêm chút xíu ở đây
    
class Polygon(Shape):
    def __init__(self, name):
        self.name = name  # we'll come back to this later in the context of using the super()
        
    def info(self):
        return f'Polygon info called for Polygon({self.name})'
```

```python
>>> from OOP06_override02 import Shape, Polygon
>>> p = Polygon('square')
>>> p.info()
'Polygon info called for Polygon(square)'
>>> p.extended_info()
('Shape.extended_info called for Shape(square)', 'Polygon info called for Polygon(square)')
```

Chúng ta thấy rằng, `info()` vẫn được gọi từ class con, dù được gọi ở class cha.
Đây là điểm phải hết sức chú ý khi viết override, khi object là instance của class con thì self sẽ là class con dù method được gọi nằm ở class cha.


## 04. Extending
Chúng ta đã đề cập `inherit` và `override`, chúng ta còn có thêm `extend` nữa. Một ví dụ đơn giản như ở dưới:

```python
class Person:
	pass

class Student(Person):
	def study():
		return "study…study…study"
```

Ở ví dụ trên, chúng ta thấy rằng class Student là class con của Person đã mở rộng thêm `study()`.
<br>Chúng ta có đoạn có như bên dưới:

```python
class Person:
    def routine(self):
        return self.eat() + self.study() + self.sleep()
        
    def eat(self):
        return 'Person eats...'
    
    def sleep(self):
        return 'Person sleeps...'
```

Chúng ta sẽ thấy vấn đề là chúng ta sẽ bị báo lỗi khi gọi `self.study()`. Chúng ta thử viết `study()` vào class Student là class con xem thử thế nào?

```python
class Student(Person):
    def study(self):
        return 'Student studies...'
```

Chúng ta lưu file này dưới tên OOP06_extend01.py, import rồi chạy thử xem thế nào, file này có thể down [ở đây](./Code/OOP06_extend01.py):

```python
>>> from OOP06_extend01 import Person, Student
>>> p = Person()
>>> p.routine()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "D:\BackEndLearning\DatBlog\Python\Code\OOP06_extend01.py", line 3, in routine
    return self.eat() + self.study() + self.sleep()
AttributeError: 'Person' object has no attribute 'study'
>>>
>>> s = Student()
>>> s.routine()
'Person eats...Student studies...Person sleeps...'
```

Kết quả này có lẽ không làm chúng ta ngạc nhiên, class Student không có `routine` nhưng nó thừa kế từ class Person, sau đó nó trả về 3 method `eat(), study()` và `sleep()`. 
<br>Vấn đề ở đây là **self thì sẽ trả về từ class nào?** Chúng ta thấy rằng `eat()` và `sleep` được viết ở class Person mà không được override ở class Student nên self chỗ này trả về là Person, còn `study()` thì được viết mới ở class Student nên self chỗ này trả về Student, lưu ý là thứ tự của `eat, study, sleep` vẫn được giữa nguyên.

Bây giờ chúng ta edit lại `routine()` trong class Person nhu ở dưới, save lại với file OOP06_extend01.py, rồi import chạy thử xem thế nào, file này có thể down [ở đây](./Code/OOP06_extend02.py):

```python
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

```

```python
>>> from OOP06_extend02 import Person, Student
>>> p = Person()
>>> p.routine()
'Person eats...Person sleeps...'
>>> s = Student()
>>> s.routine()
'Person eats...Student studies...Person sleeps...'
```

Chúng ta thấy kết quả vẫn như ở trên nhưng gọi `routine` của Person thì không bị lỗi nữa. 
<br>Vấn đều self thuộc class nào là vấn đề khá nguy hiểm khi viết code có thừa kế, các bạn xem thêm ví dụ dưới:

```python
class Account:
    apr = 3.0
    
    def __init__(self, account_number, balance):
        self.account_number = account_number
        self.balance = balance
        self.account_type = 'Generic Account'
        
    def calc_interest(self):
        return f'Calc interest on {self.account_type} with APR = {self.apr}'
        
class Savings(Account):
    apr = 5.0
    
    def __init__(self, account_number, balance):
        self.account_number = account_number  # Tạm thời chỗ này hơi dài dòng, sẽ giới thiệu sau.
        self.balance = balance
        self.account_type = 'Savings Account'
```

Chúng ta viết một class Account là về một tài khoản thông thường (Generic Account), có tỷ lệ lợi tức hàng năm (apr = annual percentage rate) là 3.0, chúng ta có `calc_interest()` để tính tiền lãi mỗi năm.
<br>Chúng ta lại có một class Savings, là một tài khoản tiết kiệm (Savings Account) mà tài khoản tiết kiệm thì có apr cao hơn so với tài khoản thông thường.
<br>Bây giờ chúng ta save lại với file OOP06_extend03.py, rồi import chạy thử xem thế nào, file này có thể down [ở đây](./Code/OOP06_extend03.py):

```python
>>> from OOP06_extend03 import Account, Savings
>>> s = Savings(234, 200)
>>> s.apr, s.account_type, s.calc_interest()
(5.0, 'Savings Account', 'Calc interest on Savings Account with APR = 5.0')
```

Chúng ta thấy kết quả đều chạy đúng, bây giờ chúng ta thay đổi một xíu ở `calc_interest()`: đổi **with APR = {self.apr}** thành **with APR = {Account.apr}**, save lại với file OOP06_extend04.py, rồi import chạy thử xem thế nào, file này có thể down [ở đây](./Code/OOP06_extend04.py):

```python
>>> from OOP06_extend04 import Account, Savings
>>> s = Savings(234, 200)
>>> s.apr, s.account_type, s.calc_interest()
(5.0, 'Savings Account', 'Calc interest on Savings Account with APR = 3.0')
>>>
```

Khi thay đổi như vậy, giá trị apr vẫn được override giá trị mới là 5.0, nhưng ở `calc_interest()` là lấy apr từ class Account vì ở đây nó được gán rõ ràng là **Account.apr**.
<br>Bây giờ, chúng ta thay đổi xíu nữa thay đổi **with APR = {Account.apr}** thành **with APR = {self.__class__.apr}**, save lại với file OOP06_extend05.py, rồi import chạy thử xem thế nào, file này có thể down [ở đây](./Code/OOP06_extend05.py):

```python
>>> from OOP06_extend05 import Account, Savings
>>> s = Savings(234, 200)
>>> s.apr, s.account_type, s.calc_interest()
(5.0, 'Savings Account', 'Calc interest on Savings Account with APR = 5.0')
```

Chúng ta thấy kết quả về lại như cũ ở trên, vậy **self.__class__.apr thì khác gì self.apr**?
<br>Chúng ta hãy xem lần lượt các ví dụ ở dưới:

```python
# Cái này sử dụng self.apr
>>> from OOP06_extend03 import Account, Savings
>>> s1 = Savings(123, 100)
>>> s2 = Savings(234, 200)
>>> s1.apr = 10
>>> s1.calc_interest(), s2.calc_interest()
('Calc interest on Savings Account with APR = 10', 
'Calc interest on Savings Account with APR = 5.0')
```

```python
# Cái này sử dụng self.__class__.apr
>>> from OOP06_extend05 import Account, Savings
>>> s1 = Savings(123, 100)
>>> s2 = Savings(234, 200)
>>> s1.apr = 10
>>> s1.calc_interest(), s2.calc_interest()
('Calc interest on Savings Account with APR = 5.0', 
'Calc interest on Savings Account with APR = 5.0')
```

Chúng ta thấy rằng **self.apr** thì cho phép override, còn **self.__class__.apr** thì luôn lấy giá trị apr của class đó, dù gán thêm bên ngoài thì giá trị này cũng không đổi. 
<br>Nếu chúng ta muốn an toàn luôn sử dụng giá trị apr được khai báo trong class thì nên dùng **self.__class__.apr**.
<br>Khi viết code chúng ta thường dùng `type(a)` thay cho `a.__class__`, như code trên **self.__class__.apr** sẽ được viết là **type(self).apr**.

Phần này tới đây là kết thúc, chúng ta sẽ tiếp tục Inheritance ở [phần 07](https://votatdat.github.io/Python/OOP07)
