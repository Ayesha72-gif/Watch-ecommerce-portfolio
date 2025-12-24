from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from .models import Product, ProductDetail, ProductRelatedImages, RelatedImageDetail, Catagory, CartItem, ShippingAddress, OrderItem, Order, About, Blog, BlogCategory, Contact

# Create your views here.
def navbar_top(request):
    return render(request, "navbar_top.html")
def main_navbar(request):
    return render(request, "main_navbar.html")
def items_nav(request):
    return render(request, "items_nav.html")
def footer(request):
    return render(request, "footer.html")
def main(request):
    # Get latest 6 products for New Arrivals
    new_arrivals = Product.objects.filter(is_new=True)[:6]

    # Get popular items
    popular_items = Product.objects.filter(is_popular=True)[:6]

    return render(request, 'main.html', {
        'new_arrivals': new_arrivals,
        'popular_items': popular_items
    })

# ====================signup/login view=====================
def signup(request):
    if request.method =='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('signup')
        user=User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully")
        return redirect('login')
    return render(request, "signup.html")



# login//
def login_view(request):
    if request.method =='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product_list')
        else :
            messages.error(request, "Invalid Username or Password")
            return redirect('login')
    return render(request, "login.html")
# logout view//
def logout_view(request):
    logout(request)
    return redirect('login')   





# ================products views===============
def filter_products(requets, queryset):
    
    category=requets.GET.get('category')
    brand=requets.GET.get('brand')
    color=requets.GET.get('color')
    min_price=requets.GET.get('min_price')
    max_price=requets.GET.get('max_price')
    
    if category:
        queryset = queryset.filter(catagory_id=category)
    if brand:
        queryset = queryset.filter(brand=brand)
    if color:
        queryset= queryset.filter(color=color)
    if min_price:
        queryset= queryset.filter(min_price=min_price)
    if max_price:
        queryset= queryset.filter(max_price=max_price)
    return queryset
def product_list(request, page_type=None):
    
    products=Product.objects.all()
    if page_type=='new':
        products=products.filter(is_new=True)
    elif page_type =='popular':
        products=products.filter(is_popular=True)
    elif page_type =='men':
        products=products.filter(is_men=True)
    elif page_type== 'women':
        products=products.filter(is_women=True)
    products = filter_products(request, products)
    categories = Catagory.objects.all()
    brands = Product.objects.values_list('brand', flat=True).distinct()
    colors = Product.objects.values_list('color', flat=True).distinct()
    return render(request, "Product_list.html", {'products':products, 'categories':categories, 'brands':brands, 'colors':colors, 'page_type':page_type} )

def product_detail(request, id):
    produc=get_object_or_404(Product, id=id)
    main_detail=getattr(produc, "productdetail", None)
    related_images=produc.related_images.all()
    key = f"{produc.id}-0"
    qty = 1

    if request.user.is_authenticated:
        item = CartItem.objects.filter(
            user=request.user,
            product=produc,
            related_image=None
        ).first()
        if item:
            qty = item.quantity
    else:
        cart = request.session.get("cart", {})
        if key in cart:
            qty = cart[key]["quantity"]
    return render(request, "product_detail.html", {'produc':produc, 'main_detail':main_detail, 'related_images':related_images, 'key': key, 'qty':qty })


# Related Images Detail Page
def related_image_detail(request, id):
    img = get_object_or_404(ProductRelatedImages, id=id)
    detail = getattr(img, 'relatedimagedetail', None)
    other_related_images = img.product.related_images.exclude(id=img.id)

    # Pass the product object to the template
    product = img.product
    key = f"{product.id}-{img.id}"
    qty = 1

    if request.user.is_authenticated:
        item = CartItem.objects.filter(
            user=request.user,
            product=product,
            related_image=img
        ).first()
        if item:
            qty = item.quantity
    else:
        cart = request.session.get("cart", {})
        if key in cart:
            qty = cart[key]["quantity"]


    return render(request, "related_image_detail.html", {
        'img': img,
        'detail': detail,
        'other_related_images': other_related_images,
        'product': product, 
        'key': key,
        "qty": qty,
    })
    
    


# 





