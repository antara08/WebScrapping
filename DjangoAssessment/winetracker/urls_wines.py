from django.urls import path
from . import views

app_name = "wines"

urlpatterns = [
    path("", views.wine_list, name="list"),
    path("<uuid:wine_id>/", views.wine_detail, name="detail"),
]
