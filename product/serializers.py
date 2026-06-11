from rest_framework import serializers
from .models import Category, Product, Review

class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "products_count"]

    def get_products_count(self, category):
        return category.products.count()

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Название категории должно содержать минимум 2 символа")
        if len (value) > 255:
            raise serializers.ValidationError("Название категории не не может быть длинее 255 символов")
        return value

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "text", "stars", "product"]

        def validate_text(self, value):
            value = value.strip()
            if len(value) < 5:
                raise serializers.ValidationError("Текст отзыва должен содержать минимум 5 символов")
            return value

        def validate_stars(self, value):
            if value < 1 or value > 5:
                raise serializers.ValidationError("Оценка stars должна быть в диапозоне от 1 до 5")
            return value



class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = ["id", "title", "price", "category"]

        def validate_title(self, value):
            value = value.strip()
            if len(value) < 2:
                raise serializers.ValidationError("Название товара должно содержать минимум 2 символа")
            return value

        def validate_price(self, value):
            if value <= 0:
                raise serializers.ValidationError("Цена товара должна быть больше 0")
            return value

class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = "__all__"

    def validate_title(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("Название товара должно содержать минимум 2 символа")
        return value

    def validate_description(self, value):
        value = value.strip()
        if len(value) < 10:
            raise serializers.ValidationError("Описание товара должно содержать минимум 10 символов")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена товара должна быть больше 0")
        return value

class ProductReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'reviews', 'average_rating']

    def get_average_rating(self, product):
        reviews = product.reviews.all()
        if not reviews:
            return 0
        total = sum(rev.stars for rev in reviews)
        return round(total / reviews.count(), 2)