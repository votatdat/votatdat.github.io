---
layout: post
title: DRF Tutorial
subtitle: "Phần 09: giới thiệu về Schemas và Documentation"
cover-img: /assets/img/planet.jpg
thumbnail-img: /assets/img/thumb.png
share-img: /assets/img/planet.jpg
tags: [Python, Django, DRF]
---

Nội dụng phần này:
- Giới thiệu về Schemas và Documentation để làm tài liệu cho API.

Danh sách đầy đủ bài học **[ở đây](https://votatdat.github.io/DRF)**.

Cho tới nay, chúng ta cũng đã xây dựng kha khá API endpoint:

![](/assets/piks/DRF/DRF09_endpoints.PNG)

`Schema` là dạng tài liệu cho máy tính đọc, liệt kê ra toàn bộ API endpoint, URLs và HTTP Verb (GET, POST, PUT, DELETE v.v...)
<br>`Documentation` là tài liệu được thêm vào schema để dễ hơn cho người đọc và sử dụng.

## Schemas
Từ [version 3.9](https://www.django-rest-framework.org/community/3.9-announcement/), DRF đã giới thiệu [OpenAPI schema](https://www.openapis.org/) (tên cũ là `Swagger`) để thay thế [Core API](http://www.coreapi.org/) để tạo Schema.
<br>Ở đây, chúng ta sử dụng Core API để tạo schema. Chúng ta cũng cần thêm [pyyaml](https://pyyaml.org/) để render schema của chúng ta thành YAML-based format.

Chúng ta ấn Ctrl + C để stopserver và cài đặt:

{% highlight python %}
pip install coreapi==2.3.3 pyyaml==5.1.2

pip freeze > requirements.txt
{% endhighlight %}

Vì DRF có hỗ trợ cho Core API nên chúng ta không cần làm gì nhiều, chỉ thêm đường dẫn ở `urls.py`.

{% highlight python %}
# blog_project/urls.py
from django.contrib import admin
from django.urls import include, path

from rest_framework.schemas import get_schema_view # Thêm mới ở đây


schema_view = get_schema_view(title='Blog API') # Thêm mới ở đây

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/v1/', include('posts.urls')),
	path('api-auth/', include('rest_framework.urls')),
	path('api/v1/rest-auth/', include('rest_auth.urls')),
	path('api/v1/rest-auth/registration/',
	include('rest_auth.registration.urls')),
	path('schema/', schema_view), # Thêm mới ở đây
]
{% endhighlight %}

Chúng ta runserver, vào đường dẫn http://127.0.0.1:8000/schema/ để xem kết quả:
<br>Kết quả cho máy tính đọc, giống giống như ở dưới:

![](/assets/piks/DRF/DRF09_schema.PNG)

## Documentation
Schema ở trên chỉ dành cho máy tính đọc, còn để người đọc chúng ta cần một giao diện thân thiện hơn.
<br> ta thêm đường dẫn ở URLs, và khai báo ở `settings.py`, nếu không khai báo sẽ bị lỗi **Exception Value:	'AutoSchema' object has no attribute 'get_link'**.

{% highlight python %}
# blog_project/urls.py
from django.contrib import admin
from django.urls import include, path

from rest_framework.documentation import include_docs_urls # Thêm mới ở đây
from rest_framework.schemas import get_schema_view


schema_view = get_schema_view(title='Blog API')

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/v1/', include('posts.urls')),
	path('api-auth/', include('rest_framework.urls')),
	path('api/v1/rest-auth/', include('rest_auth.urls')),
	path('api/v1/rest-auth/registration/',
	include('rest_auth.registration.urls')),
	path('docs/', include_docs_urls(title='Blog API')), # Thêm mới ở đây
	path('schema/', schema_view),
]
{% endhighlight %}

{% highlight python %}
blog_project/settings.py

...
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}
{% endhighlight %}

Chúng ta runserver, vào đường dẫn http://127.0.0.1:8000/docs/ để xem kết quả:

