from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from community.models import SupportTicket
from .models import UserProfile, DeliveryAddress
from checkout.models import Order
from .forms import UserProfileForm, DeliveryAddressForm
# Create your views here.


@login_required
def user_profile_view(request):
    """
    View for viewing user profiles. Contains information on the user's
    contact info, order history, and provides a dashboard to contact support
    or access various features useful to the user.
    """
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None

    addresses = DeliveryAddress.objects.filter(user=request.user)
    support_tickets = SupportTicket.objects.filter(user=request.user)
    order_history = Order.objects.filter(
        user=request.user).order_by('-created_at')

    context = {
        'profile': profile,
        'addresses': addresses,
        'support_tickets': support_tickets,
        'order_history': order_history
    }

    return render(request, 'profiles/profile.html', context)


@login_required
def create_edit_profile_view(request):
    """
    View for creating or editing a user profile's personal info.
    Contains a form that the user fills with relevant personal information.
    """
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your personal information has now '
                             'been updated.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    context = {
        'profile': profile,
        'form': form
    }

    return render(request, 'profiles/create_edit_profile.html', context)


@login_required
def create_delivery_address_view(request):
    """
    View for creating a delivery address. Contains a form that the user
    fills with relevant address information.
    """
    if request.method == 'POST':
        form = DeliveryAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'This address has now been saved.')
            return redirect('profile')
    else:
        form = DeliveryAddressForm()

    context = {
        'form': form
    }

    return render(request, 'profiles/create_delivery_address.html', context)


@login_required
def edit_delivery_address_view(request, pk):
    """
    View for editing existing delivery addresses. Uses the same form
    as the create_delivery_address view above.
    """
    address = get_object_or_404(DeliveryAddress, pk=pk, user=request.user)
    if request.method == 'POST':
        form = DeliveryAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address details have now been '
                             'changed.')
            return redirect('profile')
    else:
        form = DeliveryAddressForm(instance=address)

    context = {
        'form': form
    }
    return render(request, 'profiles/edit_delivery_address.html', context)


@login_required
def delete_delivery_address_view(request, pk):
    """
    View for deleting delivery addresses.
    """
    address = get_object_or_404(DeliveryAddress, pk=pk, user=request.user)

    if request.method == 'POST':
        address.delete()
        messages.success(request, 'Address has now been deleted.')
        return redirect('profile')
    else:
        return redirect('profile')
