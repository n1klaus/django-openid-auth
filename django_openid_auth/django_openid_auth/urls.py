from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import CustomersView, OrdersView, CustomerOrdersView

router = DefaultRouter()
router.register(r'customers', CustomersView, basename='customers')
router.register(r'orders', OrdersView, basename='orders')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('customers/<int:customer_id>/orders/', CustomerOrdersView.as_view(), name='customer-orders'),
]