# Add normal product to cart
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_id = 0  # Normal product has related_id = 0

    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            related_image=None
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    else:
        cart = request.session.get('cart', {})
        pid = f"{product_id}-{related_id}"
        if pid in cart:
            cart[pid]['quantity'] += 1
        else:
            cart[pid] = {
                'name': product.name,
                'price': float(product.price),
                'quantity': 1,
                'image': product.image.url if product.image else '',
            }
        request.session['cart'] = cart
        request.session.modified = True

    return redirect(request.META.get('HTTP_REFERER', '/'))

# Add related product to cart
def add_related_to_cart(request, product_id, related_image_id):
    product = get_object_or_404(Product, id=product_id)
    related_image = get_object_or_404(ProductRelatedImages, id=related_image_id)

    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            related_image=related_image
        )
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart = request.session.get("cart", {})
        pid = f"{product_id}-{related_image_id}"
        if pid in cart:
            cart[pid]["quantity"] += 1
        else:
            cart[pid] = {
                "name": product.name,
                "price": float(product.price),
                "quantity": 1,
                "image": related_image.image.url,
            }
        request.session["cart"] = cart
        request.session.modified = True

    return redirect(request.META.get("HTTP_REFERER", '/'))









def cart_view(request):
    total = 0
    if request.user.is_authenticated:
        items = CartItem.objects.filter(user=request.user)
        addresses = ShippingAddress.objects.filter(user=request.user)
        cart = {}

        for item in items:
            key = f"{item.product.id}-{item.related_image.id if item.related_image else 0}"
            image_url = item.related_image.image.url if item.related_image else item.product.image.url
            price = float(item.product.price) if item.product.price else 0
            subtotal = price * item.quantity

            cart[key] = {
                'name': item.product.name,
                'price': price,
                'quantity': item.quantity,
                'image': image_url,
                'subtotal': subtotal,
            }
            total += subtotal
    else:
        addresses = None
        cart = request.session.get('cart', {})
        for item in cart.values():
            item['subtotal'] = item['price'] * item['quantity']
            total += item['subtotal']

    return render(request, "cart.html", {'cart': cart, 'total': total, 'addresses': addresses})














def remove_from_cart(request, key):
    if request.user.is_authenticated:
        ids = key.split('-')
        product_id = int(ids[0])
        related_id = int(ids[1])
        CartItem.objects.filter(
            user=request.user,
            product_id=product_id,
            related_image_id=related_id if related_id != 0 else None
        ).delete()
    else:
        cart = request.session.get('cart', {})
        if key in cart:
            del cart[key]
        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart_view')






















def increase_quantity(request, key):
    ids = key.split("-")
    product_id = int(ids[0])
    related_id = int(ids[1])

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(
            user=request.user,
            product_id=product_id,
            related_image_id=related_id if related_id != 0 else None
        )
        for item in cart_items:
            item.quantity += 1
            item.save()
    else:
        cart = request.session.get("cart", {})
        if key in cart:
            cart[key]["quantity"] += 1
        request.session["cart"] = cart
        request.session.modified = True
    return redirect(request.META.get("HTTP_REFERER", "cart_view"))
    # return redirect('cart_view')

def decrease_quantity(request, key):
    ids = key.split("-")
    product_id = int(ids[0])
    related_id = int(ids[1])

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(
            user=request.user,
            product_id=product_id,
            related_image_id=related_id if related_id != 0 else None
        )
        for item in cart_items:
            item.quantity -= 1
            if item.quantity <= 0:
                item.delete()
            else:
                item.save()
    else:
        cart = request.session.get("cart", {})
        if key in cart:
            cart[key]["quantity"] -= 1
            if cart[key]["quantity"] <= 0:
                del cart[key]
        request.session["cart"] = cart
        request.session.modified = True
    return redirect(request.META.get("HTTP_REFERER", "cart_view"))
    # return redirect('cart_view')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
def place_order(request):
    if request.method != 'POST':
        return redirect('checkout')
    user =request.user
    address_id=request.POST.get('address_id')
    payment_method=request.POST.get('payment_method')
    subtotal = float(request.POST.get("subtotal"))
    shipping=float(request.POST.get('shipping'))
    total = float(request.POST.get("total"))
    
    address = get_object_or_404(ShippingAddress, id=address_id, user=user)
    items = CartItem.objects.filter(user=user)
    
    order =Order.objects.filter(user=user)
    if not items:
        messages.error(request, "Your cart is empty")
        return redirect('cart_view1')
    
    order=Order.objects.create(
        user=user,
        address=f"{address.full_name}, {address.phone}, {address.city}, {address.address}",
        payment_method=payment_method,
        total_price=total,
        status="pending",
    )
    for item in items:
        price = (
        item.related_image.relatedimagedetail.price
        if item.related_image and hasattr(item.related_image, "relatedimagedetail")
        else item.product.price
    )
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            related_image=item.related_image,
            price=price,
            total_price=price * item.quantity
            # price=item.product.price,
            # total_price=item.product.price * item.quantity
        )
        item.delete()
    return redirect(reverse('order_confirmation', args=[order.id]))
    
