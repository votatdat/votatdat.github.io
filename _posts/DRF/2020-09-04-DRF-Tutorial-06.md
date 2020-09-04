---
layout: post
title: DRF Tutorial
subtitle: "Phần 06: giới thiệu về User Authentication"
cover-img: /assets/img/planet.jpg
thumbnail-img: /assets/img/thumb.png
share-img: /assets/img/planet.jpg
tags: [Python, Django, DRF]
---

Nội dụng phần này:
- Giới thiệu các loại authentication.
- Thiết lập authentication trong settings.py.

Danh sách đầy đủ bài học **[ở đây](https://votatdat.github.io/DRF)**.

Ở phần trước, chúng ta đã tìm hiểu về `permission` hay là `authorization`. 
<br>Ở phần này, chúng ta tìm hiểu `authentication` là qui trình mà cho phép người dùng có thể đăng ký, login và logout.

Có nhiều kiểu `authentication`, DRF hỗ trợ 4 kiểu dựng sẵn:
* `BasicAuthentication`
* `SessionAuthentication`
* `TokenAuthentication`
* `RemoteUserAuthentication`

Chúng ta cũng có thể custom authentication hoặc dùng các 3rd party package.
<br>Đọc thêm [ở đây](https://www.django-rest-framework.org/api-guide/authentication/#sessionauthentication).

## Basic Authentication
Luồng request/response của nó đại loại như vầy:
1. Phía Client sẽ tạo một `HTTP request`.
2. Phía Server sẽ trả lại một `HTTP response` chứa code `401 (Unauthorized)` chưa được phép và `WWW-Authenticate HTTP header` với chi tiết làm sao để authorize.
3. Phía Client sẽ gửi lại một chứng nhận `credential` thông qua `Authorization HTTP header`.
4. Phía Server kiểm tra chứng nhận `credentials` và trả lại `200 OK` hoặc `403 Forbidden status`.

Đại khái như hình dưới:

![](/assets/piks/DRF/DRF06_basicauth.PNG)

Ưu điểm:
- Đơn giản

Nhược điểm:
- Với mỗi request từ phía Client, phía Server phải tìm và xác nhận lại username và password.
- `Credentials` dù được mã hóa bằng [base64](https://en.wikipedia.org/wiki/Base64) nhưng truyền qua Internet qua lại nhiều lần là không an toàn.

## Session Authentication
Luồng request/response của nó đại loại như vầy:
1. Một user nào đó login dùng username/password để lấy `credential`.
2. Phía Server xác nhận `credential` đó là đúng và tạo ra một `session object` được lưu trữ trên database.
3. Phía Server gửi cho phía Client một `session ID` (không phải là `session object`) được lưu trữ như là một `cookie` trên trình duyệt (browser).
4. Tất cả mọi request trong tương lại đều phải có `session ID` nằm trong `HTTP header` và được xác nhận bởi database, sau đó các request được tiến hành.
5. Một khi user log out ra khỏi ứng dụng (application), thì `session ID` sẽ bị hủy ở cả hai phía Client và Server.
6. Nếu user log in một lần nữa, thì một `session ID` hoàn toàn mới sẽ được tạo ra như là một `cookie` ở phía Client.

DRF sử dụng kết hợp Basic Authentication và Session Authentication.
<br>Django thì dùng Session, nhưng `session ID` trong `HTTP header` thì dùng Basic.


Ưu điểm: 
- An toàn hơn do `credential` chỉ được gửi đi một lần.

Nhược điểm:
- `session ID` chỉ hợp lệ khi log in trên trình duyệt (dạng `cookie`), tuy nhiên điều này không thực hiện được trên các app di động.
- `session object` phải được giữ up-to-date, có thể khó khăn với các website lớn.
- `cookie` vẫn phải được gửi cho mỗi request.

## Token Authentication
Đây là các tiếp cận phổ biến gần đây. 
<br>Một khi user gửi `credential` dến Server, thì một `token` duy nhất là được tạo ra và lưu trên phía Client như một `cookies` hoặc ở [local storage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage).
<br>`Token` này sẽ được thêm vào trong header của mỗi HTTP request và phía Server sẽ xác nhận rằng user này có hợp lệ hay không.

**Cookies vs localStorage**
<br>`Cookie`:
- Được sử dụng để đọc thông tin ở phía Server
- Có kích thước nhỏ (4KB) và được tự động gửi đi ở mỗi `HTTP request`. 

`LocalStorage`:
- Được thiết kế cho thông tin ở phía Client. 
- Có kích thước lớn hơn hẳn (5120KB) và nội dung của nó không được mặc định gửi ở mỗi `HTTP request`. 

`Token` được lưu trữ ở cả `cookies` và `localStorage` thì dễ tổn thương bởi các tấn công XSS. 
<br>Thực tế hiện này là lưu trữ `token` ở `cookie` với `httpOnly` và `cookie flags` an toàn.

Ưu điểm: 
- `Token` được lưu trữ ở phía Client nên phía Server không phải bảo trì up-to-date.
- Sử dụng được cho cả trình duyệt lẫn app điện thoại mà `session ID` không làm được.

Nhược điểm:
- `Token` có thể trở nên lớn.

Luồng request/response đại khái như hình dưới:

![](/assets/piks/DRF/DRF06_tokenauth.PNG)

Có nhiều 3rd party package có thể được thêm vào để hỗ trợ DRF, chẳng hạn JSON Web Tokens (JWTs), Auth0.

## Thiết lập Authentication
Đầu tiên chúng ta phải thêm `authentication` vào `settings.py`. Có thể coi thêm về setting của DRF [ở đây](https://www.django-rest-framework.org/api-guide/settings/).

{% highlight python %}
# blog_project/settings.py
REST_FRAMEWORK = {
	'DEFAULT_PERMISSION_CLASSES': [
		'rest_framework.permissions.IsAuthenticated',
	],
	
	'DEFAULT_AUTHENTICATION_CLASSES': [ # thêm mới đoạn này
		'rest_framework.authentication.SessionAuthentication',
		'rest_framework.authentication.TokenAuthentication'
	],
}
{% endhighlight %}

Để tạo `token` phía Server, chúng ta cần `authtoken` app của DRF, mặc dù nó đi cùng với DRF nhưng chúng ta phải khai báo trong `settings.py`.

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
	'rest_framework.authtoken', # Thêm mới cái này
	
	'posts.apps.PostsConfig',
]
{% endhighlight %}

Vì có app mới nên chúng ta phải migrate lại và runserver, vào trang admin chúng ta sẽ thấy có mục Tokens.

{% highlight python %}
python manage.py migrate

python manage.py runserver
{% endhighlight %}

![](/assets/piks/DRF/DRF06_token.PNG)

Khi nhấn vào Tokens, chúng ta sẽ không thấy có token nào, vì app này được tạo sau khi các user được tạo.

![](/assets/piks/DRF/DRF06_token2.PNG)


Phần này tạm thời tới đây, chi tiết hơn phần `Authentication` sẽ ở [Phần 07](https://votatdat.github.io/2020-09-04-DRF-Tutorial-07).

{% highlight python %}

{% endhighlight %}