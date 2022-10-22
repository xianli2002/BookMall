from django.urls import path
from . import views

urlpatterns = [
    # path('',views.IndexView.as_view()),
    # path('index.html',views.IndexView.as_view()),
    path('list/<category>/skus/',views.ListView.as_view()),
    # path('search/',views.SKUSearchView()),
    path('detail/<sku_id>/',views.DetailView.as_view()),
    # path('goods/<sku_id>.html/',views.DetailView.as_view()),
    path('content_category/',views.IndexCategoryView.as_view()),
    path('goods_on_index/',views.IndexBooksView.as_view()),
]