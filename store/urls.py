from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('new-product/', views.ProductCreateView.as_view(), name='product-create'),
    path('product/<slug:slug>/update/', views.ProductUpdateView.as_view(), name='product-update'),
    path('product/<slug:slug>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),
    path('search/', views.ItemSearchListView.as_view(), name='item_search_list'),
    path('deliveries/', views.DeliveryListView.as_view(), name='delivery-list'),
    path('delivery/<int:pk>/', views.DeliveryDetailView.as_view(), name='delivery-detail'),
    path('new-delivery/', views.DeliveryCreateView.as_view(), name='delivery-create'),
    path('delivery/<int:pk>/update/', views.DeliveryUpdateView.as_view(), name='delivery-update'),
    path('delivery/<int:pk>/delete/', views.DeliveryDeleteView.as_view(), name='delivery-delete'),
    path('get-items/', views.get_items_ajax_view, name='get-items-ajax'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)