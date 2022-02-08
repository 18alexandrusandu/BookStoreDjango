from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import *
import requests

from twilio.rest import Client
import json
import jwt
from .models2 import *
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt,ensure_csrf_cookie
# Create your views here.

account_sid = "AC79c39c4dd399dacc7499e2eb4c37a09e"
# Your Auth Token from twilio.com/console
auth_token  = "d7167ab7300e9979623ba84e8c59971d";
trialNumber="+16015415119";

client = Client(account_sid, auth_token)









def send_products(*args,**kwargs):
    data=Products.objects.all()
    sendData=[]
    for i in data:
         i=model_to_dict(i)
         sendData.append(i)
    return JsonResponse( sendData,safe=False)


def send_product(request,id):
    data=Products.objects.get(id_product=id);
    return JsonResponse(model_to_dict(data),safe=False)

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

@csrf_exempt
def log_in(request):


   auth=json.loads(request.body.decode("utf-8"));
   #print("AUTH",auth);
   user=Users.objects.get(user_name=auth["userName"]);
   message = client.messages.create(
       to="+4"+user.phone,
       from_=trialNumber,
       body="Hello from Django thank you for log in!");
   if(user.password==auth["password"]):
       print("HURRAY")
       encoded_jwt = jwt.encode({"username":auth["userName"]},auth["password"] , algorithm="HS256");
       return JsonResponse({"jwt" : encoded_jwt},safe=False);
   else:
       print("NOOOOOO")
   raise ValidationError("password or username not right");



def findbyusername(request):
   username=request.GET.get("userName");
   print("uername",username);
   user2 = Users.objects.get(user_name=username);
   role=UserRole.objects.get(user__id_user=user2.id_user);
   dict=model_to_dict(user2);
   tempDict1={}
   tempDict1["roleData"]={"id":role.role.id_role,"role":role.role.role}
   tempDict1["userDt"]=role.user.id_user;
   tempDict1["id"]=role.id_user_role;
   dict["userRole"]=[];
   dict["userRole"].append(tempDict1);
   return JsonResponse(dict);



def findbyid(request,id):
    user = Users.objects.get(id_user=id);
    return JsonResponse(model_to_dict(user))

@csrf_exempt
def sign_in_admin(request):
    user1= json.loads(request.body.decode("utf-8"));
    user2=Users.objects.create(
    address = user1["address"],
    card_number = user1["cardNumber"],
    email = user1["email"],
    first_name = user1["firstName"],
    last_name = user1["lastName"] ,
    password = user1["password"],
    phone = user1["phone"],
    user_name =user1["userName"]
    );
    role2=Roles.objects.get(role="ROLE_ADMIN");
    userRole=UserRole.objects.create(user=user2,role=role2);
    dict=model_to_dict(user2);
    return JsonResponse(model_to_dict(user2));


@csrf_exempt
def sign_in(request):
    user1= json.loads(request.body.decode("utf-8"));
    user2=Users.objects.create(
    address = user1["address"],
    card_number = user1["cardNumber"],
    email = user1["email"],
    first_name = user1["firstName"],
    last_name = user1["lastName"] ,
    password = user1["password"],
    phone = user1["phone"],
    user_name =user1["userName"]
    );
    role2=Roles.objects.get(role="ROLE_USER");
    userRole=UserRole.objects.create(user=user2,role=role2);
    dict=model_to_dict(user2);
    message = client.messages.create(
        to="+4" + user1["phone"],
        from_=trialNumber,
        body="Hello from Django thank you for signing in!");
    return JsonResponse(model_to_dict(user2));


@csrf_exempt
def receive_product(request):
  product=json.loads(request.body.decode("utf-8"));
  newprod=Products.objects.create(  author =product["author"],
    category = product["category"],
    description =product["description"],
    image =product["image"] ,
    price = product["price"],
    product_name = product["productName"],
    publishing_house=product["publishingHouse"] ,
    year =product["year"] ,
    in_store =product["inStore"]);
  return JsonResponse(model_to_dict(newprod))


