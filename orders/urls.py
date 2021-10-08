from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _

app_name = 'orders'

urlpatterns = [
    path(_('create/'), views.order_create, name='order_create'),
    path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin/order/<int:order_id>/pdf/', views.admin_order_pdf, name='admin_order_pdf'),
    path('order_list/', views.order_list, name='order_list'),
    path('order_list/<int:order_id>/order_details', views.order_details, name='order_details'),
    path('order_list/<int:order_id>/pdf/', views.order_pdf, name='order_pdf'),
]
