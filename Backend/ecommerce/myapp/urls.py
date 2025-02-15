from django.urls import path
from . import views

urlpatterns = [
    path("add/",views.add_person, name ="add"),
    path("show/",views.show_person, name ="show"),
    path("api/Categorysearch/",views.Categorysearch_view, name ="show"),
    path("api/Homepage/",views.Homepage, name ="search"),
    path("api/AIsearch/",views.AIsearch_view,name="search"),
    path("api/Normalsearch/",views.Normalsearch_view,name="search"),
    path("", views.home, name = "home")

]