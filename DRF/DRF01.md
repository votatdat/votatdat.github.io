---
layout: post
title: DRF
subtitle: Phần 01: tạo Book model
tags: [Python, Django, DRF]
comments: true
---

* [List đầy đủ](https://votatdat.github.io/DRF/DRF_list) 
<br>
<br>

Chú ý rằng Django dùng để tạo website có chứa nhiều webpage, còn Django REST Framework (DRF) tạo ra web API, là tập hợp các URL chứa các giao thức HTTP trả về JSON.
<br>Trong phần này, chúng ta sẽ tạo một `library` site, giới thiệu về cách hoạt động của DRF.

## Tạo môi trường ảo
Khi code, chúng ta nên tạo môi trường ảo, ở đây chúng ta sử dụng luôn tính năng này của Python, hình như tính năng này mới có từ version 3.7
<br>Còn có nhiều cách khác hay hơn, các bạn có thể Google thêm.
<br>Lưu ý là trên Windows, Linux hay Mac thì các lệnh ở dưới sẽ khác nhau một chút xíu.
<br>Mở terminal và gõ như ở dưới, ở VS Code thì phím tắt để mở terminal là `Ctrl + ~`

{% highlight python %}
# Tạo folder Library và chuyển vào thư mục đó
mkdir Library && cd Library 

# Dùng Python tạo virtual env
python -m venv env

# Activate 
env/Scripts/activate #Windows 

source env/bin/activate #Linux
{% endhighlight %}

Để deactivate môi trường ảo này thì chỉ đơn gõ `deactivate`.

Khi có môi trường ảo rồi thì chúng ta cài đặt Django. Ở đây chúng ta sử dụng bản 2.2.6 (bản mới nhất lúc viết file này là 3.1).

{% highlight python %}
pip install django==2.2.6
{% endhighlight %}

Mỗi khi cài đặt môi trường xong, chúng ta nên lưu lại lên file requirements.txt để khi share project hoặc share cho người khác thì chỉ cần gửi file này, người khác sẽ tự cài đặt môi trường giống hệt.

{% highlight python %}
#Để coi các package đã cài đặt
pip freeze

#Để lưu lại lên file text
pip freeze > requirements.txt
{% endhighlight %}

Tiếp theo chúng ta sẽ tạo project tên là `library_project`

{% highlight python %}
django-admin startproject library_project .
{% endhighlight %}

Lưu ý dấu `.` ở cuối câu lệnh:
* Có dấu `.` thì các file sẽ nằm ở foler Library/library_project
* Không có dấu `.` thì các file sẽ nằm ở foler Library/library_project/library_project

Các sắp xếp folder thì tùy mỗi người, nhưng cũng nên theo một chuẩn nào đó để mọi người tiện theo dõi.

Tiếp theo chúng ta `migrate` và `runserver`:

{% highlight python %}
python manage.py migrate
python manage.py runserver
{% endhighlight %}

Chúng ta mở trình duyệt, gõ http://127.0.0.1:8000/ để xem project đã ok hay chưa.

## Tạo app `books`
Tiếp theo chúng ta tạo một app có tên là `books`:

{% highlight python %}
python manage.py startapp books
{% endhighlight %}

Sau khi tạo app xong, chúng ta phải vào settings.py để add thêm app này.

{% highlight python %}
# library_project/settings.py
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	
	'books.apps.BooksConfig', # Thêm dòng này
]
{% endhighlight %}

hoặc đơn giản thêm `'books'` cũng được, nhớ có thêm dấu phẩy `,` ở cuối.

Chúng ta chạy lại `migrate` để đồng bộ với database.
{% highlight python %}
python manage.py migrate
{% endhighlight %}

## Tạo Models
Chúng ta tạo một model Book có 4 field `title`, `subtitle`, `author`, `isbn`:

{% highlight python %}
# books/models.py
from django.db import models

	class Book(models.Model):
		title = models.CharField(max_length=250)
		subtitle = models.CharField(max_length=250)
		author = models.CharField(max_length=100)
		isbn = models.CharField(max_length=13)
	
	def __str__(self):
		return self.title
{% endhighlight %}

