from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    user_age = models.PositiveSmallIntegerField(validators=[MinValueValidator(15), MaxValueValidator(70)], null=True, blank=True)
    user_phone_number = PhoneNumberField(null=True, blank=True)
    account_created_date = models.DateField(auto_now_add=True)
    STATUS_CHOICES = (
        ('gold', 'gold'),
        ('silver', 'silver'),
        ('bronze', 'bronze'),
        ('simple', 'simple')
    )
    membership_status = models.CharField(choices=STATUS_CHOICES, default='simple')

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'

class Category(models.Model):
    icon_file = models.FileField(upload_to='category_icons/', blank=True, null=True)
    category_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return f'{self.category_name}'

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_category')
    subcategory_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return f'{self.category} - {self.subcategory_name}'

class Product(models.Model):
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='sub_category_product')
    product_name = models.CharField(max_length=64)
    product_owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    article_number = models.PositiveSmallIntegerField(unique=True)
    description = models.TextField()
    is_original = models.BooleanField(default=False)
    video_file = models.FileField(upload_to='product_videos/', null=True, blank=True)
    product_price = models.PositiveIntegerField()
    product_created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name

    def get_avg_rating(self):
        rating = self.reviews_connect_product.all()
        if rating.exists():
            return round(sum([i.rating_stars for i in rating]) / rating.count(), 1)
        return 0

    def get_count_review(self):
        return self.reviews_connect_product.count()

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images_connect_product')
    image_file = models.ImageField(upload_to='product_image/', null=True, blank=True)

    def __str__(self):
        return f'{self.product}, {self.image_file}'

class Reviews(models.Model):
    review_author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews_connect_product')
    review_text = models.TextField()
    rating_stars = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product} - {self.rating_stars}'

class Cart(models.Model):
    product_owner = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product_owner}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    item_quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.product}, {self.item_quantity}'

class Favorite(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.profile}'

class FavoriteItem(models.Model):
    carts = models.ForeignKey(Cart, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.products}'
