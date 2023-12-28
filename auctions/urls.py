from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<str:title>", views.listing, name="listing"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
    path("bid/<str:title>", views.bid, name="bid"),
    path("close_listing/<str:title>", views.close_listing, name="close_listing"),
    path("add_wishlist/<str:title>", views.add_wishlist, name="add_wishlist"),
    path("remove_wishlist/<str:title>", views.remove_wishlist, name="remove_wishlist"),
    path("wishlists", views.wishlists, name="wishlists"),
    path("comment/<str:title>", views.comment, name="comment")
]
