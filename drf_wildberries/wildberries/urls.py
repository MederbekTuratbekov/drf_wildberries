from django.urls import path, include
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import (UserProfileViewSet, CategoryListAPIView, CategoryDetailAPIView,
                    SubCategoryListAPIView, SubCategoryDetailAPIView,
                    ProductListAPIView, ProductDetailAPIView, ProductCreateAPIView, ProductEditAPIView,
                    ReviewsViewSet, CartViewSet, CartItemViewSet, FavoriteViewSet, FavoriteItemViewSet,
                    RegisterView, CustomLoginView, LogoutView)

router = routers.SimpleRouter()
router.register(r'users', UserProfileViewSet, basename='users')
router.register(r'reviews', ReviewsViewSet, basename='reviews')

urlpatterns = [
    path('', include(router.urls)),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/create/', ProductCreateAPIView.as_view(), name='product-create'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('products/<int:pk>/edit/', ProductEditAPIView.as_view(), name='product-edit'),

    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),

    path('sub-categories/', SubCategoryListAPIView.as_view(), name='subcategory-list'),
    path('sub-categories/<int:pk>/', SubCategoryDetailAPIView.as_view(), name='subcategory-detail'),

    path('cart/', CartViewSet.as_view(), name='cart'),
    path('cart-items/', CartItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='cart-items'),
    path('cart-items/<int:pk>/', CartItemViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='cart-items-detail'),

    path('favorites/', FavoriteViewSet.as_view({'get': 'list', 'post': 'create'}), name='favorites'),
    path('favorite-items/', FavoriteItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='favorite-items'),
    path('favorite-items/<int:pk>/', FavoriteItemViewSet.as_view({'delete': 'destroy'}), name='favorite-items-detail'),
]
