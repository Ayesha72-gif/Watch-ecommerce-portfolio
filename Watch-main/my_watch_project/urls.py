"""
URL configuration for my_watch_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from mywatchapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name="main"),
    path('navbar_top/', views.navbar_top, name="navbar_top"),
    path('main_navbar/', views.main_navbar, name="main_navbar"),
    path('items_nav/', views.items_nav, name="items_nav"),
    
    
    
    
    
    # authentication urls======
    path('signup/', views.signup, name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    
    
    
    path('product_list/', views.product_list, name="product_list"),
    path('products/new/', views.product_list, {'page_type':'new'}, name="new_arrivals"),
    path('products/popular/', views.product_list, {'page_type':'popular'}, name="popular_products"),
    path('products/men/', views.product_list, {'page_type':'men'}, name="men_products"),
    path('products/women/', views.product_list, {'page_type':'women'}, name="women_products"),
    path('product_detail/<int:id>/', views.product_detail, name="product_detail"),
    path('related_image/<int:id>/', views.related_image_detail, name="related_image_detail"), 
    path('nested_admin', include('nested_admin.urls')),
    
    
    # cart urls==============
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name="add_to_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("place-order/", views.place_order, name="place_order"),
    path("add-related/<int:product_id>/<int:related_image_id>/", views.add_related_to_cart, name="add_to_cart_related"),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('admin_orders/', views.admin_orders, name="admin_orders"),
    path('admin_order_detail/<int:order_id>/', views.admin_order_detail, name="admin_order_detail"),
    path('my_orders/', views.my_orders, name="my_orders"),
    path('my_order_detail/<int:order_id>/', views.my_order_detail, name='my_order_detail'),


    path('cart/', views.cart_view, name="cart_view"),
    
    path('remove_from_cart/<str:key>/',views.remove_from_cart, name="remove_from_cart"),
    path('increase_quantity/<str:key>/', views.increase_quantity, name="increase_quantity"),
    path('decrease_quantity/<str:key>/', views.decrease_quantity, name="decrease_quantity"),
    
    
    # ===========blog page urls-===================
    path('blog_list/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    
# shipping
    path('save_address/', views.save_address, name="save_address"),
    path('about/',views.about, name="about"),
    path('contact/', views.contact_page, name="contact"),
    
    path('footer/', views.footer, name="footer"),
    
    
    
    
]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)