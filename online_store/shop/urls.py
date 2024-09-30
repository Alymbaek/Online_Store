from django.urls import path
from .views import *

urlpatterns = [

    path('register/', RegisterView.as_view(), name='register_list'),
    path('login/', CustomLoginView.as_view(), name='login_list'),
    path('logout/', LogoutView.as_view(), name='logout_list'),

    path('', ProductListViewSet.as_view({'get': 'list',
                                         'post': 'create'}), name='product_list'),
    path('<int:pk>/', ProductDetailViewSet.as_view({'get': 'retrieve',
                                              'put': 'update',
                                              'delete': 'destroy'}), name='product_detail'),

    path('photos/', ProductPhotosViewSet.as_view({'get': 'list',
                                                  'post': 'create'}), name='photos_list'),
    path('photos/<int:pk>/', ProductPhotosViewSet.as_view({'get': 'retrieve',
                                                           'put': 'update',
                                                           'delete': 'destroy'}), name='photos_detail'),

    path('users/', UserProfileViewSet.as_view({'get': 'list',
                                               'post': 'create'}), name='users_list'),
    path('users/<int:pk>/', UserProfileViewSet.as_view({'get': 'retrieve',
                                                        'put': 'update',
                                                        'delete': 'destroy'}), name='users_detail'),

    path('category/', CategoryViewSet.as_view({'get': 'list',
                                               'post': 'create'}), name='category_list'),
    path('category/<int:pk>/', CategoryViewSet.as_view({'get': 'retrieve',
                                                        'put': 'update',
                                                        'delete': 'destroy'}), name='category_detail'),

    path('ratings/', RatingViewSet.as_view({'get': 'list',
                                            'post': 'create'}), name='rating_list'),
    path('ratings/<int:pk>/', RatingViewSet.as_view({'get': 'retrieve',
                                                     'put': 'update',
                                                     'delete': 'destroy'}), name='rating_detail'),

    path('review/', ReviewViewSet.as_view({'get': 'list',
                                           'post': 'create'}), name='review_list'),
    path('review/<int:pk>/', ReviewViewSet.as_view({'get': 'retrieve',
                                                    'put': 'update',
                                                    'delete': 'destroy'}), name='review_detail'),

    path('cart/', CartViewSet.as_view({'get': 'retrieve'}), name='cart_detail'),

    path('cart_items/', CartItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='cart_item_list'),
    path('cart_items/<int:pk>/', CartItemViewSet.as_view({'put': 'update', 'delete': 'destroy'})),

]

