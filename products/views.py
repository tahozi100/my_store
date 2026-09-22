from django.shortcuts import render, get_object_or_404, redirect
from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

# إضافة منتج للسلة
def add_to_cart(request, pk):
    cart = request.session.get('cart', {})
    pk_str = str(pk)
    cart[pk_str] = cart.get(pk_str, 0) + 1
    request.session['cart'] = cart
    return redirect('cart_detail')

# عرض محتويات السلة
def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for pk_str, quantity in cart.items():
        product = get_object_or_404(Product, pk=int(pk_str))
        item_total = product.price * quantity
        total_price += item_total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total,
        })

    return render(request, 'products/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

# تفريغ السلة
def clear_cart(request):
    if 'cart' in request.session:
        del request.session['cart']
    return redirect('cart_detail')