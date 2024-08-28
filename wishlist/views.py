"""wishlist views"""
# pylint: disable=locally-disabled, no-member
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from profiles.models import UserProfile
from . models import Wishlist


@login_required
def wishlist(request):
    """ wishlist page """

    template = 'wishlist/wishlist.html'
    context = {
        'on_page': True,
    }
    return render(request, template, context)


@login_required
def add_to_wishlist(request, product_id):
    """ View to add product to wishlist"""
    user = UserProfile.objects.get(user=request.user)
    product = get_object_or_404(Product, pk=product_id)
    wishlist_exists = Wishlist.objects.filter(user=user,  product= product).exists()

    if wishlist_exists:
        wishlist_item = Wishlist.objects.get(
            user=user,
             Product= product
        )
        wishlist_item.delete()
        messages.info(request, 'Removed from wishlist')
        return redirect(reverse(' product_detail', args=[product.id]))
    else:
        wishlist_item = Wishlist.objects.create(
            user=user,
             Product= product
        )
        messages.success(
            request, f'Successfully added {wishlist_item} to wishlist')
        return redirect(reverse(' product_detail', args=[ product.id]))


@login_required
def remove_from_wishlist(request,  product_id):
    """ Remove from wishlist"""
    user = UserProfile.objects.get(user=request.user)
    product = get_object_or_404( Product, pk= product_id)
    wishlist_item = Wishlist.objects.get(user=user,  Product= product)
    wishlist_item.delete()
    messages.success(request, f'Successfully removed { product.name}')
    return redirect(reverse('wishlist'))