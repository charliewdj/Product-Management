from django.urls import path

from . import views

app_name = "part_management"

urlpatterns = [
    path("", views.index, name="Index"),
    path("login/", views.login, name="Login"),
    path("main-menu/", views.main_menu, name="MainMenu"),
    path("product-upload/", views.product_upload, name="ProductUpload"),
    path("product-info/", views.product_info, name="ProductInfo"),
    path("part-upload/", views.part_upload, name="PartUpload"),
    path("part-search/", views.part_search, name="PartSearch"),
]
