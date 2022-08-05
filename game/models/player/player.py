from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # User是继承的“表格”；CASCADE是当user删除时，关联他的player也会一并删除
    photo = models.URLField(max_length=256, blank=True)
    openid = models.CharField(default="", max_length=50, blank=True, null=True)

    def __str__(self):  # 让player的信息显示在后台管理员页面
        return str(self.user)
