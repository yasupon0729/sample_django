# type: ignore
from django.shortcuts import redirect
from django.conf import settings
from django.views.generic import View, ListView
from base.models import Item
from collections import OrderedDict


class CartListView(ListView):
    model = Item
    template_name = "pages/cart.html"

    def get_queryset(self):
        cart = self.request.session.get("cart", None)
        if cart is None or len(cart) == 0:
            return redirect("/")
        self.queryset = []
        self.total = 0
        for item_pk, quantity in cart["items"].items():
            obj = Item.objects.get(pk=item_pk)
            obj.quantity = quantity  # quantity 新しく定義
            # 税込み合計
            obj.subtotal = int(obj.price * quantity)  # subtotal 新しく定義
            self.queryset.append(obj)
            self.total += obj.subtotal
        self.tax_included_total = int(self.total * (settings.TAX_RATE + 1))
        cart["total"] = self.total
        cart["tax_included_total"] = self.tax_included_total
        self.request.session["cart"] = cart
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["total"] = self.total
            context["tax_included_total"] = self.tax_included_total
        except Exception:
            pass
        return context


class AddCartView(View):

    #     # # getメソッドではトップへリダイレクトする場合はこのようにかけます。
    #     # def get(self, request):
    #     #     return redirect('/')

    def post(self, request):
        item_pk = request.POST.get("item_pk")
        quantity = int(request.POST.get("quantity"))
        cart = request.session.get("cart", None)
        if cart is None or len(cart) == 0:
            items = OrderedDict()
            cart = {"items": items}
        if item_pk in cart["items"]:
            cart["items"][item_pk] += quantity  # 辞書内辞書
        else:
            cart["items"][item_pk] = quantity
        request.session["cart"] = cart
        return redirect("/cart/")


def remove_from_cart(request, pk):
    """かーとの商品削除

    Args:
        request (_type_): _description_
        item_pk (_type_): 削除する商品の主キー（ID）

    Returns:
        _type_: _description_
    """
    cart = request.session.get("cart", None)
    if cart is not None:
        del cart["items"][pk]
        request.session["cart"] = cart
    return redirect("/cart/")
