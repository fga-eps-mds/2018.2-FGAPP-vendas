from django.urls import include, path
from django.conf.urls import url
from orders import views
from .views import create_order

urlpatterns = [
    url(r'^orders/$', views.OrderList.as_view()),
    url(r'^orders/(?P<pk>[0-9]+)/$', views.OrderDetail.as_view()),
    path('create_order', create_order),
]
