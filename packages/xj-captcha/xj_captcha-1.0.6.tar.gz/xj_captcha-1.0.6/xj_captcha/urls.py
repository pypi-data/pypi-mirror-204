# 应用名称
from django.urls import re_path

from xj_captcha.apis.SmsApis import SmsApis
from .apis import send_short_message

app_name = 'captcha'

urlpatterns = [

    re_path(r'^send_message/?$', send_short_message.SendShortMessag.as_view(), ),

    re_path(r'^send/?$', SmsApis.send),  # 发送短信(新命名)
    re_path(r'^check/?$', SmsApis.check),  # 检测验证码是否正确

]
