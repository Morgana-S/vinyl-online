from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile, DeliveryAddress
from .forms import UserProfileForm
# Create your views here.


@login_required
def user_profile_view(request):
    """
    View for viewing user profiles. Contains information on the user's
    contact info, order history, and provides a dashboard to contact support
    or access various features useful to the user.
    """

    profile = get_object_or_404(UserProfile, user=request.user)
    addresses = DeliveryAddress.objects.filter(user__user=request.user)

    context = {
        'profile': profile,
        'addresses': addresses,
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
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    context = {
        'form': form
    }

    return render(request, 'profiles/create_edit_profile.html', context)
