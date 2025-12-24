from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# Create your models here.
class Product(models.Model):
    image=models.ImageField(upload_to="product/%y/%m/%d")
    name=models.CharField(max_length=200,)
    price=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    catagory=models.ForeignKey('Catagory', on_delete=models.CASCADE, null=True, blank=True)
    color=models.CharField(max_length=100, null=True, blank=True)
    brand=models.CharField(max_length=100, null=True, blank=True)
    
    
    
    is_new=models.BooleanField(default=False)
    is_popular=models.BooleanField(default=False)
    is_men=models.BooleanField(default=False)
    is_women=models.BooleanField(default=False)
    def __str__(self):
        return self.name
class Catagory(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)  # optional, URLs me use ke liye
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class ProductDetail(models.Model):
    product=models.OneToOneField(Product, on_delete=models.CASCADE)
    image= models.ImageField(upload_to="product/%y/%m/%d")
    price=models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at=models.DateTimeField(auto_now_add=True)
    description=models.TextField()
    def __str__(self):
        return f"{self.product.name} Details"
    
class ProductRelatedImages(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name="related_images")
    image=models.ImageField(upload_to="product/%y/%m/%d")
    title=models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.title or f"Image of {self.product.name}"
    
class RelatedImageDetail(models.Model):
    related_image=models.OneToOneField(ProductRelatedImages, on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at=models.DateTimeField(auto_now_add=True)
    description=models.TextField()
    def __str__(self):
        return f"Detail for {self.related_image.title}"
    
    # cart items model=================
    
     
class CartItem(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    related_image = models.ForeignKey(
        ProductRelatedImages, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    quantity=models.PositiveIntegerField(default=1)
  
    def subtotal(self):
        return self.quantity * self.product.price
    def image(self):
        return self.product.image.url

    def __str__(self):
        return f"{self.product.name}  {self.quantity}"
    
    
class ShippingAddress(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    full_name=models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    city=models.CharField(max_length=200)
    address=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    defualt=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.full_name} - {self.city}"
    
    
    
class Order(models.Model):
    STATUS_CHOICES=(
        ("pending", "Pending"),
        ('confirmed', "Confirmed"),
        ('shipped', "Shipped"),
        ('delieverd', "Delieverd"),
        ('cancelled', "Cancelled"),
    )
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    address=models.TextField()
    payment_method = models.CharField(max_length=50)
    total_price=models.CharField(max_length=100)
    status=models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Order #{self.id}- {self.user.username}"
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    related_image = models.ForeignKey(
        ProductRelatedImages,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    def subtotal(self):
        return sum(item.total_price() for item in self.orderitem_set.all())

    def shipping_cost(self):
        return 250

    def total(self):
        return self.subtotal() + self.shipping_cost()
    
    
    
class About(models.Model):
    aboutMission=models.TextField()
    aboutVision=models.TextField()
    image = models.ImageField(upload_to='about/', null=True, blank=True)

    def __str__(self):
        return self.aboutMission
    
    
    
    
    
    
    
    
    
# ================blog page models=================

class BlogCategory(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name








class Blog(models.Model):
    title=models.CharField(max_length=200)
    slug=models.SlugField(unique=True, blank=True)
    category=models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True)
    image=models.ImageField(upload_to="blog/%y/%m/%d")
    short_description=models.TextField()
    content=models.TextField()
    auther=models.CharField(max_length=100, default='Admin')
    created_at=models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title
    
class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)
    email      = models.EmailField()
    phone      = models.CharField(max_length=20)
    address    = models.CharField(max_length=255)
    message    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name