@csrf_exempt
def receive_order(request):
    order= json.loads(request.body.decode("utf-8"));
    print("order:",order);
    print("here should come it", order);
    products2=order["productOrderList"];
    newObject=order;
    newObject["productOrderList"]=[];
    print(newObject);
    user=Users.objects.get(id_user=newObject["userData"]["id"]);
    objc=Orders.objects.create(date_time=newObject["dateTime"],
    price=newObject["price"],
    user=user);

    print(objc);

    for product in products2:
      productProduct=Products.objects.get(id_product=product["product"]["id"])
      ProductsOrder.objects.create(
          amount=product["amount"],
          order=objc,
          product=productProduct
      )
      message = client.messages.create(
          to="+4" + user.phone,
          from_=trialNumber,
          body="Hello "+user.user_name+" from Django thank you for buying at our bookstore");

    return JsonResponse(model_to_dict(objc));

@csrf_exempt
def send_orders(request):
    print("send orders")
    data = Orders.objects.all()
    sendData = []
    for i in data:
        j = model_to_dict(i)
        user=Users.objects.get(id_user=i.user.id_user);
        j["user"]=model_to_dict(user);
        prodList=ProductsOrder.objects.filter(order=i);
        j["product_order_list"]=[];
        for prod in prodList:
             product=Products.objects.get(id_product=prod.product.id_product)
             k=model_to_dict(prod);
             k["product"]=model_to_dict(product);
             j["product_order_list"].append(k)
        sendData.append(j);
    return JsonResponse(sendData, safe=False);

def send_users(request):
    data = Users.objects.all()
    sendData = []
    for i in data:
        role = UserRole.objects.get(user__id_user=i.id_user);
        dict = model_to_dict(i);
        tempDict1 = {}
        tempDict1["roleData"] = {"id": role.role.id_role, "role": role.role.role}
        tempDict1["userDt"] = role.user.id_user;
        tempDict1["id"] = role.id_user_role;
        dict["userRole"] = [];
        dict["userRole"].append(tempDict1);
        sendData.append(dict);
    return JsonResponse(sendData);


def delete_user(request,id):
    data = Users.objects.get(id_user=id)
    role = UserRole.objects.get(user__id_user=data.id_user);
    role.delete();
    orders=Orders.objects.filter(user=data);
    for order in orders:
        prod=ProductsOrder.objects.filter(order=order);
        for prod2 in prod:
            prod2.delete()
        prod.delete()
        order.delete();

    data.delete();
    return JsonResponse({"good message":"element deleted"}, safe=False);


def delete_order(request):
    print("send orders")
    order=json.loads(request.body.decode("utf-8"));
    print("order:",order)
    data = Orders.objects.get(id_order=order["id_order"]);
    prodList=ProductsOrder.objects.filter(order=data);
    for prod in prodList:
        prod.delete();
    data.delete()
    return JsonResponse({"good message":"element deleted"}, safe=False);

@csrf_exempt
def delete_product(request):
  product = json.loads(request.body.decode("utf-8"));
  print("product:",product)
  data=Products.objects.get( id_product=product["id_product"]);
  prodList = ProductsOrder.objects.filter(product=data);
  for prod in prodList:
      prod.delete();
  data.delete();
  return JsonResponse({"good message":"element deleted"},safe=False)


def filterByProductName(request):
    name=request.GET.get("productName");
    data=Products.objects.filter(product_name=name);
    sendData = []
    for i in data:
        i = model_to_dict(i)
        sendData.append(i)
    return JsonResponse(sendData, safe=False)

def filterByCategory(request):
    name = request.GET.get("category");
    data = Products.objects.filter(category=name);
    sendData = []
    for i in data:
        i = model_to_dict(i)
        sendData.append(i)
    return JsonResponse(sendData, safe=False)
