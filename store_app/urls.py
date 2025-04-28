from django.urls import path, include
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import (UserProfileViewSet, CategoryListAPIView, CategoryDetailAPIView, SubCategoryListAPIView, SubCategoryDetailAPIView, ProductListAPIView,
                    ProductDetailAPIView, ProductCreateAPIView, ProductEditAPIView, ReviewsViewSet, CartViewSet, CartItemViewSet, FavoriteViewSet,
                    FavoriteItemViewSet, RegisterView, CustomLoginView, LogoutView)


router = routers.SimpleRouter()
router.register(r'users', UserProfileViewSet, basename = 'users'),


urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name = 'register'),
    path('login/', CustomLoginView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('products/', ProductListAPIView.as_view(), name = 'product_list'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name = 'product_detail'),
    path('products/create/', ProductCreateAPIView.as_view(), name = 'product_create'),
    path('products/create/<int:pk>/', ProductEditAPIView.as_view(), name = 'product_edit'),
    path('categories/', CategoryListAPIView.as_view(), name = 'category_list'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name = 'category_detail'),
    path('sub-categories/', SubCategoryListAPIView.as_view(), name='sub-category_list'),
    path('sub-categories/<int:pk>/', SubCategoryDetailAPIView.as_view(), name='sub-category_detail'),
    path('cart/', CartViewSet.as_view(), name = 'cart_detail'),
    path('cart_items/', CartItemViewSet.as_view({'get':'list', 'post':'create'}), name = 'cart_item'),
    path('cart_items/<int:pk>/', CartItemViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('favorites/', FavoriteViewSet.as_view({'get':'list'}), name='favorites'),
    path('favorite_items/', FavoriteItemViewSet.as_view({'get':'list'}), name='favorite_items')
]