![](/assets/piks/DRF/DRF09_doc1.PNG)

Chúng ta có thể sửa thêm một chút:

{% highlight python %}
# blog_project/urls.py
from django.contrib import admin
from django.urls import include, path

from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view


API_TITLE = 'Blog API' # Thêm mới ở đây
API_DESCRIPTION = 'A Web API for creating and editing blog posts.' # Thêm mới ở đây
schema_view = get_schema_view(title=API_TITLE) # Thêm mới ở đây

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/v1/', include('posts.urls')),
	path('api-auth/', include('rest_framework.urls')),
	path('api/v1/rest-auth/', include('rest_auth.urls')),
	path('api/v1/rest-auth/registration/',
	include('rest_auth.registration.urls')),
	path('docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION)), # Thêm mới ở đây
	path('schema/', schema_view),
]
{% endhighlight %}

Giao diện đẹp hơn một chút, các bạn ấn thử vào `Interact` rồi `SEND REQUEST` để thử, các bạn hãy vọc thử với Documentation mới này:

![](/assets/piks/DRF/DRF09_doc2.PNG)

## Django REST Swagger
Documentation ở trên đã khá tốt, tuy nhiên chúng ta vẫn có thể thử [Swagger](https://swagger.io/) của thư viện [Django REST Swagger](https://marcgibbons.com/django-rest-swagger/) để thấy nó còn tốt hơn, và hiện giờ đây được xem là cách tốt nhất để tạo Documentation cho API.

Chúng ta ấn Ctrl + C để dừng và cài thêm thư viện:

{% highlight python %}
pip install django-rest-swagger==2.2.0

pip freeze > requirements.txt
{% endhighlight %}

Chúng ta khai báo trong setting:

{% highlight python %}
# blog_project/settings.py
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.sites',
	
	'rest_framework',
	'rest_framework.authtoken',
	
	'rest_framework_swagger', # Thêm ở đây
	
	'allauth',
	'allauth.account',
	'allauth.socialaccount',
	
	'rest_auth',
	'rest_auth.registration',
	
	'posts.apps.PostsConfig',
]
{% endhighlight %}

Chúng ta sẽ thay thế schema mặc định:

{% highlight python %}
# blog_project/urls.py
from django.contrib import admin
from django.urls import include, path

from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

from rest_framework_swagger.views import get_swagger_view # Thêm mới ở đây


API_TITLE = 'Blog API'
API_DESCRIPTION = 'A Web API for creating and editing blog posts.'
schema_view = get_swagger_view(title=API_TITLE) # Thêm mới ở đây

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/v1/', include('posts.urls')),
	path('api-auth/', include('rest_framework.urls')),
	path('docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION)),
	# path('schema/', schema_view), # Bỏ schema cũ
	path('swagger-docs/', schema_view), # Thêm schema mới
]
{% endhighlight %}

Chúng ra runserver, vào đường dẫn http://127.0.0.1:8000/swagger-docs xem thử: 

![](/assets/piks/DRF/DRF09_doc3.PNG)

## Swagger Log In and Log Out
Có nhiều cách để customize Swagger trên [Official Documentation](https://django-rest-swagger.readthedocs.io/en/latest/settings/).
<br>Ở góc phải phía trên, chúng ta không thể login hoặc logout. Cách dễ nhất là thêm Swagger vào `setting.py`, sau đó chúng ta refresh lại trình duyệt, và mọi thứ sẽ như cũ:

{% highlight python %}
# blog_project/settings.py
SWAGGER_SETTINGS = {
	'LOGIN_URL': 'rest_framework:login',
	'LOGOUT_URL': 'rest_framework:logout',
}
{% endhighlight %}

Tutorial tới đây là hết, mình hi vọng nó sẽ giúp ích được cho các bạn mới làm quen với Django REST Framework.
<br>Cảm ơn các bạn dã ghé ngang và đọc hết tutorial này.