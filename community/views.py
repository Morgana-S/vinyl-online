from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from .forms import SupportTicketForm
from .models import SupportTicket
# Create your views here.


def create_support_ticket_view(request):
    """
    View for creating a support ticket. If the user
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
            form = SupportTicketForm()

    context = {
        'form': form
    }

    return render(request, 'community/create_support_ticket.html', context)


def ticket_detail_view(request, pk):
    """
    View for seeing support ticket details.
    """
    ticket = get_object_or_404(SupportTicket, pk=pk)

    context = {
        'ticket': ticket
    }

    return render(request, 'community/ticket_detail.html', context)
