# Import necessary libraries and modules
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.forms import UserCreationForm
from .forms import CheckoutForm, UpdateQuantityForm
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.views import generic
import stripe

# Display a list of all products
def product_list(request):
    # Fetch all the products from the database
    products = Product.objects.all()
    # Get the cart count from the session (or default to 0 if not set)
    cart_count = request.session.get('cart_count', 0)
    # Render the product list template with products and cart count
    return render(request, 'product_list.html', {'products': products, 'cart_count': cart_count})

# Display details of a specific product
def product_detail(request, product_id):
    # Fetch the specific product by its ID
    product = Product.objects.get(id=product_id)
    # Render the product detail template with the fetched product
    return render(request, 'product_detail.html', {'product': product})

# User registration view
class Register(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

# Add a product to the user's cart
@login_required
def add_to_cart(request, product_id):
    # Fetch the specific product by its ID
    product = Product.objects.get(id=product_id)
    # Retrieve or create a cart for the logged-in user
    cart, created = Cart.objects.get_or_create(user=request.user)
    # Retrieve or create a cart item for the specified product
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 0})
    # Increase the quantity of the cart item by 1
    cart_item.quantity += 1
    cart_item.save()

    # Update the cart count in the session
    cart_count = request.session.get('cart_count', 0)
    request.session['cart_count'] = cart_count + 1

    # Redirect to the product list view
    return redirect('product_list')

# View the user's cart
@login_required
def view_cart(request):
    # Retrieve or create a cart for the logged-in user
    cart, created = Cart.objects.get_or_create(user=request.user)
    # Fetch all cart items associated with the cart
    cart_items = CartItem.objects.filter(cart=cart)
    
    # Check if the cart is empty and display a message if it is
    if not cart_items.exists():
        messages.info(request, "You have no items in the cart.")
    
    # Get the cart count from the session
    cart_count = request.session.get('cart_count', 0)
    # Calculate the total price of all items in the cart
    total = sum([item.product.price * item.quantity for item in cart_items])
    # Render the cart template with cart items, cart count, and total price
    return render(request, 'cart.html', {'cart_items': cart_items, 'cart_count': cart_count, 'total': total})

# Remove a specific item from the user's cart
@login_required
def remove_from_cart(request, cart_item_id):
    try:
        # Fetch the specific cart item by its ID
        cart_item = CartItem.objects.get(id=cart_item_id)
        # Ensure the cart item belongs to the logged-in user before deleting
        if cart_item.cart.user == request.user:
            cart_item.delete()
    except ObjectDoesNotExist:
        messages.error(request, "The item you're trying to remove does not exist in the cart.")
    # Redirect to the cart view
    return redirect('cart')

# Update the quantity of a specific item in the user's cart
@login_required
def update_cart_item_quantity(request):
    if request.method == 'POST':
        # Process the submitted form data
        form = UpdateQuantityForm(request.POST)
        if form.is_valid():
            cart_item_id = form.cleaned_data['cart_item_id']
            quantity = form.cleaned_data['quantity']
            
            try:
                # Fetch the specific cart item by its ID
                cart_item = CartItem.objects.get(id=cart_item_id)
                # Calculate the change in quantity
                delta_quantity = quantity - cart_item.quantity
                # Update the cart count in the session
                cart_count = request.session.get('cart_count', 0)
                request.session['cart_count'] = cart_count + delta_quantity
                # Update the cart item's quantity
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, 'Quantity updated successfully.')
                return redirect('cart')

            # Handle exceptions for cart item not found and other errors
            except CartItem.DoesNotExist:
                messages.error(request, 'CartItem not found.')
                return redirect('cart')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
                return redirect('cart')
    else:
        # Redirect to the cart view for GET requests
        return redirect('cart')

# Process payment for the user's cart
def checkout(request):
    if request.method == 'POST':
        # Process the submitted form data
        form = CheckoutForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data.get('payment_method')
            
            # Process card payment using Stripe
            if payment_method == 'card':
                token = request.POST.get('stripeToken')
                stripe.api_key = settings.STRIPE_SECRET_KEY
                try:
                    # Create a charge on Stripe
                    charge = stripe.Charge.create(
                        amount=1000,  # in cents
                        currency="usd",
                        source=token,
                        description="Payment for Order",
                    )
                except stripe.error.CardError as e:
                    # Handle card errors
                    messages.error(request, "Card error: " + str(e))
                    return redirect('checkout')
            # Handle cash on delivery payment method
            elif payment_method == 'cash':
                pass
            # Redirect to a success page after processing the payment
            return redirect('order_success')  
    else:
        form = CheckoutForm()
    # Render the checkout template with the form
    return render(request, 'checkout.html', {'form': form})

# Process payment using Stripe
def payment(request):
    if request.method == 'POST':
        token = request.POST.get('stripeToken')
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create a charge on Stripe
            charge = stripe.Charge.create(
                amount=1000,  # in cents
                currency="usd",
                source=token,
                description="Payment for Order",
            )
        except stripe.error.CardError as e:
            # Handle card errors
            messages.error(request, "There was an error processing your payment: " + str(e))
            return redirect('checkout')
    # Render the payment result template with the charge details
    return render(request, 'payment_result.html', {'charge': charge})

# Display a success page after processing payment
def order_success(request):
    return render(request, 'payment_result.html')