def filterByAuthor(request):
    name = request.GET.get("author");
    data = Products.objects.filter(author=name);
    sendData = []
    for i in data:
        i = model_to_dict(i)
        sendData.append(i)
    return JsonResponse(sendData, safe=False)
def filterByPublish(request):
    name = request.GET.get("publishHouse");
    data = Products.objects.filter(publishing_house=name);
    sendData = []
    for i in data:
        i = model_to_dict(i)
        sendData.append(i)
    return JsonResponse(sendData, safe=False)
def filterByYear(request):
    name = request.GET.get("year");
    data = Products.objects.filter(year=name);
    sendData = []
    for i in data:
        i = model_to_dict(i)
        sendData.append(i)
    return JsonResponse(sendData, safe=False)
def filterByPrice(request):
    name = request.GET.get("price");
    data = Products.objects.filter(price=name);
    sendData = []
    for i in data:
        i = model_to_dict(i)
        sendData.append(i)
    return JsonResponse(sendData, safe=False)
def filterByPrice2(request):
    name = request.GET.get("price");
    data = Products.objects.filter(price__lte =name);
    sendData = []
    for i in data:
        i = model_to_dict(i)
        sendData.append(i)
    return JsonResponse(sendData, safe=False)
def filterByPrice3(request):
    name = request.GET.get("price");
    data = Products.objects.filter(price__gte=name);
    sendData = []
    for i in data:
        i = model_to_dict(i)
        sendData.append(i)
    return JsonResponse(sendData, safe=False)

def filterByOrderTime(request):
    name = request.GET.get("date");
    data = Orders.objects.filter(date_time__date=name);
    sendData = []
    for i in data:
        j = model_to_dict(i)
        user = Users.objects.get(id_user=i.user.id_user);
        j["user"] = model_to_dict(user);
        prodList = ProductsOrder.objects.filter(order=i);
        j["product_order_list"] = [];
        for prod in prodList:
            product = Products.objects.get(id_product=prod.product.id_product)
            k = model_to_dict(prod);
            k["product"] = model_to_dict(product);
            j["product_order_list"].append(k)

        sendData.append(j)
    return JsonResponse(sendData, safe=False)
def filterByOrderUsername(request):
    name = request.GET.get("user");
    data = Orders.objects.filter();
    sendData = []
    for i in data:
        j = model_to_dict(i)
        user = Users.objects.get(id_user=i.user.id_user);
        j["user"] = model_to_dict(user);
        prodList = ProductsOrder.objects.filter(order=i);
        j["product_order_list"] = [];
        for prod in prodList:
            product = Products.objects.get(id_product=prod.product.id_product)
            k = model_to_dict(prod);
            k["product"] = model_to_dict(product);
            j["product_order_list"].append(k)

        sendData.append(j)
    return JsonResponse(sendData, safe=False)
def filterByOrderUserName(request):
    name = request.GET.get("user");
    name=name.split();
    print("names:",name);
    data = Orders.objects.filter(user__first_name=name[0],  user__last_name=name[1] );
    sendData = []
    for i in data:
        j = model_to_dict(i)
        user = Users.objects.get(id_user=i.user.id_user);
        j["user"] = model_to_dict(user);
        prodList = ProductsOrder.objects.filter(order=i);
        j["product_order_list"] = [];
        for prod in prodList:
            product = Products.objects.get(id_product=prod.product.id_product)
            k = model_to_dict(prod);
            k["product"] = model_to_dict(product);
            j["product_order_list"].append(k)

        sendData.append(j)
    return JsonResponse(sendData, safe=False)

