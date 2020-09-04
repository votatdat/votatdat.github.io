---
layout: post
title: DRF Tutorial
subtitle: "Phần 02: tạo API cho Book database"
cover-img: /assets/img/planet.jpg
thumbnail-img: /assets/img/thum.jpg
share-img: /assets/img/planet.jpg
tags: [Python, Django, DRF]
---

* [List đầy đủ](https://votatdat.github.io/DRF) 
<br>
<br>

Ở [phần 01](https://votatdat.github.io/DRF/DRF01) chúng ta đã xây dựng Book model, hiển thị database lên được template html.
<br>Nhưng khi hiển thị như vậy thì các front-end framework sẽ không xử lý thông tin được, do đó chúng ta cần API.
<br>Thêm nữa là xu thế mới, chúng ta phải chia front-end và back-end tách biệt, front-end không chỉ có web mà còn có app trên Android hay iOS.

## Cài đặt

{% highlight python %}
pip install djangorestframework==3.10.3
pip freeze > requirements.txt #Cập nhật file requirements.txt
{% endhighlight %}

Vì DRF được coi như là third-party app nên chúng ta cũng đối xử với nó như một app, chúng ta phải cập nhật nó vào trong `settings.py`.

{% highlight python %}

# library_project/settings.py
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	
	'rest_framework', # Thêm vào ở đây
	
	'books.apps.BooksConfig',
]
{% endhighlight %}

Để có thể xuất ra được JSON, chúng ra cần URL route, view và serializer mới.
<br>Có nhiều cách sắp xếp file khác nhau, nhưng ở đây chúng ta tạo một app mới gọi là `api` và cập nhật vào `settings.py`.

{% highlight python %}
python manage.py startapp api
{% endhighlight %}

{% highlight python %}
# library_project/settings.py
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	
	'rest_framework',
	
	'books.apps.BooksConfig',
	'api.apps.ApiConfig', # Thêm mới ở đây
]
{% endhighlight %}

## Serializers
`Serializer` sẽ chuyển đổi dữ liệu thành các dạng dễ sử dụng trên Internet, chẳng hạn như JSON.
<br>Và để làm việc đó, chúng ta cần một file `serializers.py` trong folder `api`.

{% highlight python %}
touch api/serializers.py
{% endhighlight %}

Và thêm code:

{% highlight python %}
# api/serializers.py
from rest_framework import serializers

from books.models import Book


class BookSerializer(serializers.ModelSerializer):
	class Meta:
		model = Book
		fields = ('title', 'subtitle', 'author', 'isbn')
{% endhighlight %}

Chúng ta tao class `BookSerializer` thừa kế `ModelSerializer` từ REST Framework, sử dụng model là model chúng ta xây dựng từ phần 01.
<br>Và chúng ta muốn hiển thị là: `title`, `subtitle`, `author`, `isbn`, đây là những field ở model mà chúng ta đã xây dựng.

## Views
`views.py` dựa vào built-in generic từ REST Framework, thoạt nhìn chúng ta thấy nó cũng giống như views.py của Django truyền thống, nhưng chúng không phải cùng một thứ.
<br>Một vài developer sợ nhầm lẫn nên đã đặt tên là `apiviews.py` hoặc `api.py`. Ở đây, chúng ta để nguyên `views.py`.

{% highlight python %}
# api/views.py
from rest_framework import generics

from books.models import Book

from .serializers import BookSerializer


class BookAPIView(generics.ListAPIView):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
{% endhighlight %}

Ở đây, chúng ta dùng `ListAPIView`, nó sẽ liệt kê toàn bộ danh sách Book mà chúng ta có thông qua `queryset`.
<br>Và `ListAPIView` chỉ tạo ra read-only endpoint mà thôi.

## URLs
Cuối cùng, chúng ta cần một API endpoint được xác lập ở URLs.
<br>Đầu tiên, chúng ta đăng kí URL cho API trong file `urls.py` ở project chính.

{% highlight python %}
# library_project/urls.py
from django.contrib import admin

from django.urls import path, include


urlpatterns = [
	path('admin/', admin.site.urls),
	path('', include('books.urls')),
	path('api/', include('api.urls')), # Thêm mới ở đây
]
{% endhighlight %}

Sau đó, chúng ta tạo file `urls.py` ở api:

{% highlight python %}
touch api/urls.py
{% endhighlight %}

{% highlight python %}
# api/urls.py
from django.urls import path

from .views import BookAPIView


urlpatterns = [
	path('', BookAPIView.as_view()),
]
{% endhighlight %}

## Kết quả
Các bước chuẩn bị ở trên đã xong, chúng ta chạy thử.

{% highlight python %}
python manage.py runserver
{% endhighlight %}

Chúng ta dùng lệnh `curl` để xem kết quả:

{% highlight python %}
curl http://127.0.0.1:8000/api/
{% endhighlight %}

Kết quả:

{% highlight python %}
[{"title":"Django","subtitle":"API","author":"Tom Christie","isbn":"123-456789012"},
{"title":"Python","subtitle":"Programming Language","author":"Guido van Rossum","isbn":"012-345678901"}]
{% endhighlight %}

Hoặc mở trình duyệt, gõ  http://127.0.0.1:8000/api/, kết quả: 

![](/Piks/DRF/DRF02_APIresult.PNG)


Như vậy, chúng ta đã tạo được một API đơn giản, sử dụng REST Framework.
<br>[Phần 01](https://votatdat.github.io/DRF/DRF01) và [phần 02](https://votatdat.github.io/DRF/DRF02) là một ví dụ cơ bản về API của REST Framework.
<br>[Phần 03](https://votatdat.github.io/DRF/DRF03) trở đi là một ví dụ phức tạp hơn.

{% highlight python %}

{% endhighlight %}