from django.contrib import admin
from django.urls import path
from base.views.cart_views import CartListView, AddCartView, remove_from_cart
from base.views.item_views import IndexListView, ItemDetailView

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    # Cart
    path("cart/add/", AddCartView.as_view(), name="add_cart"),
    path("cart/remove/<str:pk>/", remove_from_cart, name="remove_from_cart"),
    path("cart/", CartListView.as_view(), name="cart"),
    # Items
    path("items/<str:pk>/", ItemDetailView.as_view(), name="item"),
    # Top page
    path(
        "", IndexListView.as_view(), name="index"
    ),  # top page クラスビューの場合は、as_view()をつける
]
