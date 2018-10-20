from django.urls import include, path
from django.conf.urls import url
from orders import views
from .views import create_order, user_orders, buyer_orders

urlpatterns = [
    url(r'^orders/$', views.OrderList.as_view()),
    url(r'^orders/(?P<pk>[0-9]+)/$', views.OrderDetail.as_view()),
    path('create_order/', create_order),
    path('user_orders/', user_orders),
    path('buyer_orders/', buyer_orders),
]
