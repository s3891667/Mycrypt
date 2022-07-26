# from urllib import response

from django.db import models
# import requests,json

# url = "https://api.nomics.com/v1/currencies/ticker?key=5dd42c9bb899c59da6ab6981e745ad8a6ea92d78&ids=BTC,ETH,XRP&interval=1d,30d&convert=EUR&platform-currency=ETH&per-page=100&page=1"

# data = json.loads(requests.get(url).text)
# print(data)


class Coin(models.Model):
    name = models.CharField(max_length=200)
    symbol = models.TextField(default="")

    def __str__(self):
        return self.name


class CoinData(models.Model):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    priceDate = models.DateField('datefield')
    numExchange = models.IntegerField(default=0)

    def __str__(self):
        return str(self.price)


class User(models.Model):
    userName = models.CharField(max_length=30)
    passWord = models.CharField(max_length=50)
    role = models.CharField(max_length=30)
     
    def __str__(self):
        return self.userName


# The model will be classes to display the data such as prices for the users
# then allow them to set track status for the currencies
# display and id of the currency + price -> if the user tick on track
# the system allows the user to see the price graph
