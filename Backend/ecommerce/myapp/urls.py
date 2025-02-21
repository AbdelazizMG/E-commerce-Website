from django.urls import path
from . import views

urlpatterns = [
    path("api/Homepage/",views.Homepage, name ="search"),
    path("api/AIsearch/",views.AIsearch_view,name="search"),
    path("api/Normalsearch/",views.Normalsearch_view,name="search"),
    path("", views.home, name = "home")

]