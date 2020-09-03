---
layout: page
title: Python OOP
subtitle: Phần 01: Giới thiệu về Class (phần 1)

comments: true
---

* [List đầy đủ](https://votatdat.github.io/Python/Python_list) 
<br>
<br>

(Có những cái mình phải để nguyên tiếng Anh vì mình không dịch được như class, object, attribute, function, method, class medthod, static method, property... các bạn thông cảm)

## 01. Object và Class
### Object (đối tượng) là gì?
Object (đối tượng) như một cái gì đó để chứa (container):
<br>•  Chứa `data` (dữ liệu) -> `state` (trạng thái) -> `attribute` (thuộc tính)
<br>•  Chứa `functionality` (chức năng) -> `behavior` (hành vi) -> `method` (phương thức)

Như một cái xe hơi `my_car`:
<br>•  Có `state` là: brand (thương hiệu), model (kiểu dáng), year (năm sản xuất)
<br>•  Có `behavior` là accelerate (tăng tốc), brake (thắng), steer (bẻ lái)

{% highlight python %}
my_car
	# state
	brand = Ferrari
	model = 599XX
	year = 2010
	
	# behavior
	accelerate
	brake
	steer
{% endhighlight %}

Chúng ta có thể dùng `dot notation` (dấu chấm) để truy cập/gán:

{% highlight python %}
my_car.brand ->  Ferrari
my_car.purchase_price = 1_600_000
my_car.accelerate(10)
my_car.steer(-15)
{% endhighlight %}

### Tạo Object
`Class` giống như một `template` (bản mẫu) để tạo `Object`:
<br>•  Mọi class đều có kiểu `type`.
<br>•  Object được tạo từ class được gọi là `instance` của class đó.

{% highlight python %}
>>> class MyClass:
...     pass
...
>>> type (MyClass)
<class 'type'>
>>> c = MyClass()
>>> type(c)
<class '__main__.MyClass'>
{% endhighlight %}

Ở ví dụ trên, chúng ta thấy class MyClass có kiểu `type`, `c` là một `object`, và là một `instance` của class MyClass (đó là lí do mà mình hay dùng object và instance khá lẫn lộn với nhau).


### Instance
Class có `behavior` -> class có thể được gọi (callable) -> khi được gọi, sẽ trả về `instance` của class đó, thường được gọi là object.
<br>Do đó, `instance` được tạo từ class, mà `type` (kiểu) của instance này là class mà nó được tạo.
<br>Ví dụ: *Myclass* là một class trong Python, *my_obj* là `instance` của class này: 

{% highlight python %}
>>> class MyClass():
...     pass
...
>>> my_obj=MyClass()
>>> type(my_obj)
<class '__main__.MyClass'>
>>> isinstance(my_obj, MyClass)
True
{% endhighlight %}

### Tạo Class
Ở những ví dụ phía trên, chúng ta đã tạo một class hết sức đơn giản:

{% highlight python %}
class MyClass():
	pass
{% endhighlight %}

Tuy đơn giản, nhưng class này đã tạo một object:
<br>•  Có tên MyClass
<br>•  Có kiểu `type`
<br>•  Tự động tạo ra vài `attributes` và `behavior`

{% highlight python %}
>>> class MyClass():
...     pass
...
>>> MyClass.__name__
'MyClass'
>>> MyClass()
<__main__.MyClass object at 0x000001618F670AF0>
>>> type(MyClass)
<class 'type'>
>>> isinstance(MyClass, type)
True
{% endhighlight %}


## 02. Class Attributes
### Định nghĩa
Định nghĩa `attributes` trong class:

{% highlight python %}
class MyClass:
	language = 'Python'
	version = '3.6'
{% endhighlight %}

`MyClass` là một class, nên nó là một object có kiểu type. Đồng thời cũng có nhiều `attributes` đã được tự động thêm, chẳng hạn `__name__`, `__module__`:
<br>Để coi hết `attribute` này, chúng ta dùng hàm **dir()**.

{% highlight python %}
>>> class MyClass:
...     pass
...
>>> type (MyClass)
<class 'type'>
>>> MyClass.__name__
'MyClass'
>>> MyClass.__module__
'__main__'
>>>
>>> dir(MyClass)
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__']
{% endhighlight %}

### Lấy giá trị từ attribute
**Cách 1**: dùng hàm `getattr`: **getattr(object_symbol, attribute_name, optional_default)**
<br>Nếu gọi một attribute, mà attribute đó không có trong class thì sẽ bị báo lỗi.

{% highlight python %}
>>> class MyClass:
...     language = 'Python'
...     version = '3.6'
...
>>> getattr(MyClass, 'language')
'Python'
>>> getattr(MyClass, 'x')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: type object 'MyClass' has no attribute 'x'
>>> getattr(MyClass, 'x', 'N/A')
'N/A'
{% endhighlight %}


**Cách 2**: dùng `dot notation` (dấu chấm)

{% highlight python %}
>>> MyClass.language
'Python'
>>> MyClass.x
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: type object 'MyClass' has no attribute 'x'
{% endhighlight %}

### Gán giá trị cho attribute
Cũng có 2 cách như trên, hàm sử dụng ở đây là `setatrr`: **setattr(object_symbol, attribute_name, attribute_value)**

{% highlight python %}
>>> setattr(MyClass, 'version', '3.7')
>>> MyClass.version
'3.7'
>>> MyClass.version = '3.8'
>>> MyClass.version
'3.8'
{% endhighlight %}

Nếu chúng ta set cho một `attribute` không tồn tại trong class, thì class sẽ tự tạo `attribute` mới.
<br>Chúng ta gán **setattr(MyClass, 'x', 100)** hoặc **MyClass.x = 100** thì class sẽ tạo attribute mới là x và gán giá trị 100.

### Nơi lưu trữ các state của class
Được lưu trong một `dictionary`.

{% highlight python %}
>>> class MyClass:
...     language = 'Python'
...     version = '3.6'
...
>>> MyClass.__dict__
mappingproxy({
	'__module__': '__main__', 
	'language': 'Python', #Ở đây
	'version': '3.6', #Ở đây
	'__dict__': <attribute '__dict__' of 'MyClass' objects>, 
	'__weakref__': <attribute '__weakref__' of 'MyClass' objects>, 
	'__doc__': None
})
{% endhighlight %}

Chúng ta thêm attribute x có giá trị 100, chúng ta xem lại sẽ thấy x được thêm vào cuối ở `mappingproxy`:

{% highlight python %}
>>> MyClass.x = 100
>>> MyClass.__dict__
mappingproxy({
	'__module__': '__main__', 
	'language': 'Python', 
	'version': '3.6', 
	'__dict__': <attribute '__dict__' of 'MyClass' objects>, 
	'__weakref__': <attribute '__weakref__' of 'MyClass' objects>, 
	'__doc__': None, 
	'x': 100, # Ở đây
})
{% endhighlight %}

### Xóa Attribute
Dùng hàm `delattr`:  **delattr(obj_symbol, attribute_name)** hoặc từ khóa `del`: delattr(MyClass, 'version') hoặc del MyClass.version

### Truy cập Namespace trực tiếp
Khi dùng `__dict__`, thì class sẽ trả về `mappingproxy` là một `dictionary`, nên có thể truy cập trực tiếp từ dict này.

{% highlight python %}
>>> MyClass.__dict__['language']
'Python'
{% endhighlight %}

Vậy là tới nay chúng ta có 3 cách truy cập giá trị của một attribute:
1. MyClass.language
2. getattr(MyClass, 'language')
3. MyClass.\_\_dict\_\_\['language'\]

Chúng ta nên sử dụng cách 1, 2. Cách 3 có thể sẽ gây sai sót.


## 03. Callable Attribute
Ở trên, chúng ta đã định nghĩa về `attribute`, ở đây chúng ta sẽ có thêm định nghĩa về `callable attribute` ám chỉ những attribute mà chúng ta có thể gọi lên được.

{% highlight python %}
>>> class MyClass:
...     language = 'Python'
...     def say_hello():
...             print('Hello world!')
...
>>> MyClass.__dict__
mappingproxy({
	...
	'language': 'Python', 
	'say_hello': <function MyClass.say_hello at 0x000001C759768A60>, # mới
	...
{% endhighlight %}


Chúng ta có 3 cách gọi:

{% highlight python %}
# Cách 1
>>> my_func = MyClass.__dict__['say_hello']
>>> my_func()
Hello world!

>>> MyClass.__dict__['say_hello']()
Hello world!
# Cách 2
>>> getattr(MyClass, 'say_hello')()
Hello world!
# Cách 3
>>> MyClass.say_hello()
Hello world!
{% endhighlight %}

## 04. Classes are callable
Khi chúng ta dùng từ khóa class, thì Python đã tự động làm những điều sau:
- Nó biến class thành `callable`
- Giá trị là trả lại là 1 object, kiểu của object là class đó.

{% highlight python %}
>>> my_obj = MyClass()
>>> type(my_obj)
<class '__main__.MyClass'>
>>> isinstance(my_obj, MyClass)
True
{% endhighlight %}

Khi gán **my_obj = MyClass()** chúng ta gọi là khởi tạo (`instantiation`).
<br>Python tự tạo các attribute cho chúng ta:
- `__dict__`: cho chúng ta biết local namespace của object
- `__class__`: cho chúng ta biết class nào được sử dụng để khởi tạo object

{% highlight python %}
>>> my_obj.__dict__
{}
>>> my_obj.__class__
<class '__main__.MyClass'>
{% endhighlight %}


## 05. Data Attribute
Chúng ta coi ví dụ dưới:

{% highlight python %}
>>> class MyClass:
...     language = 'Python'
...
>>> my_obj = MyClass()
>>> MyClass.__dict__
mappingproxy({
	'__module__': '__main__', 
	'language': 'Python', 
	'__dict__': <attribute '__dict__' of 'MyClass' objects>, 
	'__weakref__': <attribute '__weakref__' of 'MyClass' objects>, 
	'__doc__': None})
>>>	
>>> my_obj.__dict__
{}
>>>
{% endhighlight %}

Vì `__dict__` cho chúng ta biết local namespace của object, nên MyClass sẽ có đầy đủ các attribute tạo sẵn từ Python, còn my_obj sẽ không có gì.
<br>Khi chúng ta gọi **MyClass.language** thì Python sẽ tìm kiếm language trong `MyClass namespace`, đó là MyClass.language và in ra 'Python'.
<br>Còn khi chúng ta gọi **my_obj.language** thì Python sẽ tìm kiếm language trong `my_obj namespace`, nếu tìm ra sẽ trả về giá trị.
<br>Nếu tìm không ra, sẽ tìm tiếp trong type (class) của my_obj, nó là MyClass và trả về 'Python'.

Chúng ta xem thêm ví dụ dưới:

{% highlight python %}
>>> MyClass.language
'Python'
>>> my_obj.__dict__
{}
>>>
>>> my_obj.language = 'Java'
>>> my_obj.__dict__
{'language': 'Java'}
>>> my_obj.language
'Java'
>>> MyClass.language
'Python'
>>>
>>> other_obj = MyClass()
>>> other_obj.__dict__
{}
>>> other_obj.language
'Python'
{% endhighlight %}

`language` là attribute của cả MyClass và my_obj, nhưng ở MyClass `language` là **Class Attribute**, còn ở my_obj thì `language` là **Instance Attribute**.

## 06. Function Attribute
Chúng ta coi ví dụ ở dưới:

{% highlight python %}
>>> class MyClass:
...     def say_hello():
...             print('Hello World!')
...
>>> my_obj = MyClass()
>>>
>>> MyClass.say_hello
<function MyClass.say_hello at 0x0000022DAC108A60>
>>>
>>> my_obj.say_hello
<bound method MyClass.say_hello of <__main__.MyClass object at 0x0000022DABF10AF0>>
>>> MyClass.say_hello()
Hello World!
>>>
>>> my_obj.say_hello()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: say_hello() takes 0 positional arguments but 1 was given
{% endhighlight %}

Chúng ta thấy, đối với MyClass thì say_hello là **function**, còn đồi với my_obj thì nó là **bound method**.
<br>Tương tự, khi gọi MyClass.say_hello() thì nó in ra 'Hello World!', nhưng gọi my_obj.say_hello() nó lại báo lỗi thiếu arguments.

Tới đây chúng ta nhận ra được sự khác nhau giữa `function` và `method`: method cũng là function, nhưng nó bị cột (bound) với một object nào đó, và object đó được đưa vào method như argument đầu tiên.
<br>Khi gọi **my_obj.say_hello()** thì say_hello là một method, được cột vào my_obj, khi gọi như vậy thì my_obj là parameter đầu tiên được đưa vào method say_hello.
<br>Do đó **my_obj.say_hello()** sẽ tương đương với  **MyClass.say_hello(my_obj)**, nhưng khai báo say_hello ở trên không có argument nào, nên Python sẽ báo lỗi.

Cũng như các object khác, method cũng có các attribute như `__self__`, `__func__`:
<br>Khi gọi **obj.method(args)** sẽ tương đương với **method.__func__(method.__self__, args)**.

{% highlight python %}
class Person:
	def hello(self): # p.hello.__func__
		pass


p = Person() # p.hello.__self__
{% endhighlight %}

Chúng ta coi thêm ví dụ bên dưới, chúng ta thêm obj vào say_hello:

{% highlight python %}
>>> class MyClass:
...     def say_hello(obj): #tại thời điểm này nó vẫn là function
...             print('Hello World!')
...
>>> my_obj = MyClass()
>>> my_obj.say_hello #tại thời điểm này, nó trở thành method, bị cột vào my_obj
<bound method MyClass.say_hello of <__main__.MyClass object at 0x000001BB796D0AF0>>
>>> my_obj.say_hello()
Hello World!
>>> MyClass.say_hello(my_obj)
Hello World!
{% endhighlight %}

Ở ví dụ bên dưới, chúng ta thêm arg cho say_hello:

{% highlight python %}
>>> class MyClass:
...     language = 'Python'
...     def say_hello(obj, name):
...             return f'Hello {name}! I am {obj.language}. '
...
>>> python = MyClass()
>>> python.say_hello('John')
'Hello John! I am Python. '
>>> MyClass.say_hello(python, 'John')
'Hello John! I am Python. '
>>>
>>> java = MyClass()
>>> java.language = 'Java'
>>> java.say_hello('John')
'Hello John! I am Java. '
>>> MyClass.say_hello(java, 'John')
'Hello John! I am Java. '
{% endhighlight %}


Phần này tới đây là hết, chúng ta sẽ nói tiếp về Class ở [phần 02](https://votatdat.github.io/Python/OOP02).

{% highlight python %}

{% endhighlight %}