# checkout view===============
def checkout(request):
    if not request.user.is_authenticated:
        return redirect("login")
    items=CartItem.objects.filter(user=request.user) 
    if not items.exists():
        messages.error(request, "Your Cart is empty")
        return redirect("cart_view1")
    addresses=ShippingAddress.objects.filter(user=request.user)
    subtotal=sum(item.product.price * item.quantity for item in items)   
    shipping= 250
    final_total=subtotal + shipping
    
    return render(request, "checkout.html", {"items":items, "addresses":addresses, "subtotal":subtotal, "shipping":shipping, "final_total":final_total})    

def save_address(request):
    if request.method =='POST':
        full_name=request.POST.get('full_name')
        phone=request.POST.get('phone')
        city=request.POST.get('city')
        address=request.POST.get('address')
        if full_name and phone and city and address:
            ShippingAddress.objects.create(
                user=request.user,
                full_name=full_name,
                phone=phone,
                city=city,
                address=address
            )
        return redirect('cart_view')
    
    
    
    
    
    
    # order_confirmation
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    subtotal = sum(item.total_price for item in order.items.all())
    shipping = 250  # ya jitna bhi tumhara shipping cost ho
    final_total = subtotal + shipping
    return render(request,"order_confirmation.html", {"order":order, "subtotal":subtotal, "shipping":shipping, "final_total":final_total} )


# admin==========================
def is_admin(user):
    return user.is_superuser
# adminviews=======================
def admin_orders(request):
    orders=Order.objects.all().order_by('-created_at')
    return render(request,"admin_orders.html", {'orders':orders})
def admin_order_detail(request, order_id):
    order=get_object_or_404(Order, id=order_id)
    return render(request, "admin_order_detail.html", {'order':order} )


# loggedin cutomer order_view===============================


def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "my_orders.html", {'orders':orders})

def my_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "my_order_detail.html", {'order':order})


def about(request):
    about=About.objects.first()
    return render(request, "about.html", {'about':about})













def blog_list(request):
    blogs=  Blog.objects.all().order_by('-created_at')
    categories=BlogCategory.objects.all()
    return render(request, "blog_list.html", {'blogs':blogs, 'categories':categories})

def blog_detail(request, slug):
    blog=get_object_or_404(Blog, slug=slug)
    return render(request, 'blog_detail.html', {'blog': blog})





def contact_page(request):
    if request.method == "POST":
        try:
            first_name = request.POST.get('first_name')
            last_name  = request.POST.get('last_name')
            email      = request.POST.get('email')
            phone      = request.POST.get('phone')
            address    = request.POST.get('address')
            message    = request.POST.get('message')

            # save to database
            Contact.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address,
                message=message
            )

            # ================= EMAIL TO ADMIN =================
            admin_subject = "📩 New Contact Message - Time Zone"
            admin_message = f"""
New Contact Message Received

Name: {first_name} {last_name}
Email: {email}
Phone: {phone}
Address: {address}

Message:
{message}
"""

            send_mail(
                admin_subject,
                admin_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],  # admin email
                fail_silently=False,
            )

            # ================= EMAIL TO USER =================
            user_subject = "✅ We received your message - Time Zone"

            user_html_message = f"""
            <h2>Hello {first_name},</h2>
            <p>Thank you for contacting <b>Time Zone Watches</b>.</p>
            <p><b>Your message:</b></p>
            <p>{message}</p>
            <br>
            <p>Regards,<br><b>Time Zone Watches Team</b></p>
            """

            email_msg = EmailMultiAlternatives(
                subject=user_subject,
                body="Thank you for contacting Time Zone Watches.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],
            )
            email_msg.attach_alternative(user_html_message, "text/html")
            email_msg.send()

            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')

        except Exception as e:
            print(e)
            messages.error(request, "Something went wrong. Please try again.")

    return render(request, 'contact.html')

