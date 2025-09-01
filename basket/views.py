from django.shortcuts import render

# Create your views here.


def view_basket(request):
    """
    View for viewing the total items in the shopping basket.
    """
    return render(request, 'basket/view_basket.html')