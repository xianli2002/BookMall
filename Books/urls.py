from django.urls import path
from . import views

urlpatterns = [
    path('list/<category>/skus/',views.ListView.as_view()),
    path('search/',views.BookSearchView()),
    path('good_detail/<sku_id>',views.DetailView.as_view()),
    path('content_category/',views.IndexCategoryView.as_view()),
    path('goods_on_index/',views.IndexBooksView.as_view()),
]