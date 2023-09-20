import app.oauth as oauth
from app.views import CustomerOrdersView
from app.views import CustomersView
from app.views import OrdersView
from django.contrib import admin
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"customers", CustomersView, basename="customers")
router.register(r"orders", OrdersView, basename="orders")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path(
        "customers/<int:customer_id>/orders/",
        CustomerOrdersView.as_view(),
        name="customer-orders",
    ),
    path("oauth_home", oauth.oauth_index, name="oauth_index"),
    path("login", oauth.login, name="login"),
    path("logout", oauth.logout, name="logout"),
    path("callback", oauth.callback, name="callback"),
]
