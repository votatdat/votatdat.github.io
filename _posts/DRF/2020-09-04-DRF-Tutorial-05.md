---
layout: post
title: DRF Tutorial
subtitle: "Phần 05: giới thiệu về permissions/authorization"
cover-img: /assets/img/planet.jpg
thumbnail-img: /assets/img/thum.jpg
share-img: /assets/img/planet.jpg
tags: [Python, Django, DRF]
---

* [List đầy đủ](https://votatdat.github.io/DRF) 
<br>
<br>

Ở phần trước, chúng ta đã tạo một API cho Post model, nhưng khi có được đường link thì bất kỳ ai cũng có thể xem bài, post bài, edit hay xóa bài.
<br>Trong thực tế, anonymous chỉ có thể xem bài, hoặc có khi phải login mới được xem bài.
<br>Và user nào thì chỉ được xem bài của user khác, chỉ được sửa lại bài hoặc xóa bài của chính mình.

## Tạo user mới
Chúng ta runserver, vào trang admin http://127.0.0.1:8000/admin/, tạo vài user mới, chẳng hạn như ở dưới:

![](./PIKs/DRF05_adduser1.PNG)

Chúng ta tạo luôn vài user để test thử các chức năng:

![](./PIKs/DRF05_adduser2.PNG)

## Thêm chức năng login vào trình duyệt
Cho tới nay chúng ta đã có vài user, khi muốn thay đổi user thì phải nhảy vào trang admin logout ra rồi login lại, rồi vào lại trang API rất phiền hà.
<br>Nên chúng ta tạo luôn một API để login, logout ngay trên trang API chúng ta đang xem.
<br>Để làm điều này, chúng ta chỉ cần chỉnh sửa tí xíu file `urls.py` trong project chính.

{% highlight python %}
# blog_project/urls.py
from django.contrib import admin

from django.urls import include, path


urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/v1/', include('posts.urls')),
	path('api-auth/', include('rest_framework.urls')), # Thêm dòng này
]
{% endhighlight %}

 Bây giờ khi vào lại trang http://127.0.0.1:8000/api/v1/ sẽ có username và mũi tên hướng xuống ở góc phải phía trên, có thể login logout tiện hơn.
 
![](./PIKs/DRF05_inout.PNG)

## Project-level Permissions
Ở [phần 04](https://votatdat.github.io/DRF/DRF04), trong file `settings.py`, chúng ta đã thêm đoạn code dưới:

{% highlight python %}
# blog_project/settings.py
REST_FRAMEWORK = {
	'DEFAULT_PERMISSION_CLASSES': [
		'rest_framework.permissions.AllowAny',
	]
}
{% endhighlight %}

Có 4 mức permission cho `DEFAULT_PERMISSION_CLASSES`:
* `AllowAny` - bất cứ ai cũng có toàn quyền truy cập.
* `IsAuthenticated` - chỉ những user đã đăng ký sẽ có quyền truy cập.
* `IsAdminUser` - chỉ có các admin/superuser mới có quyền truy cập.
* `IsAuthenticatedOrReadOnly` - chỉ những user đã đăng ký sẽ có quyền truy cập, nếu anonymous thì sẽ được xem nội dung.

Chúng ta thử sửa một chút setting chỗ này, chẳng hạn:

{% highlight python %}
# blog_project/settings.py
REST_FRAMEWORK = {
	'DEFAULT_PERMISSION_CLASSES': [
		'rest_framework.permissions.IsAuthenticated', # Sửa xíu chỗ này
	]
}
{% endhighlight %}
 
Các bạn runserver lại, vô lại trang http://127.0.0.1:8000/api/v1/ và thử nhé, chỉ login với danh sách user ở trên kia mới có quyền truy cập.
<br>Các bạn thử luôn cả 4 mức permission nhé.
<br>Đây gọi là project-level Permission, khi bạn sửa file `settings.py` thì nó tác động lên toàn project.

## View-level Permissions
Giả sử rằng chúng ta có nhiều API, mà không phải API nào cũng có permission giống API nào, một cách khác là điều chỉnh permission theo view.
<br>Đầu tiên, chúng ta sửa lại file `settings.py` trả về như cũ, cho phép AllowAny:

{% highlight python %}
# blog_project/settings.py
REST_FRAMEWORK = {
	'DEFAULT_PERMISSION_CLASSES': [
		'rest_framework.permissions.AllowAny', # Trả chỗ này về như trước, cho phép toàn bộ
	]
}
{% endhighlight %}

`rest_framework` có một chức năng `permissions` dựng sẵn, cho phép thêm vào `permission_classes` để tạo permission riêng biệt cho từng class trong view.
<br>Chúng ta thay đổi `views.py` như ở dưới: 

{% highlight python %}
# posts/views.py
from rest_framework import generics, permissions # thêm permissions

from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
	permission_classes = (permissions.IsAuthenticated,) # thêm permissions là IsAuthenticated
	queryset = Post.objects.all()
	serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (permissions.IsAuthenticated,) # thêm permissions là IsAuthenticated
	queryset = Post.objects.all()
	serializer_class = PostSerializer
{% endhighlight %}

Các bạn vô lại trang http://127.0.0.1:8000/api/v1/ và thử nhé.

## Custom Permissions
Permission ở project-level có 4 mức, view-level hình như cũng có 4 mức tương tự như vậy.
<br>Giả sử rằng bạn muốn user nào đó được chỉnh sửa, xóa bài viết của chính mình và user khác chỉ được xem, thì 4 mức permission ở trên không giải quyết được.
<br>Do đó chúng ta phải custom permission.

Đầu tiên, chúng ta tạo file `permissions.py` trong app posts:

{% highlight shell %}
touch posts/permissions.py
{% endhighlight %}

Tiếp theo, chúng ta sẽ tạo một class mới, dựa trên `BasePermission` được dựng sẵn:

{% highlight python %}
# posts/permissions.py
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		# Kiểm tra permissions cho các yêu cầu mà read-only
		# SAFE_METHODS gồm có GET, HEAD và OPTIONS
		if request.method in permissions.SAFE_METHODS:
			return True
			
		# Kiểm tra permission cho các yêu cầu write
		return obj.author == request.user
{% endhighlight %}

Bước đầu, chúng ta kiểm tra xem các method từ request có phải là các request read-only hay không, ở đây là `SAFE_METHODS`, nếu đúng sẽ trả lại true.
<br>Nếu là các method khác, chẳng hạn như `PUT`, `PATCH`, `DELETE` thì kiểm tra xem user đang request có phải là author của obj không.

Chúng ta sửa lại chút xíu ở `views.py`:

{% highlight python %}
# posts/views.py
from rest_framework import generics

from .models import Post
from .permissions import IsAuthorOrReadOnly # Thêm cái này
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
	# Chuyển permissions.IsAuthenticated dựng sẵn thành IsAuthorOrReadOnly tự viết
	permission_classes = (IsAuthorOrReadOnly,) # sửa dòng này
	queryset = Post.objects.all()
	serializer_class = PostSerializer
{% endhighlight %}

Các bạn có thể đọc thêm về permission trên trang chủ [ở đây](https://www.django-rest-framework.org/api-guide/permissions/).

Các bạn runserver, vô lại trang http://127.0.0.1:8000/api/v1/ và thử nhé.
<br>
<br>
<br>Phần này tới đây là hết, [phần 06](https://votatdat.github.io/DRF/DRF06) chúng ta sẽ tìm hiểu về `User Authentication`.

{% highlight python %}

{% endhighlight %}