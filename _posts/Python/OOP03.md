---
layout: page
title: Python OOP
subtitle: Phần 03: Giới thiệu về Polymorphism và special methods (phần 1).
comments: true
---

* [List đầy đủ](https://votatdat.github.io/Python/Python_list) 
<br>
<br>

## 01. \_\_str\_\_ và \_\_repr\_\_
Cả 2 method này đều tạo ra string để hiện thị cho một object. Chúng ta xem các ví dụ dưới:

```python
>>> class Person:
...     pass
...
>>> p = Person()
>>> p
<__main__.Person object at 0x000001BD91420AF0>
>>> print(p)
<__main__.Person object at 0x000001BD91420AF0>
>>> str(p)
'<__main__.Person object at 0x000001BD91420AF0>'
>>> repr(p)
'<__main__.Person object at 0x000001BD91420AF0>'
>>>
```

Khi không có \_\_repr\_\_ hay \_\_str\_\_ thì khi gọi object, chúng ta chỉ được địa chỉ trên bộ nhớ của object đó.
<br>Bây giờ, chúng ta thêm \_\_repr\_\_:
<br>

```python
>>> class Person2:
...     def __repr__(self):
...             print('__repr__ is called.')
...             return 'This is Person2 class'
...
>>> p2 = Person2()
>>> p2
__repr__ is called.
This is Person2 class
>>> print(p2)
__repr__ is called.
This is Person2 class
>>> str(p2)
__repr__ is called.
'This is Person2 class'
>>> repr(p2)
__repr__ is called.
'This is Person2 class'
```

Khi thêm method \_\_repr\_\_ thì chúng ta có thể dùng các function như **print**, **repr**, hay **str**, kết quả giống như gọi trực tiếp object.
<br>Bây giờ, chúng ta thêm \_\_str\_\_ nữa:
<br>

```python
>>> class Person3:
...     def __repr__(self):
...             print('__repr__ is called.')
...             return 'This is Person3 class'
...     def __str__(self):
...             print('__str__ is called.')
...             return Person3.__name__
...
>>> p3 = Person3()
>>> p3
__repr__ is called.
This is Person3 class
>>> print(p3)
__str__ is called.
Person3
>>> str(p3)
__str__ is called.
'Person3'
>>> repr(p3)
__repr__ is called.
'This is Person3 class'
```

Chúng ta thấy khi gọi p3 trực tiếp hoặc hàm repr thì \_\_repr\_\_ được gọi, còn dùng hàm print hoặc str thì \_\_str\_\_ được gọi.
<br>Khi không viết method \_\_str\_\_ trong class thì gọi trực tiếp lẫn dùng 3 hàm print, str và repr đều gọi method \_\_repr\_\_.
<br>Vậy chuyện gì xảy ra khi chỉ viết \_\_str\_\_ mà không viết \_\_repr\_\_?


```python
>>> class Person4:
...     def __str__(self):
...             print('__str__ is called.')
...             return Person4.__name__
...
>>> p4 = Person4()
>>> p4
<__main__.Person4 object at 0x000001BD91962C70>
>>> print(p4)
__str__ is called.
Person4
>>> str(p4)
__str__ is called.
'Person4'
>>> repr(p4)
'<__main__.Person4 object at 0x000001BD91962C70>'
>>>
```

Chúng ta thấy rằng \_\_repr\_\_ sử dụng được cho tất cả, còn \_\_str\_\_ chỉ dùng được cho hàm print và str. Chúng ta sẽ nói về inheritance (thừa kế) sau.
<br>Ngoài print và str ra, còn vài hàm sử dung \_\_str\_\_ như ở dưới:

```python
>>> f'{p4}'
__str__ is called.
>>>
'Person4'
>>> '{}'.format(p4)
__str__ is called.
'Person4'
>>>
>>> '%s' % p4
__str__ is called.
'Person4'
```

<br>
## 02. Các toán tử số học
Một vài phép toán cơ bản:

```python
__add__: +
__sub__: -
__mul__: *
__truediv__: /
__floordiv__: //
__mod__: %
__pow__: **
```
Chẳng hạn như khi thực hiện a + b, thì Python sẽ thực hiện `a.__add__(b)`, và sẽ trả về **NotImplemented** nếu a và b không cùng kiểu.

```python
>>> a = 1
>>> b = 'text'
>>> a + b
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for +: 'int' and 'str'
>>> a.__add__(b)
NotImplemented
```

Khi này Python sẽ swap 2 toán tử và thử: `b.__radd__(a)`, ngoài ra còn có:

```python
__radd__ 
__rsub__ 
__rmul__
__rtruediv__ 
__rfloordiv__ 
__rmod__
__rpow__
```

Một vài phép toán khác:

```python
__iadd__: +=
__isub__: -=
__imul__: *=
__itruediv__: /=
__ifloordiv__: //=
__imod__: %=
__ipow__: **=
__neg__: -a
__pos__: +a
__abs__: abs(a)
```

Chúng ta đọc đoạn code như ở dưới, lưu thành file `OOP03_vector01.py`, ở đây chúng ta chỉ mới xây dựng một class Vector với chỉ phép cộng và trừ:
Các bạn có thể download file này [ở đây](./Code/OOP03_vector01.py).

```python
class Vector:
    def __init__(self, *components):
        # validate number of components is at least one, and all of them are real numbers
        if len(components) < 1:
            raise ValueError('Cannot create an empty Vector.')
        for component in components:
            if not isinstance(component, Real):
                raise ValueError(f'Vector components must all be real numbers - {component} is invalid.')
        
        # use immutable storage for vector
        self._components = tuple(components)
        
    def __len__(self):
        return len(self._components)
        
    @property
    def components(self):
        return self._components
    
    def __repr__(self):
        # works - but unwieldy for high dimension vectors
        return f'Vector{self._components}'
    
    def validate_type_and_dimension(self, v):
        return isinstance(v, Vector) and len(v) == len(self)
            
    def __add__(self, other):
        if not self.validate_type_and_dimension(other):
            return NotImplemented
        components = (x + y for x, y in zip(self.components, other.components))
        return Vector(*components)
            
    def __sub__(self, other):
        if not self.validate_type_and_dimension(other):
            return NotImplemented
        components = (x - y for x, y in zip(self.components, other.components))
        return Vector(*components)
```

Chúng ta import và chạy thử vài ví dụ:

```python
>>> from OOP03_vector01 import Vector
>>> v1 = Vector(1, 2)
>>> v2 = Vector(10, 10)
>>> v3 = Vector(1, 2, 3, 4)
>>> v1
Vector(1, 2)
>>> v1 + v2
Vector(11, 12)
>>> v2 + v1
Vector(11, 12)
>>> v1 + v3
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for +: 'Vector' and 'Vector'
>>> v1 + 100
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for +: 'Vector' and 'int'
>>> v1*2
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for *: 'Vector' and 'int'
```

Bây giờ chúng ta thêm phép nhân, lưu lại với tên `OOP03_vector02.py`, các bạn có thể download file này [ở đây](./Code/OOP03_vector02.py):

```python
class Vector:
.....
.....
	def __mul__(self, other):
        print('__mul__ called...')
        if not isinstance(other, Real):
            return NotImplemented
        components = (other * x for x in self.components)
        return Vector(*components)
```

Chúng ta thử vài ví dụ:

```python
>>> from OOP03_vector02 import Vector
>>> v1 = Vector(1, 2)
>>> v1 * 10
__mul__ called...
Vector(10, 20)
>>> 10 * v1
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for *: 'int' and 'Vector'
```

Đến lúc này, chúng ta phải cần `__rmul__` cho phép nhân, lưu lại với tên `OOP03_vector03.py`, các bạn có thể download file này [ở đây](./Code/OOP03_vector03.py).

```python
class Vector:
.....
.....
	def __rmul__(self, other):
        print('__rmul__ called...')
        # for us, multiplication is commutative, so we can leverage our existing __mul__ method
        return self * other
```

Chúng ta thử lại:

```python
>>> from OOP03_vector03 import Vector
>>> v1 = Vector(1, 2)
>>> v1 * 10
__mul__ called...
Vector(10, 20)
>>> 10 * v1
__rmul__ called...
__mul__ called...
Vector(10, 20)
```

Chúng ta có thể thêm tích vô hướng (dot product), tích hữu hướng (cross product) cho 2 Vector, lưu lại với tên `OOP03_vector04.py`, các bạn có thể download file này [ở đây](./Code/OOP03_vector04.py). Các bạn tự thử vài ví dụ nhé.

Tiếp theo chúng ta nói về toán tử `in-place`, toán tử này dùng để thay đổi object phía trái biểu thức, ví dụ:

```python
>>> l = [1, 2]
>>> id(l)
2319173481536
>>> l += [3]
>>> id(l)
2319173481536
>>> l
[1, 2, 3]
>>>
```

Chúng ta thấy rằng, `l` thì thay đổi nhưng `id` của `l` không thay đổi.
<br>Chúng ta xem ví dụ dưới:

```python
>>> l = [1, 2]
>>> id(l)
2327813172160
>>> l = l + [3]
>>> id(l)
2327813485568
>>> l
[1, 2, 3]
```

Chúng ta thấy rằng dù **l += \[3\]** và **l = l + \[3\]** cho kết quả l giống nhau, nhưng toán tử `+=` vẫn giữ ở object l như cũ, trong khi toán tử `+` tạo ra object l mới. Tuy nhiên, điều này đúng với list, nhưng không đúng với tuple.

```python
>>> t = (1, 2)
>>> id(t)
2137968148992
>>> t += (3, )
>>> id(t)
2137967871808
>>> t
(1, 2, 3)
```

Điều trên cũng tương tự với string, integer, fload..., lí do list là mutable (có thể thay đổi) còn tuple, string, integer ... là immutable (không thể thay đổi). Vì không thể thay đổi nên nó phải tạo object mới, không thể đè lên object ban đầu.

Trong đoạn code ở trên, nếu muốn thêm toán tử += cho 2 vector mà không muốn tạo mới object v1 thì có thể thêm đoạn code sau vào, [file cuối](./Code/OOP03_vector05.py):

```python
.....
	def __iadd__(self, other):
        print('__radd__ called...')
        if self.validate_type_and_dimension(other):
            components = (x + y for x, y in zip(self.components, other.components))
            self._components = tuple(components)  # mutating our Vector object
            return self # don't forget to return the result of the operation!
        return NotImplemented
```

Các toán tử số học không chỉ giới hạn chỉ làm việc với con số, nó có thể dùng cho string, ví dụ file [này](./Code/OOP03_family.py):

```python
class Person:
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return f"Person('{self.name}')"
		
		
class Family:
    def __init__(self, mother, father):
        self.mother = mother
        self.father = father
        self.children = []
        
    def __iadd__(self, other):
        self.children.append(other)
        return self
```

Chúng ta import vào rồi test thử:

```python
>>> from OOP03_family import Person, Family
>>> f = Family(Person('Mary'), Person('John'))
>>> id(f)
1785630884192
>>> f += Person('Eric')
>>> id(f)
1785630884192
>>> f.children
[Person('Eric')]
>>> f += Person('Michael')
>>> id(f)
1785630884192
>>> f.children
[Person('Eric'), Person('Michael')]
```

Chúng ta thấy rằng id của f không đổi.

Phần này tới đây là kết thúc, chúng ta tiếp tục với [phần 04](https://votatdat.github.io/Python/OOP04).
<br>[Phần 04](https://votatdat.github.io/Python/OOP04) và [phần 05](https://votatdat.github.io/Python/OOP05) vẫn tiếp tục đi vào các `magic method` nên mình tạm thời nêu lên, chưa có code ví dụ.
