from email.policy import default
from django.conf import settings
from django.db import models


class Coin(models.Model):
    symbol = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=200)
    icon = models.URLField(max_length=200,default='url')
    def __str__(self):
        return self.name


class User(models.Model):
    id = models.AutoField(primary_key=True)
    userName = models.CharField(max_length=30)
    passWord = models.CharField(max_length=50)
    role = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    coin = models.ManyToManyField(Coin)
    verified = models.BooleanField()

    def __str__(self):
        return self.userName


class Content(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    date = models.DateField()
    author = models.CharField(max_length=30)
    source = models.URLField(max_length=200)
    status = models.CharField(max_length=1, choices=[
        ('d', 'Draft'),
        ('p', 'Published'),
        ('w', 'Withdrawn'),
    ])
    def __str__(self):
        return self.title

# The model will be classes to display the data such as prices for the users
# then allow them to set track status for the currencies
# display and id of the currency + price -> if the user tick on track
# the system allows the user to see the price graph
