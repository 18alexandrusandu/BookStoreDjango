"""ptoj521 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from django.views.decorators.csrf import csrf_exempt
from pages import views
from products import views as view2
from rest_framework_simplejwt import views as jwt_views


from products.models2 import MyTokenObtainPairView;

urlpatterns = [

    path('admin/', admin.site.urls),
    path("",views.home_view,name="home"),
    path("api/product/all",view2.send_products),
    path("api/product/<int:id>", view2.send_product),
    path("api/product/add/", view2.receive_product),
    path("api/order/add", view2.receive_order),
    path('api/order/', view2.send_orders),
    path("api/user/add",csrf_exempt(view2.sign_in)),
    path("api/user/addadmin",view2.sign_in_admin),
    path('api/token/',jwt_views.TokenObtainPairView.as_view(),name ='token_obtain_pair'),
    path('api/token/refresh/',jwt_views.TokenRefreshView.as_view(), name ='token_refresh'),
    path('api/user/findUserByUserName',view2.findbyusername),
    path("api/product/findByPrice",view2.filterByPrice),
    path('api/product/findByPriceThatAreCheaper',view2.filterByPrice2),
    path("api/product/findByPriceThatAreExpensive",view2.filterByPrice3),
    path("api/product/publishingHouse",view2.filterByPublish),
    path("api/product/findByYear",view2.filterByYear),
    path("api/product/findByProductName",view2.filterByProductName),
    path("api/product/findByCategory",view2.filterByCategory),
    path("api/product/findByAuthor",view2.filterByAuthor),
    path('api/order/Date', view2.filterByOrderTime),
    path("api/order/findByUserName",view2.filterByOrderUserName),
    path("api/order/findByUsername",view2.filterByOrderUsername),
    path("api/order/findByPrice",view2.filterByOrderPrice),
    path("api/order/findByPriceThatAreExpensive",view2.filterByOrderPrice2),
    path("api/order/findByPriceThatAreCheaper",view2.filterByOrderPrice3),
    path("api/order/findByAmount",view2.filterByOrderAmount),
    path("api/order/findByAmountThatAreLess",view2.filterByOrderAmount2),
    path("api/order/findByAmountThatAreMore",view2.filterByOrderAmount3),
    path("api/order/findByProductId",view2.filterByOrderProduct),
    path("api/user/", view2.send_users),
    path("api/user/login", (view2.log_in)),
    path("api/order/delete",view2.delete_order),
    path("api/product/delete",view2.delete_product),
    path("api/user/update",view2.update_user),
    path("api/order/changeall",view2.update_orders),
    path("api/product/changeall",view2.update_products),


];

