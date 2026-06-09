from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductListSerializer, ProductDetailSerializer, ReviewSerializer, ProductReviewsSerializer


@api_view(['GET', 'POST'])
def category_list_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        ser = CategorySerializer(categories, many=True)
        return Response(ser.data)

    elif request.method == 'POST':
        ser = CategorySerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_view(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        ser = CategorySerializer(category)
        return Response(ser.data)

    elif request.method == 'PUT':
        ser = CategorySerializer(category, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def product_list_view(request):
    products = Product.objects.select_related("category").all()
    ser = ProductListSerializer(products, many=True)
    return Response(ser.data)

@api_view(['GET', 'POST'])
def product_detail_view(request):
    if request.method == 'GET':
        product = Product.objects.all()
        ser = ProductDetailSerializer(product, many=True)
        return Response(ser.data)
    elif request.method == 'POST':
        ser = ProductDetailSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    try:
        prod = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({"error": "Товар не найден"}, status=status.HTTP_404_NOT_FOUND)
    ser = ProductDetailSerializer(prod)
    return Response(ser.data)


@api_view(['GET', 'POST'])
def review_list_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        ser = ReviewSerializer(reviews, many=True)
        return Response(ser.data)

    elif request.method == 'POST':
        ser = ReviewSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_view(request, pk):
    try:
        rev = Review.objects.get(pk=pk)
    except Review.DoesNotExist:
        return Response({"error": "Отзыв не найден"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        ser = ReviewSerializer(rev)
        return Response(ser.data)
    elif request.method == 'PUT':
        ser = ReviewSerializer(rev, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        rev.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def product_with_reviews_list_view(request):
    products = Product.objects.prefetch_related('reviews').all()
    ser = ProductReviewsSerializer(products, many=True)
    return Response(ser.data)