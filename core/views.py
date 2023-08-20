from django.shortcuts import render
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import CheckoutForm
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from .forms import UpdateQuantityForm

def product_list(request):
    products = Product.objects.all()
    cart_count = request.session.get('cart_count', 0)
    return render(request, 'product_list.html', {'products': products, 'cart_count': cart_count})


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'product_detail.html', {'product': product})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})




@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 0})
    cart_item.quantity += 1
    cart_item.save()

    # Update the cart count in session
    cart_count = request.session.get('cart_count', 0)
    request.session['cart_count'] = cart_count + 1

    return redirect('product_list')


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    # Check if cart is empty
    if not cart_items.exists():
        messages.info(request, "You have no items in the cart.")
    
    cart_count = request.session.get('cart_count', 0)

    total = sum([item.product.price * item.quantity for item in cart_items])
    return render(request, 'cart.html', {'cart_items': cart_items, 'cart_count': cart_count, 'total':total})


@login_required
def remove_from_cart(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
        if cart_item.cart.user == request.user:
            cart_item.delete()
    except ObjectDoesNotExist:
        messages.error(request, "The item you're trying to remove does not exist in the cart.")
    return redirect('cart')



@login_required
def update_cart_item_quantity(request):
    if request.method == 'POST':
        form = UpdateQuantityForm(request.POST)
        if form.is_valid():
            cart_item_id = form.cleaned_data['cart_item_id']
            quantity = form.cleaned_data['quantity']
            
            try:
                cart_item = CartItem.objects.get(id=cart_item_id)
                delta_quantity = quantity - cart_item.quantity
                cart_count = request.session.get('cart_count', 0)
                request.session['cart_count'] = cart_count + delta_quantity
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, 'Quantity updated successfully.')
                return redirect('cart')

            except CartItem.DoesNotExist:
                messages.error(request, 'CartItem not found.')
                return redirect('cart')

            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
                return redirect('cart')
    else:
        # This block handles GET requests and can redirect to the cart or another appropriate page.
        return redirect('cart')


from django.conf import settings
import stripe

def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data.get('payment_method')
            
            if payment_method == 'card':
                token = request.POST.get('stripeToken')
                stripe.api_key = settings.STRIPE_SECRET_KEY

                try:
                    charge = stripe.Charge.create(
                        amount=1000,  # in cents, you can dynamically set this based on cart total
                        currency="usd",
                        source=token,
                        description="Payment for Order",
                    )
                    # Handle order completion (e.g., save the order, reduce stock, send confirmation email)
                except stripe.error.CardError as e:
                    # Handle card error (e.g., card declined)
                    messages.error(request, "Card error: " + str(e))
                    return redirect('checkout')

            elif payment_method == 'cash':
                # Handle order for cash on delivery (e.g., save the order, send confirmation email)
                pass

            return redirect('order_success')  # Redirect to a success page or order summary page
            
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {'form': form})


import stripe

def payment(request):
    if request.method == 'POST':
        token = request.POST.get('stripeToken')

        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            charge = stripe.Charge.create(
                amount=1000,  # in cents
                currency="usd",
                source=token,
                description="Payment for Order",
            )
            # Handle order completion (e.g., save the order, reduce stock, etc.)
        except stripe.error.CardError as e:
            messages.error(request, "There was an error processing your payment: " + str(e))
            return redirect('checkout')


    return render(request, 'payment_result.html', {'charge': charge})

def order_success(request):
    return render(request, 'payment_result.html')
