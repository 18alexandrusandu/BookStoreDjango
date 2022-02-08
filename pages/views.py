from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home_view(*args,**kwargs):
    return HttpResponse("<h1>Hello World</h1>");
    author = models.CharField(max_length=60)
    category = models.CharField(max_length=40)
    description = models.TextField()
    image = models.TextField()
    price = models.FloatField()
    product_name = models.CharField(max_length=100)
    publishing_house = models.CharField(max_length=40)
    year = models.IntegerField()
    in_store = models.IntegerField()