from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from cart.cart import Cart
from .forms import OrderCreateForm

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            cart.clear()
            return redirect('order_confirmation', order_id=order.id)
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order_create.html', {'cart': cart, 'form': form})

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_confirmation.html', {'order': order})