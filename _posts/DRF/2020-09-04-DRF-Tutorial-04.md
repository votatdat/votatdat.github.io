---
layout: post
title: DRF Tutorial
subtitle: "Phần 04: tạo API cho Post database"
cover-img: /assets/img/planet.jpg
thumbnail-img: /assets/img/thumb.png
share-img: /assets/img/planet.jpg
tags: [Python, Django, DRF]
---

Nội dụng phần này:
- Tạo API cho Post model.

Danh sách đầy đủ bài học **[ở đây](https://votatdat.github.io/DRF)**.

## Cài đặt
Như ở [phần 02](https://votatdat.github.io/2020-09-04-DRF-Tutorial-02), chúng ta thấy để tạo một API thì qui trình gồm tạo 3 files:
* `serializers.py`: để chuyển database thành JSON.
* `views.py`: hơi giống với views.py của Django truyền thống.
* `urls.py`: để định hướng url.

Cài đặt package:

{% highlight python %}
pip install djangorestframework==3.10.3

pip freeze > requirements.txt
{% endhighlight %}

Cập nhật vào `settings.py`:

{% highlight python %}
# blog_project/settings.py
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',

	'rest_framework', # Thêm mới ở đây

	'posts.apps.PostsConfig',
]
# Thêm mới thêm đoạn này.
REST_FRAMEWORK = {
	'DEFAULT_PERMISSION_CLASSES': [
		'rest_framework.permissions.AllowAny',
	]
}
{% endhighlight %}

Ở đoạn trên, chúng ta setup `permissions` là **AllowAny**, nghĩa ta cho phép mọi người đều xem được API chúng ta xuất ra, chúng ta sẽ tìm hiểu thêm phần này sau.

## Serializers
Chúng ta tạo file `serializers.py` trong posts để chuyển database thành JSON:

{% highlight python %}
touch posts/serializers.py
{% endhighlight %}

{% highlight python %}
# posts/serializers.py
from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ('id', 'author', 'title', 'body', 'created_at',)
{% endhighlight %}

Ở trên, chúng ta đã bỏ `update_at` field.

## Views
Ở ví dụ [phần 02](https://votatdat.github.io/2020-09-04-DRF-Tutorial-02) chúng ta đã sử dụng `ListAPIView`, cái này chỉ tạo ra một read-only endpoint.
<br>Có View Class như sau:
* `CreateAPIView`: dùng để tạo (**create-only**), cung cấp `post` method.
* `ListAPIView`: dùng để liệt kê danh sách các mục (**read-only**), cung cấp `get` method.
* `RetrieveAPIView`: dùng để liệt kê một mục cụ thể trong danh sách (**read-only**), cung cấp `get` method.
* `DestroyAPIView`: dùng để xóa một mục cụ thể trong danh sách (**delete-only**), cung cấp `delete` method.
* `UpdateAPIView`: dùng để cập nhật một mục cụ thể trong danh sách (**update-only**), cung cấp `put` và `patch` method.

Các Class dưới là tổng hợp chức năng của 2 hay nhiều class ở trên:
* `ListCreateAPIView`
* `RetrieveUpdateAPIView`
* `RetrieveDestroyAPIView`
* `RetrieveUpdateDestroyAPIView`

Ở dưới, chúng ta sẽ sử dụng `ListCreateAPIView` để xuất danh sách các Post và `RetrieveUpdateDestroyAPIView` để xử lý một Post cụ thể.

{% highlight python %}
# posts/views.py
from rest_framework import generics

from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	
	
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
{% endhighlight %}

<br>
## URLs
Đầu tiên, chúng ta thêm vào `urls.py` ở project:

{% highlight python %}
# blog_project/urls.py
from django.contrib import admin

from django.urls import include, path # Thêm include


urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/v1/', include('posts.urls')), # Thêm dòng này
]
{% endhighlight %}

Có thể sau này chúng ta sẽ cập nhật api, nên trước mắt cứ để nó ở version 1.
<br>Tiếp theo, chúng ta thêm đường dẫn vào `urls.py` ở app:

{% highlight shell %}
touch posts/urls.py
{% endhighlight %}

{% highlight python %}
# posts/urls.py
from django.urls import path

from .views import PostList, PostDetail


urlpatterns = [
	path('', PostList.as_view()), # Xem toàn bộ các post
	path('<int:pk>/', PostDetail.as_view()), # Xem post cụ thể theo id
]
{% endhighlight %}

<br>
## Kết quả

Chúng ta runserver và vào đường link http://127.0.0.1:8000/api/v1/ để thấy kết quả.

{% highlight shell %}
python manage.py runserver
{% endhighlight %}

![](/assets/piks/DRF/DRF04_result1.PNG)

Đây là post mà chúng ta tạo ở trên, nếu các bạn làm từ đầu thì `"id": 1`, nhưng do mình làm vài cái trước rồi xóa nên nó id là 4.
<br>Các bạn chú ý rằng mỗi khi tạo một post thì id sẽ tự động tăng lên 1, dù xóa đi hết thì các post sau id vẫn tăng thêm chứ không reset.
<br>Ở class PostList chúng ta sử dụng `ListCreateAPIView` nên ở đây chúng ta sẽ coi được đầy đủ toàn bộ các post và có thể `post` thêm bài mới.
<br>Chúng ta xem `Allow` để biết chúng ta được làm gì, ở đây gồm `GET`, `POST`, `HEAD`, `OPTIONS`.
<br>Chúng ta vào thêm id vào đường link ở trên để xem cụ thể, chẳng hạn  http://127.0.0.1:8000/api/v1/4/

![](/assets/piks/DRF/DRF04_result2.PNG)

Ở đây, có thêm `PUT` và `PATCH` để edit post, có thêm `DELETE` để xóa bài viết, nhưng không có `POST`.

Phần này tới đây là kết thúc, chúng ta thấy rằng các API có thể được xem, cập nhật, xóa mà không cần login.
<br>Điều này là không thực tế, [phần 05](https://votatdat.github.io/2020-09-04-DRF-Tutorial-05) sẽ giới thiệu về `permissions`.

{% highlight python %}

{% endhighlight %}