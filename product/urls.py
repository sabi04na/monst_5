from django.urls import path
from . import views
from .views import CategoryListCreateView, CategoryDetailView, ProductListCreateView, ProductDetailView, ReviewListCreateView, ReviewDetailView, ProductReviewsListView

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view()),
    path('categories/<int:pk>/', CategoryDetailView.as_view()),
    path('products/', ProductListCreateView.as_view()),
    path('products/<int:pk>/', ProductDetailView.as_view()),
    path('products/reviews/', ProductReviewsListView.as_view()),
    path('reviews/', ReviewListCreateView.as_view()),
    path('reviews/<int:pk>/', ReviewDetailView.as_view()),

]