def filterByOrderPrice(request):
    print("Da intra");
    price = request.GET.get("price");
    data = Orders.objects.filter(price=price);
    sendData = [];
    for i in data:
        j = model_to_dict(i)
        user = Users.objects.get(id_user=i.user.id_user);
        j["user"] = model_to_dict(user);
        prodList = ProductsOrder.objects.filter(order=i);
        j["product_order_list"] = [];
        for prod in prodList:
            product = Products.objects.get(id_product=prod.product.id_product)
            k = model_to_dict(prod);
            k["product"] = model_to_dict(product);
            j["product_order_list"].append(k)

        sendData.append(j)
    return JsonResponse(sendData, safe=False)
def filterByOrderPrice2(request):
    price = request.GET.get("price");
    data = Orders.objects.filter(price__lte=price);
    sendData=[];
    for i in data:
        j = model_to_dict(i)
        user = Users.objects.get(id_user=i.user.id_user);
        j["user"] = model_to_dict(user);
        prodList = ProductsOrder.objects.filter(order=i);
        j["product_order_list"] = [];
        for prod in prodList:
            product = Products.objects.get(id_product=prod.product.id_product)
            k = model_to_dict(prod);
            k["product"] = model_to_dict(product);
            j["product_order_list"].append(k)

        sendData.append(j)
    return JsonResponse(sendData, safe=False)
def filterByOrderPrice3(request):
    price = request.GET.get("price");
    data = Orders.objects.filter(price__gte=price);
    sendData = []
    for i in data:
        j = model_to_dict(i)
        user = Users.objects.get(id_user=i.user.id_user);
        j["user"] = model_to_dict(user);
        prodList = ProductsOrder.objects.filter(order=i);
        j["product_order_list"] = [];
        for prod in prodList:
            product = Products.objects.get(id_product=prod.product.id_product)
            k = model_to_dict(prod);
            k["product"] = model_to_dict(product);
            j["product_order_list"].append(k)

        sendData.append(j)
    return JsonResponse(sendData, safe=False)
def filterByOrderProduct(request):
    product = request.GET.get("id");
    productOrder=ProductsOrder.objects.filter(product__id_product=product)
    data = [];
    for prod in productOrder:
       order=Orders.objects.get(id_order=prod.order.id_order);
       data.append(order);

    sendData = [];
    for i in data:
        j = model_to_dict(i)
        user = Users.objects.get(id_user=i.user.id_user);
        j["user"] = model_to_dict(user);
        prodList = ProductsOrder.objects.filter(order=i);
        j["product_order_list"] = [];
        for prod in prodList:
            product = Products.objects.get(id_product=prod.product.id_product)
            k = model_to_dict(prod);
            k["product"] = model_to_dict(product);
            j["product_order_list"].append(k)

        sendData.append(j)
    return JsonResponse(sendData, safe=False)
def filterByOrderAmount(request):
    amount = request.GET.get("amount");
    data=[];
    allOrders=Orders.objects.all();
    for order in allOrders:
        totalAmount=0;
        products=ProductsOrder.objects.filter(order__id_order=order.id_order)
        for prod in products:
           totalAmount+=prod.amount;
        print("order_",order.id_order,"amount:",totalAmount,"desired:",amount);
        if int(totalAmount) == int(amount):
            print("da");
            data.append(order);

    sendData = [];
    for i in data:
        j = model_to_dict(i)
        user = Users.objects.get(id_user=i.user.id_user);
        j["user"] = model_to_dict(user);
        prodList = ProductsOrder.objects.filter(order=i);
        j["product_order_list"] = [];
        for prod in prodList:
            product = Products.objects.get(id_product=prod.product.id_product)
            k = model_to_dict(prod);
            k["product"] = model_to_dict(product);
            j["product_order_list"].append(k)

        sendData.append(j)
    print("send data:",sendData);
    return JsonResponse(sendData, safe=False)
