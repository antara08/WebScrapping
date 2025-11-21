from django.urls import path
from . import views

app_name = "stores"

urlpatterns = [
    path("new/", views.store_new, name="new"),
]
