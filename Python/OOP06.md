---
layout: page
title: Python OOP
subtitle: Phần 06: Giới thiệu về Single Inheritance (phần 1).
comments: true
---

* [List đầy đủ](https://votatdat.github.io/Python/Python_list) 
<br>
<br>

## 01. Single Inheritance
Thừa kế (inheritance) là một khái niệm trong lập trình hướng đối tượng OOP.
<br>Trong class sẽ có các property và method và những điều này sẽ được thừa kế để tạo nên thứ bậc.
<br>Chúng ta xem hình dưới:

![](./PIKs/OOP06_ hierarchy1.PNG)

Dấu mũi tên chỉ mối quan hện `IS-A` (dịch đại khái: là một), chẳng hạn như `Circle` is a `Ellipse` (Cirlce là một Ellipse).
<br>Các property và method trong các clas có thể được `inherit` (thừa kế), `extend` (mở rộng) hoặc `override` (ghi đè, hình như chỗ khác dịch là nạp chồng).
<br>Hình bên dưới là một vài thuật ngữ tiếng Anh, mình không dịch ra mà để nguyên.

![](./PIKs/OOP06_ hierarchy2.PNG)

Ở các ví dụ trên, một class con (children) chỉ thừa kế lại duy nhất một class cha (parent), nên gọi là `single inheritance` (đơn thừa kế), thực tế còn có `multiple inheritance` (đa thừa kế) là class con thừa kế từ nhiều class cha, vấn đề này chúng ta chưa đề cập ở đây.

![](./PIKs/OOP06_ hierarchy3.PNG)

Ở hình trên, chúng ta thấy s1 là một Student hoặc s1 là một instance của Student, và do Student thừa kế từ Person nên s1 cũng là một Person, hay s1 cũng là một instance của Person, nhưng s1 không là Teacher.

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



<br>
<br>
<br>
<br>
(Sẽ viết và cập nhật tiếp)
