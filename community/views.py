from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from checkout.models import Order
from .forms import SupportTicketForm, NewsletterSubscriptionForm, ReviewForm
from .models import SupportTicket
from records.models import Record, Review
# Create your views here.


def create_support_ticket_view(request):
    """
    View for creating a support ticket. If the user is signed in, contact
    info will be populated from their personal profile. An email is also
    sent to the user on support ticket creation.

    **Context**
    ``form``
        The form used to create a support ticket.

    **Template**
    :template:`community/create_support_ticket.html`
    """

    if request.user.is_authenticated:
        if request.method == 'POST':
            form = SupportTicketForm(request.POST, user=request.user)
            if form.is_valid():
                ticket = form.save(commit=False)
                ticket.user = request.user
                ticket.save()

                # Confirmation Email
                ticket_url = request.build_absolute_uri(reverse(
                    'ticket_detail', kwargs={'pk': ticket.pk}
                ))
                subject = f'Vinyl Online - Support Ticket Ref. {ticket.pk}'
                html_message = render_to_string(
                    'emails/support_ticket_confirmation.html',
                    {'ticket': ticket,
                     'user': request.user,
                     'ticket_url': ticket_url}
                )
                plain_message = strip_tags(html_message)

                send_mail(
                    subject,
                    plain_message,
                    None,
                    [ticket.email],
                    html_message=html_message
                )

                messages.success(request,
                                 'Your support ticket has now been submitted.'
                                 ' You will receive an email with your ticket'
                                 ' details.')
                return redirect('profile')
            else:
                return JsonResponse({'errors': form.errors}, status=400)
        else:
            form = SupportTicketForm(user=request.user)
    else:
        if request.method == 'POST':
            form = SupportTicketForm(request.POST)
            if form.is_valid():
                ticket = form.save()

                # Confirmation Email
                ticket_url = request.build_absolute_uri(reverse(
                    'ticket_detail', kwargs={'pk': ticket.pk}
                ))
                subject = f'Vinyl Online - Support Ticket Ref. {ticket.pk}'
                html_message = render_to_string(
                    'emails/support_ticket_confirmation.html',
                    {'ticket': ticket,
                     'user': None,
                     'ticket_url': ticket_url}
                )
                plain_message = strip_tags(html_message)

                send_mail(
                    subject,
                    plain_message,
                    None,
                    [ticket.email],
                    html_message=html_message
                )

                messages.success(request,
                                 'Your support ticket has now been submitted.'
                                 ' You will receive an email with your ticket'
                                 ' details.')
                return redirect('index')
            else:
                return JsonResponse({'errors': form.errors}, status=400)
        else:
            form = SupportTicketForm()

    context = {
        'form': form
    }

    return render(request, 'community/create_support_ticket.html', context)


def ticket_detail_view(request, pk):
    """
    View for seeing support ticket details.

    **Context**
    ``ticket``
        The SupportTicket instance.

    **Template**
    :template:`community/ticket_detail.html`
    """
    ticket = get_object_or_404(SupportTicket, pk=pk)

    context = {
        'ticket': ticket
    }

    return render(request, 'community/ticket_detail.html', context)


@login_required
def support_ticket_history_view(request):
    """
    View for seeing all support tickets created by the user.

    **Context**
    ``support_tickets``
        All SupportTicket instances associated with the user.

    **Template**
    :template:`community/support_ticket_history.html`
    """
    support_tickets = SupportTicket.objects.filter(
        user=request.user).order_by('-created_at')

    context = {
        'support_tickets': support_tickets
    }

    return render(request, 'community/support_ticket_history.html', context)


def about_page_view(request):
    """
    View for the 'Who we are' page.

    **Template**
    :template:`community/about_us.html`
    """
    return render(request, 'community/about_us.html')


