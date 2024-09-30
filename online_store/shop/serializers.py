from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'age',
                  'date_registered', 'phone_number', 'status']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
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
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    date_registered = serializers.DateTimeField(format='%d-%m-%Y-%H-%M')

    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name', 'age', 'phone_number', 'status', 'date_registered']



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']




class ProductPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhotos
        fields = ['image']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name']

class RatingSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    user = UserProfileSerializer()
    class Meta:
        model = Rating
        fields = ['id', 'user', 'product', 'stars']


class RatingSimpleSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = Rating
        fields = ['id', 'user', 'stars']

class ReviewSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format='%d-%m-%Y-%H-%M')
    product = ProductSerializer()
    author = UserProfileSerializer()

    class Meta:
        model = Review
        fields = ['id', 'author', 'text', 'product', 'parent_review', 'created_date']

class ProductListSerializer(serializers.ModelSerializer):
    product_photo = ProductPhotosSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'product_photo', 'price', 'average_rating', 'date']

    def get_average_rating(self, obj):
        return obj.get_average_rating()


class ProductDetailSerializer(serializers.ModelSerializer):
    product_photo = ProductPhotosSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    category = CategorySerializer()
    date = serializers.DateField(format='%d-%m-%Y')
    ratings = RatingSimpleSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    owner = UserProfileSerializer()


    class Meta:
        model = Product
        fields = ['id', 'category', 'product_name', 'product_photo', 'product_video',
                  'active', 'price', 'average_rating', 'description', 'date', 'ratings', 'reviews', 'owner']

    def get_average_rating(self, obj):
        return obj.get_average_rating()


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, source='product')

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'get_total_price']





class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(read_only=True, many=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()