def filterByOrderAmount2(request):
    amount = request.GET.get("amount");
    data = [];
    amount = request.GET.get("amount");
    data = [];
    allOrders = Orders.objects.all();
    for order in allOrders:
        totalAmount = 0;
        products = ProductsOrder.objects.filter(order__id_order=order.id_order)
        for prod in products:
            totalAmount += prod.amount;
        print("order_", order.id_order, "amount:", totalAmount, "desired:", amount);
        if int(totalAmount) < int(amount):
            print("da");
            data.append(order);
    sendData=[];
    for i in data:
        j = model_to_dict(i)
        user = Users.objects.get(id_user=i.user.id_user);
        j["user"] = model_to_dict(user);
        prodList = ProductsOrder.objects.filter(order=i);
        j["product_order_list"] = [];
        for prod in prodList:
            product = Products.objects.get(id_product=prod.product.id_product)
            k = model_to_dict(prod);
            k["product"] = model_to_dict(product);
            j["product_order_list"].append(k)

        sendData.append(j)
    return JsonResponse(sendData, safe=False)
def filterByOrderAmount3(request):
    amount = request.GET.get("amount");
    data = [];
    allOrders = Orders.objects.all();
    for order in allOrders:
        totalAmount = 0;
        products = ProductsOrder.objects.filter(order__id_order=order.id_order)
        for prod in products:
            totalAmount += prod.amount;
        print("order_", order.id_order, "amount:", totalAmount, "desired:", amount);
        if int(totalAmount) > int(amount):
            print("da");
            data.append(order);
    sendData=[];
    for i in data:
        j = model_to_dict(i)
        user = Users.objects.get(id_user=i.user.id_user);
        j["user"] = model_to_dict(user);
        prodList = ProductsOrder.objects.filter(order=i);
        j["product_order_list"] = [];
        for prod in prodList:
            product = Products.objects.get(id_product=prod.product.id_product)
            k = model_to_dict(prod);
            k["product"] = model_to_dict(product);
            j["product_order_list"].append(k)

        sendData.append(j)
    return JsonResponse(sendData, safe=False)

def update_user(request):
    user=json.loads(request.body.decode("utf-8"));
    user=Users.objects.filter(id_user=user["id_user"]).update(
        address=user["address"],
        card_number=user["card_number"],
        email=user["email"],
        first_name=user["first_name"],
        last_name=user["last_name"],
        password=user["password"],
        phone =user["phone"],
        user_name=user["user_name"],

    );
    return JsonResponse(user, safe=False);

def update_order(request):
    order = json.loads(request.body.decode("utf-8"));
    order2 = Orders.objects.filter(id_order=order["id_order"]).update(
    date_time=order["date_time"],user=order["user"]);
    return JsonResponse(model_to_dict(order2), safe=False);
def update_product(request):

    id = request.GET.get("id");
    product =Products.objects.filter(id_product=id).update();
    return JsonResponse(model_to_dict(product), safe=False);

def update_users(request):
    users = json.loads(request.body.decode("utf-8"));
    sendData = [];
    for user in users:
      user2 = update_user();
      sendData.append(model_to_dict(user2));
    return JsonResponse(model_to_dict(user), safe=False);
def update_orders(request):
    orders= json.loads(request.body.decode("utf-8"));
    sendData = [];
    for order in orders:
       print("order:",order);
       order2 = Orders.objects.filter(id_order=order["id_order"]).update(
           date_time=order["date_time"], user=order["user"]["id_user"],
           price=order["price"]

       );
       sendData.append(order2);
    return JsonResponse(sendData, safe=False);

def update_products(request):
    products = json.loads(request.body.decode("utf-8"));
    sendData = [];
    for product in products:
        print("product:",product);
        product2 = Products.objects.filter(id_product=product["id_product"]).update(
            author=product["author"],
            category=product["category"],
            description=product["description"],
            image=product["image"],
            price=product["price"],
            product_name=product["product_name"],
            publishing_house=product["publishing_house"],
            year=product["year"],
            in_store=product["in_store"],

        );
        sendData.append(product2);
    return JsonResponse(sendData, safe=False);
