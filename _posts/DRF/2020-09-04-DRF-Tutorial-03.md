---
layout: post
title: DRF Tutorial
subtitle: "Phần 03: tạo blog_project, Post model"
cover-img: /assets/img/planet.jpg
thumbnail-img: /assets/img/thum.jpg
share-img: /assets/img/planet.jpg
tags: [Python, Django, DRF]
---

* [List đầy đủ](https://votatdat.github.io/DRF) 
<br>
<br>

Để làm quen với REST Framework, các bạn có thể coi lại 2 phần trước: 
* [phần 01](https://votatdat.github.io/DRF/DRF01) 
* [phần 02](https://votatdat.github.io/DRF/DRF02) 

Từ phần này trở đi, chúng ta sẽ tạo một Blog API, có `user`, `permissions`, cho phép full `CRUD (Create-Read-Update-Delete)`.

## Cài đặt

Chúng ta sẽ tạo một `blog_project` và một app `posts`.
<br>Mở VS Code, mở folder, nhấn `Ctrl + ~` để mở Terminal và gõ:

{% highlight python %}
mkdir Blog_api && cd Blog_api

python -m venv env

env/Scripts/activate #Windows 
source env/bin/activate #Linux
source env/Scripts/activate #Bash trong Windows 

install django==2.2.6

pip freeze > requirements.txt

django-admin startproject blog_project .

python manage.py startapp posts
{% endhighlight %}

Đăng ký app mới tạo trong `settings.py`:

{% highlight python %}
# blog_project/settings.py
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	
	'posts.apps.PostsConfig', # Thêm mới ở đây
]
{% endhighlight %}

## Models
Chúng ta sẽ tạo một model `Post` với 5 field `author`, `title`, `body`, `created_at` và `pdated_at`:

{% highlight python %}
# posts/models.py
from django.db import models

from django.contrib.auth.models import User


class Post(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=50)
	body = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.title
{% endhighlight %}

Ở trên, chúng ta đã tạo một class Post, field `author` chúng ta sử dụng User có sẵn của Django, trong thực tế nên custom lại User, có thể xem [ở đây](https://votatdat.github.io/DRF/DRF_bonus01).
<br>`__str__` để hiện thị cho model ở Django Admin, khi vào trang administrator, các post sẽ hiện theo `title`.

Chúng ta đăng ký `Post` ở `admin.py`:

{% highlight python %}
# posts/admin.py
from django.contrib import admin

from .models import Post


admin.site.register(Post)
{% endhighlight %}

Chúng ta `migrate` để đồng bộ lên database:

{% highlight python %}
python manage.py makemigrations posts

python manage.py migrate
{% endhighlight %}

Tiếp theo, chúng ta tạo `superuser`, nhập username, email, password:

{% highlight python %}
python manage.py createsuperuser
{% endhighlight %}

Sau đó `runserver`: 

{% highlight python %}
python manage.py runserver
{% endhighlight %}

Chúng ta vào trang admin http://127.0.0.1:8000/admin/, login bằng username và password đăng ký ở trên, tạo một post đơn giản.

![](/Piks/DRF/DRF03_firstpost.PNG)

## Tests
Chúng ta sẽ tạo một file `tests.py` đơn giản để test `Post`, trong thực tế test rất quan trọng, ở đây chúng ta đi nhanh.

{% highlight python %}
touch posts/tests.py
{% endhighlight %}

{% highlight python %}
# posts/tests.py
from django.test import TestCase

from django.contrib.auth.models import User

from .models import Post


class BlogTests(TestCase):
	@classmethod
	def setUpTestData(cls):
		# Create a user
		testuser1 = User.objects.create_user(
		username='testuser1', password='abc123')
		testuser1.save()
		
		# Create a blog post
		test_post = Post.objects.create(
			author=testuser1, 
			title='Blog title', 
			body='Body content...'
		)
		test_post.save()
		
		
	def test_blog_content(self):
		post = Post.objects.get(id=1)
		author = f'{post.author}'
		title = f'{post.title}'
		body = f'{post.body}'
		self.assertEqual(author, 'testuser1')
		self.assertEqual(title, 'Blog title')
		self.assertEqual(body, 'Body content...')
{% endhighlight %}

Và sau đó, chúng ta vào terminal:

{% highlight python %}
python manage.py test
{% endhighlight %}

Kết quả sẽ giống giống như ở dưới:

Ran 1 test in 0.119s
<br>OK
<br>Destroying test database for alias 'default'...

Ở phần này, chúng ta đã tạo `Post` model, và test thử OK.
<br>[phần 04](https://votatdat.github.io/DRF/DRF04)  sẽ tạo API cho model này.


{% highlight python %}

{% endhighlight %}