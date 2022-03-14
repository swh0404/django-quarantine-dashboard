from django.urls import path
from dashboard import views

urlpatterns = [
    path('/hello', views.hello),
    path('',views.total)
]
