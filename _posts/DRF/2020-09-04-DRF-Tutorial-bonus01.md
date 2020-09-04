---
layout: post
title: DRF Tutorial
subtitle: Customize User
cover-img: /assets/img/planet.jpg
thumbnail-img: /assets/img/thum.jpg
share-img: /assets/img/planet.jpg
tags: [Python, Django, DRF]
---

* [List đầy đủ](https://votatdat.github.io/DRF) 
<br>
<br>

Ở phần [phần 03](https://votatdat.github.io/DRF/DRF03) chúng ta đã tạo một model Post như ở dưới:

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

Ở đây, chúng ta dùng ForeignKey để tạo author dựa trên class User có sẵn.
<br>Đây là mối quan hệ many-to-one, nghĩa là một User có thể là author của nhiều post, nhưng một author thì có một User thôi.
<br>`on_delete=models.CASCADE` nghĩa là khi User bị xóa, sẽ xóa toàn bộ author kết nối với User đó.
<br>Chúng ta sẽ thắc mắc class User dựng sẵn có gì? Chúng ta có thể đọc Document trên trang web của Django [ở đây](https://docs.djangoproject.com/en/3.1/ref/contrib/auth/#django.contrib.auth.models.User).

Mình tóm tắt lại như ở dưới, các bạn nhìn tên đoán chức năng nha.
<br> Chúng ta nên nhìn qua một lượt coi nó có cái gì, sau đó coi qua `AbstractBaseUser` [ở đây](https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser):
<br>**Fields**
- username: bắt buộc
- first_name: 
- last_name: 
- email: 
- password: bắt buộc
- groups: 
- user_permissions: 
- is_staff
- is_active
- is_superuser
- last_login
- date_joined

**Attributes**
- is_authenticated
- is_anonymous

**Methods**
- get_username()
- get_full_name
- get_short_name()
- set_password(raw_password)
- check_password(raw_password)
- set_unusable_password()
- has_usable_password()
- get_user_permissions(obj=None)
- get_group_permissions(obj=None)
- get_all_permissions(obj=None)
- has_perm(perm, obj=None)
- has_perms(perm_list, obj=None)
- has_module_perms(package_name)
- email_user(subject, message, from_email=None, \*\*kwargs)

UserManager có các method sau:
- create_user(username, email=None, password=None, \*\*extra_fields): creates, saves and returns a User.
- create_superuser(username, email=None, password=None, \*\*extra_fields)
- with_perm(perm, is_active=True, include_superusers=True, backend=None, obj=None)

Chúng ta thấy là có nhiều thứ cho chúng ta override tùy theo ý muốn của chúng ta.
<br>Nhưng lỡ đâu khách hàng không muốn login bằng username mà muốn login bằng số điện thoại, hay email thì làm thế nào?
<br>Cách dễ nhất là thừa kế từ `AbstractBaseUser` với attribute `USERNAME_FIELD` như ở dưới, có thể thay đổi `identifier` bằng biến khác, nhưng nhớ phải có `unique=True`:

{% highlight python %}
class MyUser(AbstractBaseUser):
    identifier = models.CharField(max_length=40, unique=True)
    ...
    USERNAME_FIELD = 'identifier'
{% endhighlight %}

Ngoài ra còn có `REQUIRED_FIELDS` là các field được yêu cầu khi tạo user thông qua `createsuperuser`.

{% highlight python %}
class MyUser(AbstractBaseUser):
    ...
    date_of_birth = models.DateField()
    height = models.FloatField()
    ...
    REQUIRED_FIELDS = ['date_of_birth', 'height']
{% endhighlight %}

Lưu ý rằng trong `REQUIRED_FIELDS` không được có `USERNAME_FIELD` hay `password` vì 2 field này chắc chắn được yêu cầu khi tạo User.

Vì có thể trong quá trình làm, User có thể sẽ bị thay đổi nhiều lần, nên tốt nhất ngay từ đầu customize User lẫn UserManager để sau có thêm thắt gì cũng dễ hơn.
<br>Ở dưới là một ví dụ:

{% highlight python %}
class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name,)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
	
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name for user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of user"""
        return self.email
		
{% endhighlight %}

Ở class bên dưới, chúng ta tạo một class UserProfile thừa kế `AbstractBaseUser` và `PermissionsMixin`.
<br>`AbstractBaseUser` thì chúng ta đã đề cập ở trên, còn `PermissionsMixin` sẽ cung cấp các method và field để hỗ trợ model [permission](https://votatdat.github.io/DRF/DRF05) của Django.
<br>Class của chúng ta có 4 field, vì chúng ta sử dụng `USERNAME_FIELD` là email nên chúng ta sẽ đăng nhập bằng email, khi tạo user thì có field bắt buộc khác là `name`.
<br>Vì `objects` là manager mặc định của user nên ở đây chúng ta gán nó với `UserProfileManager` chúng ta tạo ở trên bằng cách thừa kế `BaseUserManager`.
<br>`USERNAME_FIELD` và password là bắt buộc mặc định, chúng ta bắt buộc thêm 1 field là `name`, nên 2 method `create_user` và `create_superuser` có arg là email, name và password.
<br>Lưu ý nên dùng `user.set_password(password)` để password được mã hóa.

Khúc cuối, nhớ đăng ký `AUTH_USER_MODEL` vào `settings.py`, chẳng hạn:

{% highlight python %}
AUTH_USER_MODEL = 'customauth.MyUser'
{% endhighlight %}




















