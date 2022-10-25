from haystack import indexes
from .models import SKU

class BookSKUIndex(indexes.SearchIndex,indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        # 返回 需要检索的 模型类
        return SKU

    # 返回 数据。对该数据 建立索引。
    def index_queryset(self, using=None):
        return self.get_model().objects.all()