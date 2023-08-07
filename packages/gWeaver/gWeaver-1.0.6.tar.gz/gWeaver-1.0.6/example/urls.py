from django.urls import path
#from .views import products,product,category,grading,common_indicator,tax_id,product_spec
from . import views

urlpatterns = [

    path('services/',
         views.serviceView.as_view(), name="product"),
]