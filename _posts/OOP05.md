---
layout: page
title: Python OOP
subtitle: Phần 05: Giới thiệu về Polymorphism và special methods (phần 3).
comments: true
---

* [List đầy đủ](https://votatdat.github.io/Python/Python_list) 
<br>
<br>

## 06. Callable
Một object có thể được giả lập để có thể gọi được (callable) nhờ sử dụng `__call__`.
<br>Ví dụ:

```python
>>> class Person:
...     def __call__(self, name):
...             return f'Hello {name}'
...
>>> p = Person()
>>> p('Eric')
'Hello Eric'
```

Điều này có thể được sử dụng nhưng một `function-like object` (một object nhưng giống function) hoặc dùng để decorate class.

Ví dụ minh họa sẽ được thêm vào sau.


## 07. \_\_del\_\_ method
Giả sử bạn biết C++ thì hẳn bạn đã nghe tới khái niệm `garbage collector`, khi bạn tạo ra nhiều object mà không sử dụng nữa thì nó sẽ trở thành rác (garbage).
<br>Các ngôn ngữ lập trình khác nhau sẽ có kiểu dọn rác khác nhau. Ở Python, chúng ta cũng có `garbage collector` (GC) để huy các object mà không được tham chiếu ở bất cứ đâu.
<br>`__del__` sẽ được gọi ngay trước khi object bị hủy bởi GC, do đó GC sẽ quyết định khi nào method này được gọi.
<br> `__del__` được gọi là `finalizer`, đôi khi được gọi là `destructor` nhưng có vẻ tên gọi này không chính xác.

Về cơ bản, chúng ta không điều khiển được khi nào `__del__` được gọi, nó chỉ được gọi khi tất cả tham chiếu đến nó đều đã mất.

Nếu `__del__` chứa tham chiếu đến biến toàn cục, hoặc object khác thì những object này sẽ biến mất khi `__del__` được gọi.
<br>Nếu có ngoại lệ (exception) xảy ra khi `__del__` được gọi:
- exception sẽ không được raise, nó ở chế độ im lặng (silence)
- Mô tả về exception sẽ được gửi tới `stderr`
- Chương trình chính sẽ khoong cảnh báo bất cứ thứ gì sai trong quá trình kết thức.

Tốt hơn là dùng `context manager` để xóa tài nguyên.


Ví dụ minh họa sẽ được thêm vào sau.

## 08. \_\_format\_\_ method
Chúng ta dùng hàm `format()` để định dạng kiểu, 
(Sẽ viết và cập nhật tiếp)
