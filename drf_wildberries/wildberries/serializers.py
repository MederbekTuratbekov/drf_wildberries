from rest_framework import serializers
from .models import UserProfile, Category, SubCategory, Product, ProductImage, Reviews, Cart, CartItem, Favorite, FavoriteItem
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'user_age', 'user_phone_number', 'membership_status')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return UserProfile.objects.create_user(**validated_data)

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {'username': instance.username, 'email': instance.email},
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {'username': instance.username, 'email': instance.email},
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'user_age', 'user_phone_number', 'membership_status']


class UserProfileOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']


class UserProfileReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name']


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'icon_file', 'category_name']


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['subcategory_name']


class CategoryDetailSerializer(serializers.ModelSerializer):
    sub_category = SubCategorySerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = ['category_name', 'sub_category']


class SubCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'subcategory_name']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image_file']


class ReviewSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format='%d-%m-%y %H:%M', read_only=True)
    review_author = UserProfileReviewSerializer(read_only=True)

    class Meta:
        model = Reviews
        fields = ['review_author', 'review_text', 'rating_stars', 'created_date']


class ProductListSerializer(serializers.ModelSerializer):
    category = SubCategorySerializer(read_only=True)
    product_created_date = serializers.DateTimeField(format='%d-%m-%y %H:%M', read_only=True)
    product_owner = UserProfileOwnerSerializer(read_only=True)
    images_connect_product = ProductImageSerializer(read_only=True, many=True)
    get_avg_rating = serializers.SerializerMethodField()
    get_count_review = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'images_connect_product', 'category', 'product_price',
                  'product_created_date', 'is_original', 'product_owner', 'get_avg_rating', 'get_count_review']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_review(self, obj):
        return obj.get_count_review()


class ProductDetailSerializer(serializers.ModelSerializer):
    category = SubCategorySerializer(read_only=True)
    product_created_date = serializers.DateTimeField(format='%d-%m-%y %H:%M', read_only=True)
    product_owner = UserProfileOwnerSerializer(read_only=True)
    images_connect_product = ProductImageSerializer(read_only=True, many=True)
    reviews_connect_product = ReviewSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'video_file', 'images_connect_product', 'category', 'product_price',
                  'product_created_date', 'is_original', 'article_number', 'description',
                  'product_owner', 'reviews_connect_product']


class SubCategoryDetailSerializer(serializers.ModelSerializer):
    sub_category_product = ProductListSerializer(read_only=True, many=True)

    class Meta:
        model = SubCategory
        fields = ['subcategory_name', 'sub_category_product']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, source='product')
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'item_quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_all_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'product_owner', 'items', 'total_all_price']

    def get_total_all_price(self, obj):
        return obj.get_total_all_price()


class FavoriteItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, source='product')

    class Meta:
        model = FavoriteItem
        fields = ['id', 'favorite', 'product', 'product_id']
        read_only_fields = ['favorite']


class FavoriteSerializer(serializers.ModelSerializer):
    items = FavoriteItemSerializer(many=True, read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'profile', 'items']
