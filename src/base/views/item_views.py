from django.views.generic import ListView, DetailView
from base.models import Item


from config.logger import get_logger

logger = get_logger("base.views.item_views")


class IndexListView(ListView):
    """アイテム一覧取得"""

    # 変数をオーバーライド
    model = Item
    template_name = "pages/index.html"
    context_object_name = "object_list"

    # override
    def get(self, request, *args, **kwargs):
        logger.debug("IndexListView get")
        return super().get(request, *args, **kwargs)


class ItemDetailView(DetailView):
    """個別のアイテムの取得"""

    model = Item
    template_name = "pages/item.html"
    context_object_name = "object"