Chúng ta chạy lại `migrate` để đồng bộ với database.

{% highlight python %}
python manage.py makemigrations books
python manage.py migrate
{% endhighlight %}

## Admin
Việc đầu tiên, chúng ta tạo `superuser`:

{% highlight python %}
python manage.py createsuperuser
{% endhighlight %}

Sau đó chúng ta gõ username, email, password để đăng ký admin, rồi register model này vào admin.py:

{% highlight python %}
# books/admin.py
from django.contrib import admin

from .models import Book


admin.site.register(Book)
{% endhighlight %}

Chúng ta mở trình duyệt, vào http://127.0.0.1:8000/admin và login với username và password đã đăng ký ở trên.

Chúng ta sẽ thấy:

![](./PIKs/DRF01_book.PNG)

Sau đó chúng ta sẽ thêm vào 1 hay vài cuốn sách, ví dụ như ở dưới:

![](./PIKs/DRF01_addbook.PNG)

![](./PIKs/DRF01_addbook2.PNG)

![](./PIKs/DRF01_addbook3.PNG)

## Views
`views.py` sẽ xử lý việc các model được hiển thị thế nào. Ở đây chúng ta sẽ sử dụng class-based `ListView` ở `generic`.

{% highlight python %}
# books/views.py
from django.views.generic import ListView

from .models import Book


class BookListView(ListView):
	model = Book
	template_name = 'book_list.html'
{% endhighlight %}

## URLs

Trước tiên, chúng ta thêm url ở project chính, ở folder `library_project`:

{% highlight python %}
# library_project/urls.py
from django.contrib import admin

from django.urls import path, include # Thêm include


urlpatterns = [
	path('admin/', admin.site.urls),
	path('', include('books.urls')), # Thêm dòng này
]
{% endhighlight %}

Dòng thêm vào có nghĩa là khi chúng ta mở trình duyệt và vào http://127.0.0.1:8000/ thì nó sẽ dẫn chúng ta tới setting của file `urls.py` ở folder `books`.

Do đó, tiếp theo, chúng ta tạo file `urls.py` mới ở folder books, lệnh dưới là ví dụ ở Linux:

{% highlight python %}
touch books/urls.py
{% endhighlight %}

Và chúng ta add thêm code cho nó:

{% highlight python %}
# books/urls.py
from django.urls import path

from .views import BookListView


urlpatterns = [
	path('', BookListView.as_view(), name='home'),
]
{% endhighlight %}

Tiếp theo, chúng ta tạo `template` và file html để hiện thị nội dung trên trang web.

{% highlight python %}
mkdir books/templates
mkdir books/templates/books
touch books/templates/books/book_list.html
{% endhighlight %}


{% highlight python %}
<!-- books/templates/books/book_list.html -->
<h1>All books</h1>

{ % for book in object_list % } 
  <ul>
    <li>Title: {{ book.title }}</li>
    <li>Subtitle: {{ book.subtitle }}</li>
    <li>Author: {{ book.author }}</li>
    <li>ISBN: {{ book.isbn }}</li>
  </ul>
{ % endfor % }
# Do vấn đề hiển thị nên nếu copy-paste đoạn code trên thì nhớ bỏ khoảng trắng giữa `{` và `%`
{% endhighlight %}

`object_list` là tên của object được tạo ra từ model ở `ListView`, chúng ta duyệt hết object_list và in ra kết quả ở file html.

{% highlight python %}
python manage.py runserver
{% endhighlight %}

Chúng ta mở trình duyệt và chạy  http://127.0.0.1:8000/. Kết quả:

![](./PIKs/DRF01_result.PNG)

Tới đây là kết thúc phần 01, ở trên là cách tạo và hiện thị database lên trình duyệt.
<br>[Phần 02](https://votatdat.github.io/DRF/DRF02) sẽ trình bày cách sự dụng DRF căn bản, hiện thị nội dung như trên ở dạng JSON.


{% highlight python %}

{% endhighlight %}