def newsletter_subscribe_view(request):
    """
    View for serving the form for users to subscribe to the newsletter.

    **Context**
    ``form``
        The form used to subscribe to the newsletter.

    **Template**
    :template:`community/newsletter_subscribe.html`
    """

    if request.user.is_authenticated:
        if request.method == 'POST':
            form = NewsletterSubscriptionForm(request.POST, user=request.user)
            if form.is_valid():
                subscription = form.save(commit=False)
                subscription.user = request.user
                subscription.save()

                # Confirmation Email
                subject = 'Vinyl Online - Newsletter Subscription Confirmation'
                html_message = render_to_string(
                    'emails/newsletter_subscription_confirmation.html',
                    {
                        'subscription': subscription,
                        'user': request.user
                    }
                )
                plain_message = strip_tags(html_message)

                send_mail(
                    subject,
                    plain_message,
                    None,
                    [subscription.email],
                    html_message=html_message
                )

                messages.success(request,
                                 "Thank you for subscribing! You'll receive "
                                 "an email confirmation of your subscription "
                                 "shortly.")
                return redirect('index')
        else:
            form = NewsletterSubscriptionForm(user=request.user)
    else:
        if request.method == 'POST':
            form = NewsletterSubscriptionForm(request.POST)
            if form.is_valid():
                subscription = form.save()

                # Confirmation Email
                subject = 'Vinyl Online - Newsletter Subscription Confirmation'
                html_message = render_to_string(
                    'emails/newsletter_subscription_confirmation.html',
                    {
                        'subscription': subscription,
                    }
                )
                plain_message = strip_tags(html_message)

                send_mail(
                    subject,
                    plain_message,
                    None,
                    [subscription.email],
                    html_message=html_message
                )

                messages.success(request,
                                 "Thank you for subscribing! You'll receive "
                                 "an email confirmation of your subscription "
                                 "shortly.")
                return redirect('index')
        else:
            form = NewsletterSubscriptionForm()

    context = {
        'form': form
    }

    return render(request, 'community/newsletter_subscribe.html', context)


@login_required
def add_review_view(request, record_slug):
    """
    View for creating record reviews. Takes information about the request
    user's order history to check eligibility for writing a review.

    **Context**
    ``form``
        The form for writing a review.

    ``is_reviewable``
        Checks whether the user meets eligibility criteria to review the
        record.

    ``has_reviewed``
        Checks if the user has already reviewed the record.

    **Template**
    :template:`community/add_review.html`
    """
    record = get_object_or_404(Record, slug=record_slug)
    is_reviewable = Order.objects.filter(
        user=request.user, items__record=record).exists()
    has_reviewed = Review.objects.filter(
        author=request.user, record=record).exists()

    if is_reviewable:
        if has_reviewed:
            messages.error(request, 'You have already provided a review for '
                           'this record.')
            return redirect('record_detail', record_slug=record_slug)
        else:
            if request.method == 'POST':
                form = ReviewForm(request.POST)
                if form.is_valid():
                    review = form.save(commit=False)
                    review.author = request.user
                    review.record = record
                    review.save()
                    messages.success(request, 'Review has now been '
                                     'successfully submitted and is now '
                                     'awaiting approval.')
                    return redirect('record_detail', record_slug=record_slug)
            else:
                form = ReviewForm()
    else:
        messages.error(request,
                       'You must purchase this record in order to provide a '
                       'review.')
        return redirect('record_detail', record_slug=record_slug)

    context = {
        'form': form,
        'is_reviewable': is_reviewable,
        'has_reviewed': has_reviewed,
    }

    return render(request, 'community/add_review.html', context)


@login_required
def delete_review_view(request, review_id):
    """
    View for deleting reviews. Listens for a POST request from the review
    author and deletes the review.
    """
    review = get_object_or_404(Review, pk=review_id)
    record = review.record
    if request.method == 'POST':
        if review.author == request.user:
            review.delete()
            messages.success(request, 'Your review has now been deleted.')
            return redirect('record_detail', record_slug=record.slug)
        else:
            messages.error(request, 'You can not delete this review as you '
                           'are not the author.')
            return redirect('record_detail', record_slug=record.slug)


def privacy_policy_view(request):
    """
    View for the privacy policy page.

    **Template**
    :template:`community/privacy_policy.html`
    """
    return render(request, 'community/privacy_policy.html')


def return_policy_view(request):
    """
    View for the return policy page.

    **Template**
    :template:`community/return_policy.html`
    """
    return render(request, 'community/return_policy.html')


def terms_of_service_view(request):
    """
    View for the terms of service.

    **Template**
    :template:`community/terms_of_service.html`
    """
    return render(request, 'community/terms_of_service.html')
