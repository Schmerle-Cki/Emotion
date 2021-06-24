from django.db import models


class User(models.Model):
    name = models.CharField(unique=True, max_length=50)
    sex = models.CharField(max_length=20)
    age = models.CharField(max_length=20)
    handiness = models.CharField(max_length=20)
    register_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Trial(models.Model):
    characterType = models.CharField(max_length=500)
    groundTruth = models.CharField(max_length=500)
    userChoice = models.CharField(max_length=500)
    correct = models.BooleanField()


class DataEntry(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    data = models.CharField(max_length=8000)
    # ----------------------------------------------------------------
    # 完善Message模型的代码，共有四个字段
    # user: ForeignKey, on_delete策略使用CASCADE
    # title: CharField, max_length=100
    # content: CharField, max_length=500
    # pub_date: DateTimeField, auto_now_add=True
    # ----------------------------------------------------------------
    pass
