---
layout: post
title: DRF Tutorial
subtitle: "Phần 07: giới thiệu về User Authentication (tiếp theo)"
cover-img: /assets/img/planet.jpg
thumbnail-img: /assets/img/thumb.png
share-img: /assets/img/planet.jpg
tags: [Python, Django, DRF]
---

Nội dụng phần này:
- Giới thiệu user API.
- Giới thiệu `django-rest-auth`: login, logout, reset password API.
- Giới thiệu `django-allauth`: user registration API.

Danh sách đầy đủ bài học **[ở đây](https://votatdat.github.io/DRF)**.

## User API
Ở phần trước, chúng ta đã thêm một url ở file blog_project/urls.py để có thể login, logout ngày ở http://127.0.0.1:8000/api/v1/ mà không cần vào lại trang admin.

{% highlight python %}
# blog_project/urls.py
path('api-auth/', include('rest_framework.urls')),
{% endhighlight %}

Chúng ta có thể tạo một `users` app rồi thêm serializers, views, urls để làm việc này.
<br>Ở đây, để cho đơn giản, chúng ta sẽ sử dụng `django-rest-auth` và `django-allauth`.

## Django-Rest-Auth
Cài đặt:

{% highlight python %}
pip install django-rest-auth==0.9.5

pip freeze > requirements.txt
{% endhighlight %}

Chúng ta đăng ký app mới vào `settings.py`.

{% highlight python %}
# blog_project/settings.py
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	
	'rest_framework',
	'rest_framework.authtoken',
	
	'rest_auth', # Thêm mới cái này
	
	'posts.apps.PostsConfig',
]
{% endhighlight %}

Chúng ta cập nhật thêm vào url:

{% highlight python %}
# blog_project/urls.py
from django.contrib import admin

from django.urls import include, path


urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/v1/', include('posts.urls')),
	path('api-auth/', include('rest_framework.urls')),
	path('api/v1/rest-auth/', include('rest_auth.urls')), # Thêm mới cái này
]
{% endhighlight %}

Run server, và vào các đường dẫn phía dưới, sẽ thấy `django-rest-auth` đã tạo ra API để login, logout, reset password, confirm reset password.
<br>Lưu ý là không có resgistration, chúng ta sẽ thêm vào sau ở phần dưới khi thêm `django-allauth` để tạo token cho user.
<br>
<br>http://127.0.0.1:8000/api/v1/rest-auth/login/
<br>http://127.0.0.1:8000/api/v1/rest-auth/logout/
<br>http://127.0.0.1:8000/api/v1/rest-auth/password/reset
<br>http://127.0.0.1:8000/api/v1/rest-auth/password/reset/confirm

Các bạn thử vào vọc xem sao nhé.

## User Registration
Để tạo một API để đăng ký user, thì Django lẫn DRF đều không có views tạo sẵn nào để làm việc này, chúng ta sử dụng `django-allauth`.

Cài đặt: 

{% highlight python %}
pip install django-allauth==0.40.0

pip freeze > requirements.txt
{% endhighlight %}

Thêm setting cho phần này khá là nhiều: 
- django.contrib.sites
- allauth
- allauth.account
- allauth.socialaccount
- rest_auth.registration

{% highlight python %}
# blog_project/settings.py
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.sites', # Thêm mới ở đây
	
	'rest_framework',
	'rest_framework.authtoken',
	
	'allauth', # Thêm mới ở đây
	'allauth.account', # Thêm mới ở đây
	'allauth.socialaccount', # Thêm mới ở đây
	
	'rest_auth',
	'rest_auth.registration', # Thêm mới ở đây
	
	'posts.apps.PostsConfig',
] 

...

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # Thêm mới ở đây
SITE_ID = 1 # Thêm mới ở đây
{% endhighlight %}

`EMAIL_BACKEND` là tạo một backend email giả lập, gửi email xác nhận cho user khi có một user mới nào đó đăng ký.
<br>`SITE_ID` là một phần của Django "sites" framework (đó là lí do ở trên chúng ta thêm `django.contrib.sites`), dùng để host nhiều website trên cùng 1 project.
<br>Ở project chúng ta đang làm chỉ có 1 site, nhưng `django-allauth` sử dụng sites framework nên chúng ta bắt buộc phải thêm vào.

Vì chúng ta thêm app mới, chúng ta phải migrate lại:

{% highlight python %}
python manage.py migrate
{% endhighlight %}

Sau đó chúng ta thêm đường dẫn vào url chính của project:

{% highlight python %}
# blog_project/urls.py
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/v1/', include('posts.urls')),
	path('api-auth/', include('rest_framework.urls')),
	path('api/v1/rest-auth/', include('rest_auth.urls')),
	path('api/v1/rest-auth/registration/', include('rest_auth.registration.urls')), # Thêm mới ở đây
]
{% endhighlight %}

Vậy là xong, chúng ra runserver và vào đường link http://127.0.0.1:8000/api/v1/rest-auth/registration/

![](/assets/piks/DRF/DRF07_register.PNG)

## Token
Chúng ta tạo thử 1 user mới:

![](/assets/piks/DRF/DRF07_register2.PNG)

Ấn POST và kết quả: 

![](/assets/piks/DRF/DRF07_register3.PNG)

Vậy là ngon lành cành đào, Server đã trả về `HTTP 201 Created`1 và tạo ra `key` (token), dùng 3rd party package đỡ mệt hẳn.
<br>Chúng ta xem terminal, chúng ta sẽ thấy có 1 email gửi cho user để xác nhận tài khoản (đây là do `EMAIL_BACKEND` mà chúng ta set ở trên)

![](/assets/piks/DRF/DRF07_register4.PNG)

Các bạn hãy vào trang admin, dùng superuser account và vô mục TOKENS để xem, sẽ thấy trong đó cũng có một token y hệt như token được tạo ở registration API.
<br>Lưu ý rằng chúng ta chỉ thấy token cho user test chúng ta mới tạo, không thấy token bất kỳ user nào khác vì lúc tạo các user khác, `django-allauth` chưa được thêm vào.
<br>Bây giờ chúng ta vào url này để login http://127.0.0.1:8000/api/v1/rest-auth/login/, lúc này login API sẽ xuất hiện token bên trên. 
<br>Ở phía front-end, chúng ta phải lưu token này ở [localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage) hoặc `cookie` để sau này phía Server có thể xác thực user.
<br>
<br>
<br>Phần này tới đây là hết, chúng ta sẽ tìm hiểu về `Viewsets` và `Routers` ở [phần 08](https://votatdat.github.io/2020-09-04-DRF-Tutorial-08).