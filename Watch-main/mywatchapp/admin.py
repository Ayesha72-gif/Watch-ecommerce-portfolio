import nested_admin
from django.contrib import admin
from .models import CartItem, Product, ProductDetail, ProductRelatedImages, RelatedImageDetail
# Register your models here.
from .models import Product, ProductDetail, RelatedImageDetail, ProductRelatedImages, Catagory, ShippingAddress, Order, OrderItem, About, Blog, BlogCategory, Contact

class RelatedImageDetailInline(nested_admin.NestedStackedInline):
    model=RelatedImageDetail
    max_num=1
    extra=1
    
    
class ProductRelatedImagesInline(nested_admin.NestedTabularInline):
    model=ProductRelatedImages
    inlines=[RelatedImageDetailInline]
    extra=1
    
    
class ProductDetailInline(nested_admin.NestedStackedInline):
    model=ProductDetail
    max_num=1
    
class ProductAdmin(nested_admin.NestedModelAdmin):
    inlines=[ProductDetailInline, ProductRelatedImagesInline]
    list_display=('name',)
    
admin.site.register(Product, ProductAdmin)
admin.site.register(Catagory)
admin.site.register(CartItem)
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(About)
admin.site.register(BlogCategory)
admin.site.register(Blog)
admin.site.register(Contact)

