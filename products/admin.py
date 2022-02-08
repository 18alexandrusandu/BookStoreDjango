from django.contrib import admin

# Register your models here.S
from .models2 import *

admin.site.register(Products)
admin.site.register(Users)
admin.site.register(Orders)
admin.site.register(ProductsOrder)
# Products.objects.create(
#     author = "J.K Rolling",
#     category = "Beletristica",
#     description ="a new book",
#     image = "https://mcdn.elefant.ro/mnresize/150/150/is/product-images/carte-straina/gardners/20200915/ec8eb10f/b017/4bd2/8b70/2e849f8c4774/ec8eb10f-b017-4bd2-8b70-2e849f8c4774_1.jpg",
#     price = 40,
#     product_name ="Harry Potter and philosopher's stone",
#     publishing_house ="Bloomsbury",
#     year = 2001,
#     in_store=100 );