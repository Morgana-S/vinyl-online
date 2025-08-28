from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile, DeliveryAddress
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
