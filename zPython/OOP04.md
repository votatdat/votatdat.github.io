---
layout: page
title: Python OOP
subtitle: Phần 04: Giới thiệu về Polymorphism và special methods (phần 2).
comments: true
---

* [List đầy đủ](https://votatdat.github.io/Python/Python_list) 
<br>
<br>

## 03. So sánh (comparision)
Chúng ta có các toán tử ở dưới:

```python
__lt__: less than <
__le__: less or equal <=
__eq__: equal ==
__ne__: not equal !=
__gt__: greater than >
__ge__: greater than or equal >=
```

Ví dụ minh họa sẽ được thêm vào sau.


## 04.  Hashing and Equality
Một object được gọi là `hashable` nếu nó có một giá trị `hash` hoàn toàn không thay đổi trong thời gian tồn tại của nó.
<br>Nếu `__eq__` được thêm vào class thì `__hash__` sẽ ngầm được set về None nếu `__hash__` không có trong class.
<br>Về mặc định, nếu không có ghi đè:
- `__hash__` sử dụng id của object.
- `__eq__` sử dụng `identity comparision` (đó là `is`)

Ví dụ minh họa sẽ được thêm vào sau.


## 05. Boolean
Chúng ta nhận thấy rằng:
- Bất cứ số nào không phải là 0 thì sẽ trả về True, còn 0 thì trả về False.
- Một collection rỗng (list, tuple, dictionary...) sẽ trả vè False, còn lại là True.

Thực sự thì một object mặc định sẽ có giá trị True, chúng ta có thể ghi đè điều này sử dụng `__bool__`.
<br>Nếu `__bool__` không tồn tại, Python sẽ dùng `__len__`, nếu trả về 0 thì là False, còn lại là True.

Ví dụ minh họa sẽ được thêm vào sau.




<br>
<br>
<br>
<br>
(Sẽ viết và cập nhật tiếp)
