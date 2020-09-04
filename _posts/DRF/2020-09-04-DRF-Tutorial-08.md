---
layout: post
title: DRF Tutorial
subtitle: "Phần 08: giới thiệu về Viewsets và Routers"
cover-img: /assets/img/planet.jpg
thumbnail-img: /assets/img/thumb.png
share-img: /assets/img/planet.jpg
tags: [Python, Django, DRF]
---

Nội dụng phần này:
- Giới thiệu về ViewSet và Router để tiết kiệm code.

Danh sách đầy đủ bài học **[ở đây](https://votatdat.github.io/DRF)**.

[Viewsets](https://www.django-rest-framework.org/api-guide/viewsets/) và [routers](https://www.django-rest-framework.org/api-guide/routers/) là những tool mà có thể giúp chúng ta viết API nhanh hơn, do một viewset có thể thay thế cho nhiều view và router có thể tự tạo URLs.

## User Endpoints
Chúng ta đã có những endpoint sau:

![](/assets/piks/DRF/DRF08_endpoints.PNG)

Chúng ta chỉ tạo có 2 endpoint đầu tiên, `django-rest-auth` cung cấp 5 cái còn lại.
<br>Bây giờ chúng ta sẽ thêm 2 endpoint để liệt kê danh sách toàn bộ user, và từng user.

Để tạo API bất kỳ, chúng ta đều phải làm 3 bước:
- Tạo serilizers để chuyển database thàng JSON
- Tạo views cho endpoints
- Thêm URLs route

Đầu tiên, chúng ta tạo `UserSerializer` class:

{% highlight python %}
# posts/serializers.py
from django.contrib.auth import get_user_model # Thêm mới chỗ này

from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ('id', 'author', 'title', 'body', 'created_at',)


class UserSerializer(serializers.ModelSerializer): # Thêm mới class này
	class Meta:
		model = get_user_model()
		fields = ('id', 'username',)
{% endhighlight %}

Có [3 cách](https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#referencing-the-user-model) để reference User model ở Django, ở trên chúng ta dùng `get_user_model`.

Tiếp theo, chúng ta thêm View:

{% highlight python %}
# posts/views.py
from django.contrib.auth import get_user_model # Thêm mới chỗ này

from rest_framework import generics

from .models import Post
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer, UserSerializer # Thêm mới chỗ này


class PostList(generics.ListCreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (IsAuthorOrReadOnly,)
	queryset = Post.objects.all()
	serializer_class = PostSerializer


class UserList(generics.ListCreateAPIView): # Thêm mới class này
	queryset = get_user_model().objects.all()
	serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView): # Thêm mới class này
	queryset = get_user_model().objects.all()
	serializer_class = UserSerializer
{% endhighlight %}

Chúng ta nhận thấy rằng, code khá là lặp lại: `Post` view và `User` view khá là giống nhau.

Cuối cùng, chúng ta thêm URLs:

{% highlight python %}
# posts/urls.py
from django.urls import path

from .views import UserList, UserDetail, PostList, PostDetail # Thêm mới chỗ này


urlpatterns = [
	path('', PostList.as_view()),
	path('<int:pk>/', PostDetail.as_view()),
	path('users/', UserList.as_view()), # Thêm mới chỗ này
	path('users/<int:pk>/', UserDetail.as_view()), # Thêm mới chỗ này
]
{% endhighlight %}

Vậy là xong, chúng ta runserver vào http://127.0.0.1:8000/api/v1/users/, kết quả đại khái như ở dưới:

![](/assets/piks/DRF/DRF08_users.PNG)

Chúng ta xem các id, chọn một id nào nào đó rồi xem chi tiết, chẳng hạn chọn user có id=2, http://127.0.0.1:8000/api/v1/users/2/

![](/assets/piks/DRF/DRF08_userdetail.PNG)


## Viewsets
Ở trên, trong `views.py` chúng ta thấy code khá là lặp lại ở các serializer class.
<br>`Viewsets` là một cách để kết hợp nhiều view liên quan với nhau chỉ ở trong 1 class.
<br>Hiện giờ, chúng ta có 4 view: 2 cho Post và 2 cho user. Chúng ta có thể kết hợp lại thành 2 view: 1 cho Post và 1 cho user.

Chúng ta xóa đi 4 view cũ, và thêm 2 view mới như ở dưới:

{% highlight python %}
# posts/views.py
from django.contrib.auth import get_user_model

from rest_framework import viewsets # Thêm mới chỗ này

from .models import Post
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer, UserSerializer


class PostViewSet(viewsets.ModelViewSet): # Thêm mới class này
	permission_classes = (IsAuthorOrReadOnly,)
	queryset = Post.objects.all()
	serializer_class = PostSerializer


class UserViewSet(viewsets.ModelViewSet): # Thêm mới class này
	queryset = get_user_model().objects.all()
	serializer_class = UserSerializer
{% endhighlight %}

## Routers
Sau khi tạo view xong, thì bước tiếp theo cũng là thêm vào URLs, ở trên chúng ta phải thêm 2 URLs: 1 cho danh sách user và 1 cho user chi tiết với `pk`.
<br>Tuy nhiên `Router` sẽ tạo URL pattern cho chúng ta.
<br>DRF có 2 default router:  [SimpleRouter](https://www.django-rest-framework.org/api-guide/routers/#simplerouter) và [DefaultRouter](https://www.django-rest-framework.org/api-guide/routers/#defaultrouter), chúng ta cũng có thể [customize lại router](https://www.django-rest-framework.org/api-guide/routers/#custom-routers). Dưới đây, chúng ta sử dụng `defaultrouter`.

Chúng ta xóa hết các path trong file `posts/urls.py`, thêm vào router như ở dưới:

{% highlight python %}
# posts/urls.py
from rest_framework.routers import SimpleRouter

from .views import UserViewSet, PostViewSet


router = SimpleRouter()
router.register('users', UserViewSet, base_name='users')
router.register('', PostViewSet, base_name='posts')


urlpatterns = router.urls
{% endhighlight %}

Các bạn hãy vào các link sau check lại:
<br>http://127.0.0.1:8000/api/v1/users/ : danh sách các user đã tạo
<br>http://127.0.0.1:8000/api/v1/users/2 : user có id=2, các bạn xem danh sách coi có id nào thì xem thử vài id.
<br>http://127.0.0.1:8000/api/v1/ : danh sách các Post
<br>http://127.0.0.1:8000/api/v1/4/ : post có id=4, các bạn xem danh sách coi có id nào thì xem thử vài id.

Lưu ý , chúng ta xem http://127.0.0.1:8000/api/v1/users/2

![](/assets/piks/DRF/DRF08_user2.PNG)

1. Ở view cũ nó là **User Detail**, giờ chuyển thành **User Instance**
2. User đang login là test nhưng có quyền delete user khác, đây là option mặc định của `ModelViewSet` gồm:  .list(), .retrieve(), .create(), .update(), .partial_update(), và .destroy().

Chúng ta có thể customize lại viewset nhưng chúng ta thấy được sự đánh đổi của Viewset ở đây, viết ít code hơn, nhưng phải viết nhiều cái khác để config theo ý mình.
<br>Bạn đầu chúng ta nên viết như bình thường, khi nào thấy API nhiều lên, có sự lặp lại nhiều thì hãy sử dụng ViewSet.

Phần này tới đây là hết, [phần 09](https://votatdat.github.io/2020-09-04-DRF-Tutorial-08) sẽ giới thiệu về việc làm tài liệu cho API dùng `Schemas` và `Documentation`.