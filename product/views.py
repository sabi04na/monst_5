from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductListSerializer, ProductDetailSerializer, ReviewSerializer, ProductReviewsSerializer


@api_view(['GET'])
def category_list_view(request):
    categories = Category.objects.all()
    ser = CategorySerializer(categories, many=True)
    return Response(ser.data)

@api_view(['GET'])
def category_detail_view(request, id):
    try:
        cat = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response({"error": "Категория не найдена"}, status=status.HTTP_404_NOT_FOUND)
    ser = CategorySerializer(cat)
    return Response(ser.data)


@api_view(['GET'])
def product_list_view(request):
    products = Product.objects.select_related("category").all()
    ser = ProductListSerializer(products, many=True)
    return Response(ser.data)

@api_view(['GET'])
def product_detail_view(request, id):
    try:
        prod = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({"error": "Товар не найден"}, status=status.HTTP_404_NOT_FOUND)
    ser = ProductDetailSerializer(prod)
    return Response(ser.data)


@api_view(['GET'])
def review_list_view(request):
    reviews = Review.objects.all()
    ser = ReviewSerializer(reviews, many=True)
    return Response(ser.data)


@api_view(['GET'])
def review_detail_view(request, id):
    try:
        rev = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response({"error": "Отзыв не найден"}, status=status.HTTP_404_NOT_FOUND)
    ser = ReviewSerializer(rev)
    return Response(ser.data)

@api_view(['GET'])
def product_with_reviews_list_view(request):
    products = Product.objects.prefetch_related('reviews').all()
    ser = ProductReviewsSerializer(products, many=True)
    return Response(ser.data)